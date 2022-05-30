#!/usr/bin/env python3
import json
import argparse
from elasticsearch import Elasticsearch

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
    # This might look a bit weird but I have done it so it makes more logical sense when it is passed to the requests function.
    insecure = not args.insecure

    data = load_data(args.file)

    if args.index is not None and args.apikey is not None:
        es = setup_elastic_client(args.hostname, args.apikey, insecure)
        post_data_to_elastic(data, args.index, es)
    else:
        if args.index is None:
            # TODO add functionality here using the ES library to check for existing indicies
            index = input("Please enter a name for the index to use: ")
        else:
            index = args.index
        if args.apikey is None:
            apikey = input("Please enter an API Key: ")
        else:
            apikey = args.apikey
        es = setup_elastic_client(args.hostname, apikey, insecure)
        post_data_to_elastic(data, index, es)

if __name__ == "__main__":
    main()
