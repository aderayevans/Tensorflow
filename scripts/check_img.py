import os
import cv2
import imghdr
import shutil

def check_images( s_dir, ext_list):
    bad_images=[]
    bad_ext=[]

    if os.path.isdir(s_dir):
        file_list = os.listdir(s_dir)

        for f in file_list:               
            index = f.rfind('.')
            ext = f[index+1:].lower()

            if ext == "xml":
                continue

            f_path = os.path.join(s_dir, f)

            tip = imghdr.what(f_path)

            if ext_list.count(tip) == 0:
                bad_images.append(f_path)

            if ext not in ext_list:
                print('file ', f_path, ' has an invalid extension ', ext)
                bad_ext.append(f_path)

            if os.path.isfile(f_path):
                try:
                    img=cv2.imread(f_path)
                    shape=img.shape
                except:
                    print('file ', f_path, ' is not a valid image file')
                    bad_images.append(f_path)
        # print ('*** WARNING*** you have files in ', s_dir, ' it should only contain sub directories')
    return bad_images, bad_ext

source_dir = r'D:\Workplace\JianYang\scripts\hotdog food hd'
good_exts = ['jpg', 'png', 'jpeg', 'gif', 'bmp' ] # list of acceptable extensions
bad_file_list, bad_ext_list = check_images(source_dir, good_exts)

if len(bad_file_list) !=0:
    print('improper image files are listed below ({})'.format(len(bad_file_list)))
    for i in range (len(bad_file_list)):
        print (bad_file_list[i])
        print (imghdr.what(bad_file_list[i]))

        output_path = r'D:\Workplace\JianYang\scripts\wrong_format_images'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        shutil.move(bad_file_list[i], output_path)

else:
    print(' no improper image files were found')


