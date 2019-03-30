import os
import PIL.Image as image
import PIL.ExifTags
path_dir = './test'
file_list = os.listdir(path_dir)


for text in file_list:
    print(text, type(text))

i = image.open('./test/ee.jpg')
info = i._getexif()
exif = {
   PIL.ExifTags.TAGS[k]: v for k, v in info.items() if k in PIL.ExifTags.TAGS
}

print(exif)
print(info.items())
#for tag, value info.items()
