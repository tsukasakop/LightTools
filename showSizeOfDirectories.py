from email.policy import default
import optparse
import shutil
from tqdm import tqdm
import os
import sys

dp = {}
def get_folder_size(folder_path):
    total_size = 0
    if folder_path in dp:
        return dp[folder_path]
    for path, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(path, file)
            total_size += os.path.getsize(file_path)
    dp[folder_path]=total_size
    return total_size
def print_folder_sizes(root_folder, recursive):
    folder_sizes = []
    # for path, dirs, files in os.walk(root_folder):
    for path, dirs, files in tqdm(os.walk(root_folder)):
        for dir in dirs:
            dir_path = os.path.join(path, dir)
            if not recursive and path != root_folder:
                continue
            
            terminal_size = shutil.get_terminal_size()
            nColumns = terminal_size.columns
            dirStrHeight=(len(str(dir))-1)//nColumns + 1
            resetHeight = max(dirStrHeight, 0) + 1
            tqdm.write(dir)
            tqdm.write(f"\033[{resetHeight}A")
            tqdm.write(" "*nColumns)
            tqdm.write(f"\033[2A")
            size = get_folder_size(dir_path)
            folder_sizes.append((dir_path if recursive else dir, size))
    
    folder_sizes.sort(key=lambda x: x[1], reverse=True)
    
    n_pad = max([len(d) for d,_ in folder_sizes])
    for folder, size in folder_sizes:
        unit = ["B", "KB", "MB", "GB", "TB"]
        for i,unit in enumerate(unit):
            s = size/2**(10*i)
            if s >= 2**10:
                continue
            _ = f"{s:.1f}"
            print(f"{folder:{n_pad}}:{_:>6} {unit}")
            break


# 対象のフォルダパスを指定
parser = optparse.OptionParser()
parser.add_option("-r", "--recursive", dest="recursive",
                  help="select show directory recursive or not", default=False)
(options, args) = parser.parse_args()
folder_path = args[0] if len(args) == 1 else input("Root directory path?:\n")
while True:
    try:
        print_folder_sizes(folder_path, options.recursive)
        break
    except Exception as e:
        print(e)
        input("Root directory path?:\n")

