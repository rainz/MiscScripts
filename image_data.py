from PIL import Image
from PIL.ExifTags import TAGS

imagename = "test_img.jpg"
image = Image.open(imagename)
exifdata = image.getexif()
# iterating over all EXIF data fields
for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    # decode bytes 
    if isinstance(data, bytes):
        data = data.decode()
    print(f"{tag:25}: {data}")
