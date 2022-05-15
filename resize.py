from PIL import Image
import os
import math
folder = 'dog'
curr_path = os.getcwd()
filename = f"{curr_path}/{folder}"
total = 0
#set boundary of valid in put
max_size = 10000
boundary = 2000
upper_ratio = 0.5
lower_ratio = 1.5

# get all the length of file in directory
for root, dirs, files in os.walk(folder):
    total += len(files)


for i in range (total):
    im = Image.open(f"{filename}\{i}.jpg")
    width, height = im.size
    size = os.path.getsize(f"{filename}\{i}.jpg")
    print(size)
    while True:
        if size >= max_size + boundary:
            ratio = upper_ratio

        elif size <= max_size - boundary:
            ratio = lower_ratio
        else:
            break
        width = int(math.ceil(width * ratio))
        height = int(math.ceil(height * ratio))
        newsize = (width, height)
        print(newsize)
        im = im.resize(newsize)
        im.save(f"{filename}\{i}.jpg")
        size = os.path.getsize(f"{filename}\{i}.jpg")
    
    
