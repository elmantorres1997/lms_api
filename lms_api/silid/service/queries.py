#!/usr/bin/env python3

import yaml
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def get_query(query):
    with open(BASE_DIR + '/queries.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        try:
            return data[query]
        except KeyError:
            print(f"No query named {query}")
            return None