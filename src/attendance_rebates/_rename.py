import os
from pathlib import Path
import shutil
from icecream import ic

old_date = '2023_02'
new_date = '2023_05'

dir = '/home/jeff/projects/phoenix/programs/attendance_rebates/'
source = Path(dir, f'downloaded-data/{old_date}/')
dest = Path(dir, f'renamed-data/{new_date}/')

if not dest.is_dir():
    dest.mkdir()

# source_dir = Path(source)
# dest_dir = Path(dest)
# if not

file_list = [Path(source, name)
             for name in source.iterdir() if name.is_file()]

for old_file in file_list:
    new_file = Path(dest, old_file.name.replace(old_date, new_date))
    print(old_file)
    print(new_file)
    print()
#     os.rename(old_file, new_file)
    shutil.copyfile(old_file, new_file)
