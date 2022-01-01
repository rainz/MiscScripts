import sys
import os


def collect_stats():
    root = "."
    if len(sys.argv) > 1:
        root = sys.argv[1]

    for basedir, subdirs, files in os.walk(root):
        for name in files:
            fullpath = os.path.join(basedir, name)
            stat = os.stat(fullpath)
            print("{},{}".format(fullpath, stat.st_size))
    #for name in subdirs:
    #    print(os.path.join(basedir, name))


def find_dups():
    if len(sys.argv) <= 1:
        print("Please specify a file name")
        sys.exit(-1)

    histo = {}

    ignore_substrs = ["Thumbs.db", "IphoneBackup20170618", ".AAE"]
    f = open(sys.argv[1], "rt")
    for l in f:
        ignore = False
        for s in ignore_substrs:
            if l.find(s) >= 0:
                ignore = True
                break
        if ignore:
            continue
        components = l.strip().split(",")
        comp_len = len(components)
        if comp_len < 2:
            continue
        file_size = int(components[comp_len-1])
        if file_size < 2048:
            continue
        file_name = "".join(components[:comp_len-1])
        #print("{}: {}".format(file_name, file_size))
        if file_size <= 0:
            continue
        same_size = histo.get(file_size)
        if same_size is None:
            same_size = []
            histo[file_size] = same_size
        same_size.append(file_name)

    for key, value in histo.iteritems():
        if len(value) <= 1:
            continue
        print("{}: {}".format(key, ",".join(value)))


if __name__== "__main__":
  #collect_stats()
  find_dups()
