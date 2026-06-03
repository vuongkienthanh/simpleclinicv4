from lib.paths import DB, APP_DIR
import shutil
import datetime as dt


def main():
    print(f"checking database at {DB} ...")
    if DB.exists():
        print("A database file existed.")
        if input("Back up database?[y/n]") == "y":
            bk = APP_DIR / ("simpleclinic_" + dt.datetime.now().isoformat() + ".bak")
            shutil.copyfile(DB, bk)
            print(f"Back up to {bk}")
    else:
        print("A database file doesn't exist.")
