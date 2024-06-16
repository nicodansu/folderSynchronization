#python folderSynchronization.py -s "C:/01 Data Folder/01Source" -d "C:/01 Data Folder/01Destination" -l "C:/01 Data Folder/Mylog.log" -i 30
import os
import filecmp
import shutil
import argparse
import time
from datetime import datetime

def sync_folders(source_folder, target_folder, log_file,sync_interval):
    dcmp = filecmp.dircmp(source_folder, target_folder)
    # Copy files from the source folder to the target folder
    for name in dcmp.left_only:
        source_path = os.path.join(source_folder, name)
        target_path = os.path.join(target_folder, name)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, target_path)
        else:
            shutil.copytree(source_path, target_path)
        print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"Copying: {source_path} -> {target_path}")
        with open(log_file, "a") as f:
            print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), f"Copying: {source_path} -> {target_path}", file=f)

    # Remove files that are missing in the source folder
    for name in dcmp.right_only:
        target_path = os.path.join(target_folder, name)
        if os.path.isfile(target_path):
            os.remove(target_path)
            print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"Removing: {target_path}")
            with open(log_file, "a") as f:
                print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), f"Removing: {target_path}", file=f)
        else:
            shutil.rmtree(target_path)
            print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"Removing: {target_path}")
            with open(log_file, "a") as f:
                print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), f"Removing: {target_path}", file=f)


    # Recursively synchronize sub-folders
    for sub_dcmp in dcmp.subdirs:
        sync_folders(
            os.path.join(source_folder, sub_dcmp),
            os.path.join(target_folder, sub_dcmp),
            log_file,
            sync_interval
        )


# Create the argument parser
parser = argparse.ArgumentParser(description="Script to synchronize two folders.")
parser.add_argument("-s", "--source", type=str, help="Path to the source folder.")
parser.add_argument("-d", "--destination", type=str, help="Path to the target folder.")
parser.add_argument("-l", "--log", type=str, help="Path to the log file.")
parser.add_argument("-i", "--interval", type=int, help="sync interval in seconds")

# Parse the command-line arguments
args = parser.parse_args()

# Check for required arguments
if not args.source or not args.destination or not args.log:
    parser.print_help()
else:
    source_folder = args.source
    target_folder = args.destination
    log_file = args.log
    sync_interval = args.interval

    while True:
        # Check if the log file exists and create it if it doesn't
        if not os.path.exists(log_file):
            print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"Created log file: {log_file}")
            with open(log_file, "a") as f:
                print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), f"Created log file: {log_file}", file=f)

        # Check if the target folder exists and create it if it doesn't
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"Created target folder: {target_folder}")
            with open(log_file, "a") as f:
                print(f"", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), f"Created target folder: {target_folder}", file=f)

        sync_folders(source_folder, target_folder, log_file, sync_interval)
        time.sleep(sync_interval)
