import json
from dataclasses import dataclass, fields

import requests

APIKEY = ""
try:
    with open('key.txt') as fin:
        APIKEY = fin.read().strip()
except FileNotFoundError:
    APIKEY = 'DEMO_KEY'

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

ENCODED_DOMAIN = {
    'class_dist': {20: 'SUV', 50: 'Equal', 80: 'Sedan'},
    'pref_dist': {60: 'Home60', 80: 'Home80', 100: 'Home100'},
    'home_access_dist': {50: 'HA50', 75: 'HA75', 100: 'HA100'},
    'home_power_dist': {20: 'MostL2', 50: 'Equal', 80: 'MostL1'},
    'work_power_dist': {20: 'MostL2', 50: 'Equal', 80: 'MostL1'}
}


@dataclass
class Query:
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
    base_url = f"https://developer.nrel.gov/api/evi-pro-lite/v1/daily-load-profile?api_key={APIKEY}&"
    url = f'{base_url}{"&".join(f"{k}={v}" for k, v in d.items())}'
    record_str = requests.get(url).text
    record_str = record_str.replace("'", "\"")
    raw_json = json.loads(record_str)
    print(raw_json)


if __name__ == "__main__":
    args = [v[0] for v in DOMAIN.values()]
    q = Query(*args)
    query_nrel(q.encode_args())
