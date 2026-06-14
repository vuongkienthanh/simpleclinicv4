from lib.paths import DB, APP_DIR
import shutil
import datetime as dt


def main():
    print(f"checking database at {DB} ...")
    if DB.exists():
        print("A database file existed.")
        if input("Back up database?[y/n]") == "y":
            BK = APP_DIR / ("simpleclinic_" + dt.datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".bak")
            shutil.copyfile(DB, BK)
            print(f"Back up to {BK}")
    else:
        print("A database file doesn't exist.")
