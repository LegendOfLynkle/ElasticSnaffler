#!/usr/bin/env python3
import json
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# Disable insecure requests warning (it doesn't matter)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 

def load_data():
    with open(sys.argv[1], "r") as snaffout:
        data = json.load(snaffout)
    return data

def post_data_to_elastic(data):
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
                        r = requests.put(f"https://10.48.100.119:9200/{sys.argv[2]}/_doc/{ii}", json=entry["eventProperties"][triage_level], headers={"Authorization": f"ApiKey {sys.argv[3]}"}, verify=False)
                        if(r.status_code != 201):
                            print(r.status_code, r.reason)
                        # increment the counter 
                        ii = ii + 1

def main():
    if len(sys.argv) != 3:
        print("3 arguments are required!\n1: The path to the JSON file to process\n2: The name of the index to store results in\n3: The API key to use for authentication.")
    else:
        data = load_data()
        post_data_to_elastic(data)

if __name__ == "__main__":
    main()
