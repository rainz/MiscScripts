import sys
import os
import hashlib

def md5_file(fname, block_size=2**20):
    md5 = hashlib.md5()
    with open(fname, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

def main():
    MIN_SIZE = 0
    size_hash = {}

    file_count = 0;

    for root, dirs, files in os.walk("."):
        path = root.split(os.sep)
        #print root
        #for d in dirs:
        #    print "d", d
        for f in files:
            file_count += 1
            if file_count % 1000 == 0:
                print >> sys.stderr, "{} files found".format(file_count)
            full_path = os.path.join(root, f)
            file_size = os.stat(full_path).st_size
            #print "f", f, file_size
            file_set = size_hash.get(file_size)
            if file_set is None:
                file_set = set()
                size_hash[file_size] = file_set
            file_set.add(full_path)

    print >> sys.stderr, "Found {} files. Now looking for duplicates...".format(file_count)

    for size_key, file_set in size_hash.iteritems():
        if size_key <= MIN_SIZE:
            continue
        md5sum_hash = {}
        for full_path in file_set:
            try:
                md5 = md5_file(full_path)
            except EnvironmentError:
                print >> sys.stderr, "Unable to open {}, skipping".format(full_path)
                continue
            same_set = md5sum_hash.get(md5)
            if same_set is None:
                same_set = set()
                md5sum_hash[md5] = same_set
            same_set.add(full_path)
        for md5_key, same_set in md5sum_hash.iteritems():
            if len(same_set) <= 1:
                continue
            print "Dup files: {"
            for f in same_set:
                print f
            print "}"

    print >> sys.stderr, "Done".format(file_count)

main()
