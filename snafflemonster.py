#!/usr/bin/env python3
import json
import argparse
import tqdm
import re
from kibana import Kibana
from kibana import DEFAULT_DASHBOARD
from elasticsearch.helpers import streaming_bulk
from elasticsearch import Elasticsearch

def load_data(filename:str):
    with open(filename, "r") as snaffout:
        data = json.load(snaffout)
    return data

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

def get_choice_index(es, index):
    valid = False
    valid_choice = ['a', 'r', 'i', 'q']
    # ask them how to handle it if it is in use
    count = es.cat.count(index, params={"format": "json"})[0]["count"]
    print(f"The {index} index is already in use and has {count} items stored. How would you like to proceed?")
    while not valid:
        choice = input(f"Please select one of the following options:\nA: Append data to the index\nR: Replace the data in the index. (Will delete old data first)\nI: Select a different index\nQ: Quit without doing anything.\n")
        if choice.lower() not in valid_choice:
            print(f"The option {choice} is not valid.")
        else:
            choice = choice.lower()
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
    kibana = Kibana(apikey, hostname, 5601, insecure, True)
    # Time to check the indexes to see if they already exist or not
    if args.index is not None:
        index = args.index
    else:
        index = input("Please enter a name for the index to use: ")
    # check if the index is in use
    if is_index_in_use(es, index):
        # ask them how to handle it if it is in use
        choice, index = get_choice_index(es, index)
        if choice == "r":
            es.indices.delete(index=index, ignore=[400, 404])
            post_data_to_elastic_bulk(es, data, index)
            auto_create_data_view(kibana, index, es)
            auto_create_dashboard(kibana, index)
        if choice == "a" or choice == "i":
            post_data_to_elastic_bulk(es, data, index)
            auto_create_data_view(kibana, index, es)
            auto_create_dashboard(kibana, index)
        if choice == "q":
            print("You have chose to quit, aborting")
    else:
        # The index is not in use and we can just post no worries.
        post_data_to_elastic_bulk(es, data, index)
        auto_create_data_view(kibana, index, es)
        auto_create_dashboard(kibana, index)

def post_data_to_elastic_bulk(es, data, index):
    total = get_file_result_total(data)
    print("Uploading..")
    progress = tqdm.tqdm(unit="results", total=total)
    ii = 0
    for ok, action in streaming_bulk(
        client=es, index=index, actions=gen_bulk_data(data)
    ):
        progress.update(1)
        ii += ok
    print(f"Uploaded {ii} results out of {total} succesfully.")

def gen_bulk_data(data):
    triage_levels = ["Green", "Yellow", "Red", "Black"]
    snaffle = {}
    snaffle["entries"] = []
    for entry in data["entries"]:
        if(len(entry["eventProperties"].keys()) != 0):
            for triage_level in triage_levels:
                if(list(entry["eventProperties"].keys())[0] == triage_level):
                    if(entry["eventProperties"][triage_level]["Type"] == "FileResult"):
                        yield entry["eventProperties"][triage_level]

def get_file_result_total(data):
    total = 0
    triage_levels = ["Green", "Yellow", "Red", "Black"]
    for entry in data["entries"]:
        if(len(entry["eventProperties"].keys()) != 0):
            for triage_level in triage_levels:
                if(list(entry["eventProperties"].keys())[0] == triage_level):
                    if(entry["eventProperties"][triage_level]["Type"] == "FileResult"):
                        total += 1
    return total

def auto_create_data_view(kibana, index, es):
    # TODO: check if an appropriate data view already exists or not.
    exists, matched_pattern = check_if_data_view_exists(kibana, index)
    if exists:
        print(f"Valid data-view ({matched_pattern}) for {index} index already exists.")
        #For now do nothing but TODO we will come back here and let the user choose it they want to use it/one of them or create a new one.
    else:
        print("No data-view for your index exists. Would you like to create one?")
        choice = get_choice_basic("Y: Yes\nN: No", ["y", "n"])
        if choice == "y":
            print("Would you like to use a default pattern or specify one?")
            choice = get_choice_basic("D: Default\nC: Custom", ["d", "c"])
            if choice == "d":
                kibana.create_data_view(f"{index}*")
            if choice == "c":
                valid = False
                # assume no matches until we find out otherwise.
                no_matches = True
                while not valid:
                    pattern = input("Please enter the pattern you want for your data-view:\n")
                    indices = es.indices.get_alias("*")
                    # we loop here incase the pattern they provided here uses commas to specify multiple things.
                    for sub_pattern in pattern.split(","):
                        # check each of the indices.
                        for index in indices:
                            result = re.match(sub_pattern, index)
                            if result:
                                # we can stop looping since the pattern matches an index.
                                valid = True
                                no_matches = False
                    if no_matches:
                        print("Provided pattern did not match any indices!")
                # Just going to keep looping until we get a valid one for now.
                kibana.create_data_view(pattern)

def auto_create_dashboard(kibana, index):
    data_views = kibana.get_saved_object("index-pattern")
    # Here we are retrieving the data_view_id that we are going to use within the dashboard.
    data_view_id = ""
    for data_view in data_views:
        # This will need to change. Maybe we could just let the user pick from a list of all data-views currently available. If we do that then we will want to add in a check for if the index even has the right mapping for our Dashboard. 
        if data_view["attributes"]["title"] == f"{index}*":
            data_view_id = data_view["id"]
    # We will use the default dashboard
    default_dashboard = DEFAULT_DASHBOARD
    # Setup the title and description
    default_dashboard["title"] = default_dashboard["title"].replace("INDEX_NAME", index)
    default_dashboard["description"] = default_dashboard["description"].replace("INDEX_NAME", index)
    # Change the visualisation references to refer to the desired data view
    default_dashboard["panelsJSON"] = default_dashboard["panelsJSON"].replace("DATA-VIEW-ID", data_view_id)
    kibana.create_dashboard(default_dashboard)

def get_choice_basic(prompt, valid_choice):
    valid = False
    while not valid:
        choice = input(f"Please choose an option:\n{prompt}")
        if choice.lower() not in valid_choice:
            print(f"The option {choice} is not valid.")
        else:
            choice = choice.lower()
            valid = True
    return choice

def check_if_data_view_exists(kibana, index):
    """
    check_if_data_view_exists: Used to check if a data_view already exists for our desired index
    @imports: 
    - kibana: The kibana API helper object
    - index: The index that we want to check against
    @returns:
    - exists: Boolean indicating whether a data view that captures the index exists or not.
    - matched_pattern: The pattern that captures the index, if one exists. Will return None if one does not exist.
    """
    # Assume that it does not already exist
    exists = False
    #TODO: add check for the edge case there are multiple valid patterns.
    matched_pattern = None
    # Get all data views
    data_views = kibana.get_saved_object("index-pattern")
    for data_view in data_views:
        # You can specify multiple patterns seperated by commas
        patterns = data_view["attributes"]["title"].split(",")
        # cycle through all patterns to see if we have a match.
        for pattern in patterns:
            result = re.match(pattern, index)
            if result:
                # Record the matching pattern then return the result so the user can decide what to do.
                exists = True
                matched_pattern = pattern
    return exists, matched_pattern

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
