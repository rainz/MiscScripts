import glob
import os
import shutil

import reverse_geocode

from gmplot import gmplot

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

def get_if_exist(data, key):
    if key in data:
        return data[key]
    return None
def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)


def get_geodata(filename):
    image = Image.open(filename)
    image.verify()
    exif_data = image._getexif()
    if not exif_data:
        raise ValueError("No EXIF found")
    #print(exif_data)
    
    gps_key = None
    for idx, tag in TAGS.items():
        #print(idx, tag)
        if tag == "GPSInfo":
            gps_key = idx # should be 34853
            break
    
    gps_data = exif_data[gps_key]
    #print(gps_data)
    geotagging = {}
    for idx, tag in GPSTAGS.items():
        #print(idx, tag)
        if idx in gps_data:
            geotagging[tag] = gps_data[idx]

    #print(geotagging)
    # Example
    # {
    #     'GPSVersionID': b'\x02\x02\x00\x00',
    #     'GPSLatitudeRef': 'N',
    #     'GPSLatitude': ((40, 1), (46, 1), (20268859, 1000000)),
    #     'GPSLongitudeRef': 'W',
    #     'GPSLongitude': ((73, 1), (35, 1), (43487548, 1000000)),
    #     'GPSAltitudeRef': b'\x00',
    #     'GPSAltitude': (3746, 100),
    #     'GPSTimeStamp': ((19, 1), (52, 1), (54, 1)),
    #     'GPSProcessingMethod': 'GPS',
    #     'GPSDateStamp': '2018:05:05'
    # }
    return geotagging


def main():
    #src_dir = "/mnt/c/temp/BackupHuaweiMate9/Camera"
    src_dir = "/mnt/c/temp/Test"
    files = glob.glob(src_dir +"/*")
    overwrite = False
    debug_print = False
    # dst_dir = os.getcwd()
    dst_dir = src_dir

    for f in files:
        if os.path.isdir(f):
            print("Skipping dir " + f)
            continue
        bname = os.path.basename(f)
        parts = bname.split("_")
        if len(parts) < 3:
            print("Skipping file " + bname)
            continue
        yyyymmdd = parts[1]
        if len(yyyymmdd) != 8:
            print("Can't parse date in file name, skipping: " + bname)
            continue
        year = yyyymmdd[0:4]
        month = yyyymmdd[4:6]
        day = yyyymmdd[6:]
        dst_dir_path = os.path.join(dst_dir, year, month)
        dst_file_path = os.path.join(dst_dir_path, bname)
        if not overwrite and os.path.exists(dst_file_path):
            print(dst_file_path + " exists, not overwriting")
            continue
        if debug_print:
            print("src: "+f)
            print("dst: "+dst_file_path)
        os.makedirs(dst_dir_path, exist_ok = True)
        shutil.move(f, dst_file_path)

if __name__ == "__main__":    
    #main()
    
    #geo = get_geodata('/mnt/c/temp/TestCopy/IMG_20180505_155254.jpg')
    geo = get_geodata('/mnt/c/temp/TestCopy/IMG_20191027_181134_1.jpg')
    coord = get_coordinates(geo)
    print(reverse_geocode.search([coord]))
    
    #gmap = gmplot.GoogleMapPlotter(coord[0], coord[1], 13)
    #gmap.apikey = "xxxx"
    #gmap.draw("my_map.html")