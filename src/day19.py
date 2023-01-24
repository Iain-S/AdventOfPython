import re
import functools
from multiprocessing import Pool

# counter = 0
class HashableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hashed = hash(tuple(x for x in self.values()))

    def __hash__(self):
        return self.hashed


def get_blueprint(line):
    matches = [int(x) for x in re.findall(r"\d+", line)]
    assert len(matches) == 7
    return HashableDict(
        {
            "ore_cost": (matches[1],),
            "clay_cost": (matches[2],),
            "obsidian_cost": (matches[3], matches[4]),
            "geode_cost": (matches[5], matches[6]),
        }
    )


@functools.cache
def calc_most_geodes(blueprint, minutes, ore, clay, obs, ore_r, clay_r, obs_r):
    # global counter
    minutes -= 1

    if minutes == 0:
        return 0

    new_ore = ore + ore_r
    new_clay = clay + clay_r
    new_obs = obs + obs_r
    geodes = []

    x = False
    # Build an ore robot
    (ore_cost,) = blueprint["ore_cost"]
    if ore_cost <= ore:
        geodes.append(
            calc_most_geodes(
                blueprint,
                minutes,
                new_ore - ore_cost,
                new_clay,
                new_obs,
                ore_r + 1,
                clay_r,
                obs_r,
            )
        )
    else:
        if ore_r:
            x = True

    # Build a clay robot
    (ore_cost,) = blueprint["clay_cost"]
    if ore_cost <= ore:
        geodes.append(
            calc_most_geodes(
                blueprint,
                minutes,
                new_ore - ore_cost,
                new_clay,
                new_obs,
                ore_r,
                clay_r + 1,
                obs_r,
            )
        )
    else:
        if ore_r:
            x = True

    # Build an obsidian robot
    ore_cost, clay_cost = blueprint["obsidian_cost"]
    if ore_cost <= ore and clay_cost <= clay:
        geodes.append(
            calc_most_geodes(
                blueprint,
                minutes,
                new_ore - ore_cost,
                new_clay - clay_cost,
                new_obs,
                ore_r,
                clay_r,
                obs_r + 1,
            )
        )
    else:
        if ore_r and clay_r:
            x = True

    # Build a geode robot
    ore_cost, obs_cost = blueprint["geode_cost"]
    if ore_cost <= ore and obs_cost <= obs:
        geodes.append(
            minutes
            + calc_most_geodes(
                blueprint,
                minutes,
                new_ore - ore_cost,
                new_clay,
                new_obs - obs_cost,
                ore_r,
                clay_r,
                obs_r,
            )
        )
    else:
        if ore_r and obs_r:
            x = True

    if x:
        # counter += 1
        # We couldn't afford at least one kind of robot
        geodes.append(
            calc_most_geodes(
                blueprint, minutes, new_ore, new_clay, new_obs, ore_r, clay_r, obs_r
            )
        )

    return max(geodes)


def run_one(blueprint, mins=14):
    # print(blueprint, mins)
    return calc_most_geodes(blueprint, mins, 0, 0, 0, 1, 0, 0)


def one(lines):
    blueprints = [get_blueprint(line) for line in lines]
    with Pool() as pool:
        most_geodes = pool.map(run_one, blueprints)
    quality_levels = [(i + 1) * q for i, q in enumerate(most_geodes)]
    # print(f"{counter=}")
    return sum(quality_levels)


def run_two(lines, num):
    blueprints = [get_blueprint(line) for line in lines[0:num]]
    with Pool() as pool:
        most_geodes = pool.starmap(run_one, zip(blueprints, [32] * len(blueprints)))

    def mult(a, b):
        return a * b

    return functools.reduce(mult, most_geodes, 1)


def two(lines):
    return run_two(lines, 3)

def main():
    with open("../inputs/day19.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
