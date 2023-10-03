import os
import shutil
import argparse
import time

def sync_folders(source_path, replica_path, log_file):
    try:
        if not os.path.exists(source_path) or not os.path.exists(replica_path):
            raise Exception("Source or replica folder does not exist")

        for root, dirs, files in os.walk(source_path):
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_path, os.path.relpath(source_file_path, source_path))

                if not os.path.exists(replica_file_path) or os.path.getmtime(source_file_path) > os.path.getmtime(replica_file_path):
                    shutil.copy2(source_file_path, replica_file_path)
                    log(log_file, f"Copied: {source_file_path} -> {replica_file_path}")
        
        for root, dirs, files in os.walk(replica_path):
            for file in files:
                replica_file_path = os.path.join(root, file)
                source_file_path = os.path.join(source_path, os.path.relpath(replica_file_path, replica_path))

                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    log(log_file, f"Deleted: {replica_file_path}")

    except Exception as e:
        log(log_file, f"Error: {str(e)}")

def log(log_file, message):
    with open(log_file, 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source_path", help="Path to source folder")
    parser.add_argument("replica_path", help="Path to replica folder")
    parser.add_argument("log_file", help="Path to log file")
    parser.add_argument("interval", type=int, help="Synchronization interval (in seconds)")

    args = parser.parse_args()

    while True:
        sync_folders(args.source_path, args.replica_path, args.log_file)
        time.sleep(args.interval)
