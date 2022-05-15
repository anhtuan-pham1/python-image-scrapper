from selenium import webdriver
import time
from urllib.request import Request, urlopen
import requests
import os
import errno
import sys
import argparse


# function to scroll down current website
def scroll_down(driver):
    print("Scrolling down")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)


# function to get image url and store in a list then download the images.
def get_image_url(driver,keyword, quantity=100, maxsize=float("inf")):
    URL = f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={keyword}&oq={keyword}&gs_l=img"
    driver.get(URL)
    scroll_down(driver)
    time.sleep(1)
    number_results = len(driver.find_elements_by_css_selector("img.Q4LuWd"))
    print(number_results)
    quantity = int(quantity)
    max_size = maxsize

    while number_results < quantity:
        scroll_down(driver)
        number_results = len(
            driver.find_elements_by_css_selector("img.Q4LuWd"))
        print(number_results)
        
    image_urls = []
    count = 0
    curr = 1
    actual_quantity = quantity

    while curr < actual_quantity+1:
        try:
            img = driver.find_element_by_xpath(
                    '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' % (str(curr)))
            img.click()
            time.sleep(1)
            print('Clicked')
            time.sleep(1)
            images = [driver.find_elements_by_class_name("n3VNCb")][0]
            for image in images:
                if(image.get_attribute("src")[:4].lower() in ["http"]):
                    
                    if filter_image_size(image.get_attribute("src"), max_size) == True:
                        image_urls.append(image.get_attribute("src"))
                        count += 1
                        print("%d. %s" %
                                (count, image.get_attribute("src")))
                        break
                    else:
                        actual_quantity += 1
                        print("Invalid size: " + image.get_attribute("src"))

            
        except Exception as e:
            print("[INFO] Unable to get link")
            print(e)
        curr += 1
    print(image_urls)

    save_image(image_urls,keyword)
    for i in image_urls:
        filter_image_size(i,max_size)
    return image_urls

# Optional function to filter size of an image
def filter_image_size(url,max_size):
    req = Request(url,
                headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).info()
    if (int(webpage['Content-Length']) > max_size):
        return False
    return True


# function to save image in curren_dir/keywordfolder
def save_image(urls,key_word):
    curr_path = os.getcwd()
    filename = f"{curr_path}/{key_word}"
    print(curr_path)
    if not os.path.exists(os.path.dirname(f'{key_word}')):
        print("succeeded")
        try:
            os.mkdir(filename)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    else:
        print("Existed")
    for i in range (len(urls)):
        with open(f'{key_word}/{i}.jpg', 'wb') as handle:
            response = requests.get(urls[i], stream=True)

            if not response.ok:
                print (response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)


def main(keyword, quantity, max_size):

    
    path = "D:\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(path, options=options)
    get_image_url(driver,keyword, quantity, max_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description for my parser")
    parser.add_argument(
        "-keyword", "--keyword", help="Keyword argument", required=True, default="")
    parser.add_argument(
        "-quantity", "--quantity", help="Quantity", required=False, default=100)
    parser.add_argument(
        "-maxsize", "--maxsize", help="Max Size", required=False, default=float("inf"))

    argument = parser.parse_args()
    status = False

    print(argument.keyword)
    print(argument.quantity)
    print(argument.maxsize)
    main(argument.keyword, argument.quantity, argument.maxsize)
