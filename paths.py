import os
from pathlib import Path

#######
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(SRC_DIR, "static")
DEFAULT_CONFIG_PATH = os.path.join(STATIC_DIR, "default_config.json")
BITMAPS_DIR = os.path.join(STATIC_DIR, "bitmaps")
plus_bm = os.path.join(BITMAPS_DIR, "plus.png")
minus_bm = os.path.join(BITMAPS_DIR, "minus.png")
weight_bm = os.path.join(BITMAPS_DIR, "weight.png")
update_druglist_bm = os.path.join(BITMAPS_DIR, "update_druglist.png")

#######
APP_DIR = os.path.join(Path.home(), ".simpleclinic")
if not Path(APP_DIR).exists():
    os.mkdir(APP_DIR)

DB_PATH = os.path.join(APP_DIR, "simpleclinic.db")
CFG_PATH = os.path.join(APP_DIR, "config.json")


# # sample dir
# SAMPLE_DIR = os.path.join(SRC_DIR, "sample")
