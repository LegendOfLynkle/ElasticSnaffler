#!/usr/bin/env python3
import json
import argparse
from xmlrpc.client import Boolean
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# Disable insecure requests warning (it doesn't matter)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 

def load_data(filename:str):
    with open(filename, "r") as snaffout:
        data = json.load(snaffout)
    return data

def post_data_to_elastic(data, index:str, apikey:str):
    triage_levels = ["Green", "Yellow", "Red", "Black"]
    snaffle = {}
    snaffle["entries"] = []
    ii = 0

    for entry in data["entries"]:
        if(len(entry["eventProperties"].keys()) != 0):
            for triage_level in triage_levels:
                if(list(entry["eventProperties"].keys())[0] == triage_level):
                    if(entry["eventProperties"][triage_level]["Type"] == "FileResult"):
                        # send the data
                        r = requests.put(f"https://10.48.100.119:9200/{index}/_doc/{ii}", json=entry["eventProperties"][triage_level], headers={"Authorization": f"ApiKey {apikey}"}, verify=False)
                        if(r.status_code != 201):
                            print(r.status_code, r.reason)
                        # increment the counter 
                        ii = ii + 1

def main():
    parser = argparse.ArgumentParser(description="Send Snaffler Output to ElasticSearch for analysis.", epilog="Happy Snaffling")
    parser.add_argument("-f", "--file", type=str, help="The path to the JSON file to process.", required=True)
    parser.add_argument("-i", "--index", type=str, help="The name of the index to store results in.")
    parser.add_argument("-k", "--apikey", type=str, help="The API key used to authentiate to ElasticSearch.")
    parser.add_argument("-r", "--replace", type=str, help="Optional argument to delete existing items in the index selected before adding new items.")
    parser.add_argument("-a", "--append", type=str, help="Optional argument to append new items to the selected index.")
    parser.add_argument("--insecure", type=Boolean, help="Toggle for allowing sending over HTTPS with verification turned off so self signed or invalid ceritficates can be used.")
    args = parser.parse_args()

    data = load_data(args.file)

    if args.index is not None and args.apikey is not None:
        post_data_to_elastic(data, args.index, args.apikey)
    else:
        if args.index is None:
            # TODO add functionality here using the ES library to check for existing indicies
            index = input("Please enter a name for the index to use: ")
        if args.apikey is None:
            apikey = input("Please enter an API Key: ")
        post_data_to_elastic(data, index, apikey)

if __name__ == "__main__":
    main()
