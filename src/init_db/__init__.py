from lib.paths import DB_PATH, SCHEMA_SQL, CFG_PATH, DEFAULT_CFG_PATH
from lib.db import connect
import shutil


def main():
    print(f"checking database at {DB_PATH} ...")
    if DB_PATH.exists():
        print("A database file existed.")
    else:
        print("A database file doesn't exist.")
        print("Proceed to create a new database file.")
        conn = connect(DB_PATH)
        with open(SCHEMA_SQL) as f:
            conn.executescript(f.read())
        conn.close()
        print(f"New database file created at {DB_PATH}.")

    print(f"checking config file at {CFG_PATH} ...")
    if CFG_PATH.exists():
        print("A config file existed.")
    else:
        print("A config file doesn't exist.")
        print("Proceed to create a new config file.")
        shutil.copyfile(DEFAULT_CFG_PATH, CFG_PATH)
        print(f"New config file created at {CFG_PATH}.")
