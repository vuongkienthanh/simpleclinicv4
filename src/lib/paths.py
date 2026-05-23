from pathlib import Path
import os

#######
APP_DIR = Path.home() / ".simpleclinic"
if not APP_DIR.exists():
    os.mkdir(APP_DIR)
SRC = Path(__file__).resolve().parent.parent
ASSETS = SRC.parent / "assets"

#######
PYPROJECT = SRC.parent / "pyproject.toml"

#######
BITMAPS = ASSETS / "bitmaps"

# UPDATE_BM = BITMAPS / "update.png"
# REMOVE_BM = BITMAPS / "remove.png"
# OK_BM = BITMAPS / "ok.png"
# CANCEL_BM = BITMAPS / "cancel.png"
PLUS_BM = BITMAPS / "plus.png"
MINUS_BM = BITMAPS / "minus.png"
WEIGHT_BM = BITMAPS / "weight.png"
REFRESH_BM = BITMAPS / "refresh.png"
MEDICINE_BM = BITMAPS / "medicine.png"
SERVICE_BM = BITMAPS / "service.png"

#######
ICONS = ASSETS / "icons"
LOGO = ICONS / "logo.png"

#######
SCHEMA_SQL = ASSETS / "schema.sql"
START_APP_SQL = ASSETS / "start_app.sql"
CLOSE_APP_SQL = ASSETS / "close_app.sql"

######
DEFAULT_CFG = ASSETS / "default_config.toml"
CFG = APP_DIR / "config.toml"

######
DB = APP_DIR / "simpleclinic.db"

######
DEFAULT_PRESCRIPTION_TEMPLATE = ASSETS / "default_donthuoc_template.docx"
PRESCRIPTION_TEMPLATE = APP_DIR / "donthuoc_template.docx"
PRESCRIPTION_OUTPUT = APP_DIR / "donthuoc.docx"


# # sample dir
# SAMPLE_DIR = os.path.join(SRC_DIR, "sample")
