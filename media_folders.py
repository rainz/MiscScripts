import sys
import os
import glob

base_folder = "/path/to/media/dir"

img_listing = glob.glob(os.path.join(base_folder, "IMG*"))
vid_listing = glob.glob(os.path.join(base_folder, "VID*"))
listing = img_listing + vid_listing
date_set = set()
month_set = set()
for f_path in listing:
    f_name = os.path.basename(f_path)
    parts = f_name.split('_')
    yyyymmdd = parts[1]
    yyyy_mm = yyyymmdd[:4] + "_" + yyyymmdd[4:6]
    date_set.add(yyyymmdd)
    month_set.add(yyyy_mm)
    month_path = os.path.join(base_folder, yyyy_mm)
    dest_f_path = os.path.join(month_path, f_name)
    os.makedirs(month_path, exist_ok=True)
    mv_cmd = "mv " + f_path + " " + dest_f_path
    print(mv_cmd)
    os.system(mv_cmd)

# print("IMG ", len(img_listing), ", VID " , len(vid_listing), ", total ", len(listing))
# print("dates", len(date_set))
# print(date_set)
# print("months", len(month_set))
# print(month_set)
