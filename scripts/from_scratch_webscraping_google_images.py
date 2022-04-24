from ast import keyword
import bs4
from grpc import services
import requests
from selenium import webdriver
import os
import pathlib
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#creating a directory to save images
CUR_DIR = str(pathlib.Path(__file__).parent.resolve())
print(CUR_DIR)

keyword = "table"
folder_name = os.path.join(CUR_DIR, keyword)
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)


def download_image(url, folder_name, num):
    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)

# chromeDriverPath = os.path.join(CUR_DIR, 'chromedriver.exe')
# service = webdriver.chrome.service.Service(chromeDriverPath)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver = webdriver.Chrome(service=service, options=options)

search_URL = "https://www.google.com/search?q=" + keyword + "&source=lnms&tbm=isch"
driver.get(search_URL)

a = input("Waiting...")

SCROLL_PAUSE_TIME = 0.5

#Scrolling all the way up
driver.execute_script("window.scrollTo(0, 0);")

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"isv-r PNCib MSM1fd BUooTd"} )

print(len(containers))

len_containers = len(containers)

for i in range(1, len_containers + 1):
    if i % 25 == 0:
        continue

    xPath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)

    try:
        previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
        previewImageElement = driver.find_element(By.XPATH, previewImageXPath)
        previewImageURL = previewImageElement.get_attribute("src")
    #print("preview URL", previewImageURL)
    except:
        print("Unable to locate element XPATH at %i" %i)
        continue

    #print(xPath)

    driver.find_element(By.XPATH, xPath).click()
    time.sleep(3)

    timeStarted = time.time()
    while True:

        imageElement = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")
        # imageURL= imageElement.get_attribute('src')
        imageURL = driver.find_element_by_css_selector(".tvh9oe.BIB1wf .eHAdSb>img").get_attribute("src")

        if imageURL != previewImageURL:
            #print("actual URL", imageURL)
            break

        else:
            #making a timeout if the full res image can't be loaded
            currentTime = time.time()

            if currentTime - timeStarted > 10:
                print("Timeout! Will download a lower resolution image and move onto the next one")
                break


    #Downloading image
    try:
        download_image(imageURL, folder_name, i)
        print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
    except:
        print("Couldn't download an image %s, continuing downloading the next one"%(i))