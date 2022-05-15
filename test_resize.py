import os
import time
folder = 'dog'
curr_path = os.getcwd()
filename = f"{curr_path}/{folder}"
total = 0
max_size = 10000
boundary = 2000

for root, dirs, files in os.walk(folder):
    total += len(files)

for i in range(total):
    print("-----------------------------")
    size = os.path.getsize(f"{filename}\{i}.jpg")
    print(f'Current size of {i}.jpg is : {size}')
    if size >= boundary - max_size or size <= boundary + max_size:
        print('Passed')
    else:
        print('Failed')

