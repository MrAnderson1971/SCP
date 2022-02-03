from selenium import webdriver
from webdriver_manager.opera import OperaDriverManager
from selenium.common.exceptions import NoSuchElementException
from os.path import expanduser
from tqdm import tqdm
from urllib3.exceptions import ProtocolError
import random
import time

SAMPLE_SIZE = 500
CONTINUE = 3094

class SCP:
    def __init__(self, link, rating, object_class):
        self.link = link
        self.rating = rating
        self.object_class = object_class
        
    def __repr__(self):
        return '%s,%s,%s,%s,\n' % (self.link, self.link.strip('http://scp-wiki.net/scp-'), self.rating, self.object_class)
    
    def __eq__(self, other):
        return self.link == other.link


def get_object_class(driver):
    try:
        driver.find_element_by_link_text('safe')
        return 'safe'
    except NoSuchElementException:
        pass

    try:
        driver.find_element_by_link_text('euclid')
        return 'euclid'
    except NoSuchElementException:
        pass

    try:
        driver.find_element_by_link_text('keter')
        return 'keter'
    except NoSuchElementException:
        pass

    try:
        driver.find_element_by_link_text('thaumiel')
        return 'thaumiel'
    except NoSuchElementException:
        pass

    try:
        driver.find_element_by_link_text('neutralized')
        return 'neutralized'
    except NoSuchElementException:
        pass

    return 'esoteric'
    
# Hope the user has enabled VPN on Opera.
opera_profile = 'C:\\Users\\marym\\AppData\\Roaming\\Opera Software\\Opera Stable'
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=%s' % opera_profile)
options._binary_location = '%s\\AppData\Local\\Programs\\Opera\\67.0.3575.137\\opera.exe' % expanduser('~')

driver = webdriver.Opera(executable_path=OperaDriverManager().install(), options=options)

driver.get('https://whatismyipaddress.com')
time.sleep(5)

scps = list(range(2, 3904))
#random.shuffle(scps)

_ = list(range(SAMPLE_SIZE))

start = time.time()

for skip in tqdm(scps):
    if skip < CONTINUE:
        continue
    
    number = str(skip)
    while len(number) < 3:
        number = '0' + number

    link = 'http://scp-wiki.net/scp-' + number

    while True:
        try:
            driver.get(link)
            break
        except BaseException as e:
            print(e)
    
    try:
        rating = int(driver.find_element_by_id('prw54355').text.strip('+'))
    except NoSuchElementException:
        rating = -999
        
    object_class = get_object_class(driver)

    new_scp = SCP(link, rating, object_class)

    scps.append(new_scp)

    while True:
        try:
            with open('scps.csv', 'a') as f:
                f.write(str(new_scp))
            break
        except PermissionError:
            print('Please close the document.')

print('Dataset generated in %s seconds.' % (time.time() - start))
input()
    
