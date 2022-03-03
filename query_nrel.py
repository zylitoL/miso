from dataclasses import dataclass, fields

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
    'class_dist': [20, 50, 80],  # TODO: SUV, Equal, Sedan
    'pref_dist': [60, 80, 100],  # TODO: Home60, Home80, Home100
    'home_access_dist': [60, 80, 100],  # TODO: HA50, HA75, HA100
    'home_power_dist': [20, 50, 80],  # TODO: MostL2, Equal, MostL1
    'work_power_dist': [20, 50, 80],  # TODO: same as up
    'res_charging': ['min_delay', 'max_delay', 'timed_charging', 'load_leveling'],
    'work_charging': ['min_delay', 'max_delay', 'load_leveling']
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


if __name__ == "__main__":
    args = [23, 1004, 29, 'BEV', 23, 81, 68, 21, 21, 'load_leveling', 'load_leveling']
    q = Query(*args)
    print(q.neighbors())
