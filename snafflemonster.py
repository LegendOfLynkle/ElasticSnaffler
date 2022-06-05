#!/usr/bin/env python3
import json
import argparse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index

def load_data(filename:str):
    with open(filename, "r") as snaffout:
        data = json.load(snaffout)
    return data

def post_data_to_elastic(data, index:str, es):
    triage_levels = ["Green", "Yellow", "Red", "Black"]
    snaffle = {}
    snaffle["entries"] = []
    ii = 0
    #TODO: optimise this process by bulk uploading documents if possible.
    for entry in data["entries"]:
        if(len(entry["eventProperties"].keys()) != 0):
            for triage_level in triage_levels:
                if(list(entry["eventProperties"].keys())[0] == triage_level):
                    if(entry["eventProperties"][triage_level]["Type"] == "FileResult"):
                        # send the data
                        resp = es.index(index=index, id=ii, document=entry["eventProperties"][triage_level])
                        # TODO: Add check for if response is an error before printing
                        print(resp)
                        ii = ii + 1

def setup_elastic_client(hostname:str, api_key:str, verify:str):
    es = Elasticsearch(
        f"https://{hostname}:9200/",
        api_key=api_key,
        verify_certs=verify)
    return es

def is_index_in_use(es, index_name):
    in_use = False
    if index_name in es.indices.get_alias("*"):
        in_use = True
    return in_use

def get_choice(es, index):
    valid = False
    valid_choice = ['a', 'r', 'i', 'q']
    # ask them how to handle it if it is in use
    count = es.cat.count(index, params={"format": "json"})[0]["count"]
    print(f"The {index} index is already in use and has {count} items stored. How would you like to proceed?")
    while not valid:
        choice = input(f"Please select one of the following options:\nA: Append data to the index\nR: Replace the data in the index. (Will delete old data first)\nI: Select a different index\nQ: Quit without doing anything.")
        if choice.lower() not in valid_choice:
            print(f"The option {choice} is not valid.")
        else:
            if choice == "a":
                valid = True
            if choice == "r":
                valid = True
            if choice == "i":
                temp_index = input("Please enter a name for the index you would like to use: ")
                # check if the index is in use
                if is_index_in_use(es, temp_index):
                    # if it is then redo the intial prompt.
                    count = es.cat.count(temp_index, params={"format": "json"})[0]["count"]
                    print(f"The {temp_index} index is already in use and has {count} items stored. How would you like to proceed?")
                else:
                # if not choice is valid and we need to return both.....
                    index = temp_index
                    valid = True
            if choice == "q":
                valid = True
    # if index has changed then cool, if it hasn't then we still have the original value going back out.
    return choice, index

def view(data, args):
    # This might look a bit weird but I have done it so it makes more logical sense when it is passed to other functions/configuration.
    insecure = not args.insecure
    index = ""
    apikey = ""
    hostname = args.hostname
    # This needs to be optimized more (logically).
    if args.apikey is not None:
        apikey = args.apikey
    else:
        if args.apikey is None:
            apikey = input("Please enter an API Key: ")
        else:
            apikey = args.apikey
    # now that we have all the required arguments, setup the elasticsearch client.
    es = setup_elastic_client(hostname, apikey, insecure)
    # Time to check the indexes to see if they already exist or not
    if args.index is not None:
        index = args.index
    else:
        # TODO add functionality here using the ES library to check for existing indicies
        index = input("Please enter a name for the index to use: ")
    # check if the index is in use
    if is_index_in_use(es, index):
        # ask them how to handle it if it is in use
        choice, index = get_choice(es, index)
        if choice == "r":
            # TODO: Add call here to delete items in the index/delete the index
            # This call here should work but I won't remove the the TODO until I have tested it.
            old_index = Index(index)
            old_index.delete(ignore=[400, 404])
            post_data_to_elastic(data, index, es)
        if choice == "a":
            # TODO: add functionality to append here.
            pass
        if choice == "i":
            # The new index is not in use and we can just post the data like normal.
            post_data_to_elastic(data, index, es)
        if choice == "q":
            print("You have chose to quit, aborting")
    else:
        # The index is not in use and we can just post no worries.
        post_data_to_elastic(data, index, es)

def main():
    parser = argparse.ArgumentParser(description="Send Snaffler Output to ElasticSearch for analysis.", epilog="Happy Snaffling")
    parser.add_argument("-f", "--file", type=str, help="The path to the JSON file to process.", required=True)
    parser.add_argument("-n", "--hostname", type=str, help="Hostname or IP pointing to the ElasticSearch instance.", required=True)
    parser.add_argument("-i", "--index", type=str, help="The name of the index to store results in.")
    parser.add_argument("-k", "--apikey", type=str, help="The API key used to authentiate to ElasticSearch.")
    parser.add_argument("-r", "--replace", type=str, help="Optional argument to delete existing items in the index selected before adding new items.")
    parser.add_argument("-a", "--append", type=str, help="Optional argument to append new items to the selected index.")
    parser.add_argument("--insecure", type=bool, help="Toggle for allowing sending over HTTPS with verification turned off so self signed or invalid ceritficates can be used.", default=False)
    args = parser.parse_args()
    data = load_data(args.file)
    view(data, args)

if __name__ == "__main__":
    main()
