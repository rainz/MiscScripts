import sys
import os
from mutagen.mp3 import MP3

if len(sys.argv) < 2:
    print("Please specify at least one file name!")
    sys.exit(-1)

for i in range(1, len(sys.argv)):
    fname = sys.argv[i];
    audio = MP3(fname)
    if not audio:
        print("Unable to load {}, skipping".format(fname))
        continue
    title = ",".join(audio["TIT2"].text).encode("utf8")
    # Only works in the current dir!
    os.rename(fname, "{}.mp3".format(title))
