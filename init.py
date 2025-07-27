from paths import CFG_PATH, DB_PATH, APP_DIR, DEFAULT_CFG_PATH
from database.connection import create_connection, close_connection, init_database
import os
import shutil
import datetime as dt

if (
    input(
        "Initialize database? This will backup old database and create a new one.[y/n]"
    )
    == "y"
):
    if DB_PATH.exists():
        shutil.copyfile(DB_PATH, APP_DIR / dt.datetime.now().isoformat() / ".bak")
        shutil.copyfile(DEFAULT_CFG_PATH, CFG_PATH)
        os.remove(DB_PATH)
    con = create_connection(DB_PATH)
    init_database(con)
    close_connection(con)
