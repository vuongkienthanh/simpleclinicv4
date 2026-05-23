from lib.paths import (
    DB,
    DEFAULT_S1A_TEMPLATE,
    PRESCRIPTION_TEMPLATE,
    S1A_TEMPLATE,
    SCHEMA_SQL,
    CFG,
    DEFAULT_CFG,
    DEFAULT_PRESCRIPTION_TEMPLATE,
)
from lib.db import connect
import shutil


def main():
    print(f"checking database at {DB} ...")
    if DB.exists():
        print("A database file existed.")
    else:
        print("A database file doesn't exist.")
        print("Proceed to create a new database file.")
        conn = connect(DB)
        with open(SCHEMA_SQL) as f:
            conn.executescript(f.read())
        conn.close()
        print(f"New database file created at {DB}.")

    print()
    print(f"checking config file at {CFG} ...")
    if CFG.exists():
        print("A config file existed.")
    else:
        print("A config file doesn't exist.")
        print("Proceed to create a new config file.")
        shutil.copyfile(DEFAULT_CFG, CFG)
        print(f"New config file created at {CFG}.")

    print()
    print(f"checking prescription template at {PRESCRIPTION_TEMPLATE} ...")
    if PRESCRIPTION_TEMPLATE.exists():
        print("A prescription template existed.")
    else:
        print("A prescription template doesn't exist.")
        print("Proceed to create a new prescription template.")
        shutil.copyfile(DEFAULT_PRESCRIPTION_TEMPLATE, PRESCRIPTION_TEMPLATE)
        print(f"New prescription template created at {PRESCRIPTION_TEMPLATE}.")

    print()
    print(f"checking s1a template at {S1A_TEMPLATE} ...")
    if S1A_TEMPLATE.exists():
        print("A s1a template existed.")
    else:
        print("A s1a template doesn't exist.")
        print("Proceed to create a new s1a template.")
        shutil.copyfile(DEFAULT_S1A_TEMPLATE, S1A_TEMPLATE)
        print(f"New s1a template created at {S1A_TEMPLATE}.")
