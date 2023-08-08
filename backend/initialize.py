import multiprocessing
import time
from database.db_init import *
from certaboHelper.initCertabo import InitializeCertabo
from certaboHelper.certabo import Certabo

# Main calibration of the Certabo board
def calibration():
    InitializeCertabo()
    calibrate = True
    new_setup = True    
    Certabo(calibrate, new_setup)
    time.sleep(7)
    print("Certabo calibration finished")

def main():
    # Create table in database if it doesn't exist
    create_table(table_players)

    inp = input("Place pieces to initial positions, and press enter...")
    if inp == "":
        # Multiprocessing added for Certabo board calibration
        # Serialreader only reads one port at a time, so we need to run it in a separate process.
        process = multiprocessing.Process(target=calibration)
        process.start()

    # Promotion pieces are added to the board, and the calibration process starts again.
    process.join()
    inp = input("Add pieces for promotion on the board, and press enter...")
    
    if inp == "":
        print("Calibrating new pieces...")
        calibrate = True
        new_setup = False
        Certabo(calibrate, new_setup)
        # Sleep needed for calibration to finish
        time.sleep(7)
        print("Success! New pieces added")


if __name__ == "__main__":
    main()