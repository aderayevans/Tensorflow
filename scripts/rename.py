import os
import pathlib
import shutil
import re
from bs4 import BeautifulSoup as BS
from xml.etree import ElementTree as et

CUR_DIR = str(pathlib.Path(__file__).parent.resolve())

input_path = os.path.join(CUR_DIR, 'bed')

output_path = CUR_DIR + '/new'

if not os.path.exists(output_path):
    os.makedirs(output_path)

images = [f for f in os.listdir(input_path)
            if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.jpeg|.png|.webp)$', f)]

num_images = len(images)
print(num_images)

for i in range(num_images):
    newname = 'bed-' + str(i)
    filename = images[i]
    xml_filename = os.path.splitext(filename)[0]+'.xml'

    absolute_path_image = os.path.join(input_path, filename)
    absolute_path_xml = os.path.join(input_path, xml_filename)

    try:
        xmlTree  = et.parse(absolute_path_xml)
        rootElement = xmlTree.getroot()
        xmlTree.find('filename').text = newname + '.jpg'
        xmlTree.write(absolute_path_xml)
    except FileNotFoundError:
        continue


    dist_xml = os.path.join(output_path, newname + '.xml')
    # print(dist_xml)
    dist_jpg = os.path.join(output_path, newname + '.jpg')
    
    # os.replace(absolute_path_xml, dist_xml)
    # os.replace(absolute_path_image, dist_jpg)

    shutil.copyfile(absolute_path_xml, dist_xml)
    shutil.copyfile(absolute_path_image, dist_jpg)

    # print(filename + '--->' + newname + '.jpg')
    # print(xml_filename + '--->' + newname + '.xml')
