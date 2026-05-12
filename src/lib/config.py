from lib.paths import CFG_PATH
import tomllib


def get_config():
    with open(CFG_PATH, "rb") as f:
        return tomllib.load(f)
