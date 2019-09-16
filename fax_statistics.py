#!/usr/bin/env python3

# Todo: Allow filtering by time range

import json
import re

FILE_PATH = "./"
FILE_NAME = "faxrelay.log"
# RX denied should be received - sent_permitted
QUERIES = {
    "received": "Received message",
    "sent_permitted": "Sending message",
    "server_starts": "server enabled"
    }

def log_parser(event, json_output=False):
    results = {}
    with open(FILE_PATH + FILE_NAME) as file:
        logs = file.readlines()

    for log in logs:
        if re.search(QUERIES[event], log):
            date = log.split(" ")[0]
            # Create key/value pair if it doesn't already exist
            results.setdefault(date, 0)
            results[date] += 1
    if json_output:
        results = {event: results}
        return json.dumps(results, indent=4, sort_keys=True)
    else:
        return results

def parse_all(json_output=False):
    """Collects all event types into a single output"""
    results = {}
    for query in QUERIES:
        results[query] = log_parser(query)
    if json_output:
        return json.dumps(results, indent=4, sort_keys=True)
    else:
        return results

if __name__ == "__main__":
    #print(log_parser("server_starts", json_output=True))
    #print(log_parser("received", json_output=True))
    #print(log_parser("sent_permitted", json_output=True))
    print(parse_all(json_output=True))
