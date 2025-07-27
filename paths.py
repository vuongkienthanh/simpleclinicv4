from pathlib import Path
import os

#######
SRC_DIR = Path(__file__).resolve().parent
STATIC_DIR = SRC_DIR / "static"
DEFAULT_CFG_PATH = STATIC_DIR / "default_config.toml"
BITMAPS_DIR = STATIC_DIR / "bitmaps"
plus_bm = BITMAPS_DIR / "plus.png"
minus_bm = BITMAPS_DIR / "minus.png"
weight_bm = BITMAPS_DIR / "weight.png"
update_druglist_bm = BITMAPS_DIR / "update_druglist.png"

#######
APP_DIR = Path.home() / ".simpleclinic"
if not APP_DIR.exists():
    os.mkdir(APP_DIR)
DB_PATH = APP_DIR / "simpleclinic.db"
CFG_PATH = APP_DIR / "config.toml"


# # sample dir
# SAMPLE_DIR = os.path.join(SRC_DIR, "sample")
