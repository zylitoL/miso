"""NREL Query utilities

Utilities for constructing queries to the NREL API, described here:
    https://developer.nrel.gov/docs/transportation/evi-pro-lite-v1/

The query_nrel function queries the NREL API, given a dictionary that mimics the key-value pairs for the
"daily-load-profile" gateway and returns the JSON object as a dictionary.

To facilitate querying, the Query dataclass can be used. For modeling purposes, the datatypes of the Query dataclass
are internal numeric representations for some attributes. Given a Query object, the encode_args method returns a
dictionary that can be used for query_nrel.

Globals:
    - APIKEY: The APIKEY for the NREL API. Reads "key.txt", otherwise defaults to "DEMO_KEY"
    - DOMAIN: Dictionary that represents the acceptable inputs to the NREL API with numerical interpretations
    - ENCODED_DOMAIN: Dictionary that represents numerical interpretations as their NREL API equivalents
"""


import json
from dataclasses import dataclass, fields

import requests

APIKEY = ""
try:
    with open('../../key.txt') as fin:
        APIKEY = fin.read().strip()
except FileNotFoundError:
    APIKEY = 'DEMO_KEY'

"""Dictionary mapping arguments for the NREL API to internal values acceptable by the Query class."""
DOMAIN = {
    'temp_c': [-20, -10, 0, 10, 20, 30, 40],
    'fleet_size': [1000, 10000, 30000],
    'mean_dvmt': [25, 35, 45],
    'pev_dist': ['BEV', 'PHEV', 'EQUAL'],
    'class_dist': [20, 50, 80],
    'pref_dist': [60, 80, 100],
    'home_access_dist': [50, 75, 100],
    'home_power_dist': [20, 50, 80],
    'work_power_dist': [20, 50, 80],
    'res_charging': ['min_delay', 'max_delay', 'timed_charging', 'load_leveling'],
    'work_charging': ['min_delay', 'max_delay', 'load_leveling']
}

"""Dictionary for arguments which are encoded differently in the NREL API compared to the Query class."""
ENCODED_DOMAIN = {
    'class_dist': {20: 'SUV', 50: 'Equal', 80: 'Sedan'},
    'pref_dist': {60: 'Home60', 80: 'Home80', 100: 'Home100'},
    'home_access_dist': {50: 'HA50', 75: 'HA75', 100: 'HA100'},
    'home_power_dist': {20: 'MostL2', 50: 'Equal', 80: 'MostL1'},
    'work_power_dist': {20: 'MostL2', 50: 'Equal', 80: 'MostL1'}
}


@dataclass
class Query:
    """Internal representation for NREL queries.

    Wrapper around the NREL query with numerical datatypes for attributes.
    """
    temp_c: float
    fleet_size: int
    mean_dvmt: float
    pev_dist: str
    class_dist: float
    pref_dist: float
    home_access_dist: float
    home_power_dist: float
    work_power_dist: float
    res_charging: str
    work_charging: str

    def neighbors(self) -> dict:
        """Returns a mapping of the nearest canonical values in the NREL API for all attributes.

        For a given valid query, returns a dictionary mapping, for each query attribute, a tuple containing the exact
        value, if the value of the attribute is one of the discrete permitted values in the NREL API, or the two closest
        exact values, if it does not.

        :return dict: Dictionary mapping attribute to tuple of its nearest permissible values
        """
        ret = dict()
        for field in fields(Query):
            field_name = field.name
            val = getattr(self, field_name)
            if field.type == str:
                ret[field_name] = (val,)
                continue

            domain = DOMAIN[field_name]
            for i, x in enumerate(domain):
                if val == x:
                    ret[field_name] = (val,)
                    break

                if val < x:  # TODO: properly guard against values outside domain
                    ret[field_name] = (domain[i - 1], x)
                    break

        return ret

    def encode_args(self) -> dict:  # TODO: ensure that args lay *in* domain
        """Encodes query object as a dictionary.

        Encodes arguments of the query object into a dictionary, with proper encoding for the NREL domain, to be
        used with the query_nrel function

        :return dict: Encoded dictionary representation of the query
        """
        ret = dict()
        for field in fields(Query):
            field_name = field.name
            val = getattr(self, field_name)

            if field_name not in ENCODED_DOMAIN:
                ret[field_name] = val
                continue

            ret[field_name] = ENCODED_DOMAIN[field_name][val]

        return ret


def query_nrel(d: dict):
    """Queries NREL API using dictionary mapping.

    Given an encoded representation mapping attributes in the NREL API to their values, constructs the URL using the
    API key (or default if one is not found), and returns the request result JSON as a dictionary

    :param d: Dictionary adhering to NREL API
    :return:
    """
    base_url = f"https://developer.nrel.gov/api/evi-pro-lite/v1/daily-load-profile?api_key={APIKEY}&"
    url = f'{base_url}{"&".join(f"{k}={v}" for k, v in d.items())}'
    record_str = requests.get(url).text
    record_str = record_str.replace("'", "\"")
    raw_json = json.loads(record_str)
    return raw_json


if __name__ == "__main__":
    args = [v[0] for v in DOMAIN.values()]
    q = Query(*args)
    print(query_nrel(q.encode_args()))
