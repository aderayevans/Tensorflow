import os
import pathlib
from bs4 import BeautifulSoup

CUR_DIR = str(pathlib.Path(__file__).parent.resolve())
print('Current directory: ' + CUR_DIR)

def load_xml(label, CHECK_EACH = False):
    print('\n*** Label:' + label)
    file_path = os.path.join(CUR_DIR, label)
    print('Current path: ' + file_path)

    label_num = 0
    xml_num = 0
    for file in os.listdir(file_path):
        if CHECK_EACH: print(file)

        if file.endswith(".xml"):
            absolute_path = os.path.join(file_path, file)
            # print(absolute_path)
            with open(absolute_path, 'r') as f:
                data = f.read()
            Bs_data = BeautifulSoup(data, "xml")
            
            for element in Bs_data.find_all('name'):
                if element.get_text() != label:
                    b_filename = Bs_data.find('filename')
                    print('!!!WRONG LABEL NAME')
                    print('{} got label {} instead of {}'.format(b_filename.get_text(), element.get_text(), label))
                    break
                else:
                    label_num += 1
            xml_num += 1
    print(label + " checked " + str(xml_num) + " imgs with " + str(label_num) + " labels")


# THE_LABEL = 'bed'
# load_xml(THE_LABEL, CHECK_EACH = True)

# load_xml('bed')
# load_xml('induction_hob')
# load_xml('ban')
# load_xml('ghe')
# load_xml('curtains')
# load_xml('hammock')
# load_xml('tulanh')
# load_xml('kettle')

[load_xml(s) for s in os.listdir(CUR_DIR) if os.path.isdir(os.path.join(CUR_DIR, s))]