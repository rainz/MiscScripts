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
    res = md5.hexdigest()
    return res


def is_trash_dir(dname):
    return dname.find("$RECYCLE") >= 0


def main():
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
        if base_dir[-1] == os.sep:
            base_dir = base_dir[0:-1]
    else:
        base_dir = os.getcwd()
    print ("Base dir:", base_dir, file=sys.stderr)

    MIN_SIZE = 1024*1024
    visit_hidden_dir = False
    visit_hidden_file = False
    visit_trash = False

    file_count = 0

    size_hash = {}
    curr_level = [base_dir]
    while len(curr_level) > 0:
        next_level = []
        files = []
        # Get a list of files and dir
        for d in curr_level:
            try:
                children = os.listdir(d)
                #print("======= {} =======".format(d))
                for c in children:
                    is_hidden = c.startswith(".")
                    p = os.path.join(d, c)
                    if os.path.isdir(p):
                        if not visit_hidden_dir and is_hidden:
                            continue
                        if not visit_trash and is_trash_dir(c):
                            continue
                        next_level.append(p)
                    else:
                        if visit_hidden_file or not is_hidden:
                            files.append(p)
            except PermissionError:
                continue

        for f in files:
            file_count += 1
            if file_count % 1000 == 0:
                print("{} files found".format(file_count), file=sys.stderr)
            file_size = os.stat(f).st_size
            if file_size < MIN_SIZE:
                continue
            #print("File: ", f, file_size)
            # Group files of the same size together
            file_set = size_hash.get(file_size)
            if file_set is None:
                file_set = set()
                size_hash[file_size] = file_set
            file_set.add(f)

        curr_level = next_level
        continue

    print("Found {} files. Now looking for duplicates...".format(file_count), file=sys.stderr)

    for size_key, file_set in size_hash.items():
        #if size_key <= MIN_SIZE:
        #    continue
        md5sum_hash = {}
        if len(file_set) < 2:
            continue # only 1 file of this size, so there's no dup and don't compute md5
        for full_path in file_set:
            try:
                md5 = md5_file(full_path)
            except EnvironmentError:
                print("Unable to open {}, skipping".format(full_path))
                continue
            same_set = md5sum_hash.get(md5)
            if same_set is None:
                same_set = set()
                md5sum_hash[md5] = same_set
            same_set.add(full_path)
        for md5_key, same_set in md5sum_hash.items():
            if len(same_set) <= 1:
                continue
            print("Dup files: {")
            for f in same_set:
                print(f)
            print("}")

    print("Done with {} files".format(file_count), file=sys.stderr)


if __name__ == "__main__":    
    main()
