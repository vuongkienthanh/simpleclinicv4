from lib.paths import CFG
import tomllib


def get_config():
    with open(CFG, "rb") as f:
        return tomllib.load(f)
