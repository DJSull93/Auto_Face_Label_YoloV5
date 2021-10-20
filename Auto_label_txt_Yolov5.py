from mtcnn import MTCNN
import cv2
import os
import utils
from PIL import Image

import numpy as np 

def draw_bbox(bounding_boxes, image):
    x1, y1, x2, y2 = bounding_boxes
    cv2.rectangle(image, (int(x1), int(y1)), (int(x1)+int(x2), int(y1)+int(y2)),
                    (0, 0, 255))
    
    return image

def write_txt(list, fname, sep) :
    file = open(fname, 'w')
    vstr = ''
    for a in list :
        vstr = vstr + str(a) + sep
    vstr = vstr.rstrip(sep)  
    file.writelines(vstr)    
    file.close()

def label_image(source_dir, dest_dir, mode):
    
    if os.path.isdir(dest_dir)==False:
        os.mkdir(dest_dir)
    detector = MTCNN()
    source_list=os.listdir(source_dir)
    undif_file_list=[]

    for f in source_list:
        f_path=os.path.join(source_dir, f)
        dest_path=os.path.join(dest_dir, f)
        img=cv2.imread(f_path)
        data=detector.detect_faces(img)
        if data ==[]: # not detected
            undif_file_list.append(f_path)
        else:
            if mode==1:  #detect the box with the largest area
                for i, faces in enumerate(data): # iterate through all the faces found
                    box=faces['box']  # get the box for each face                
                    biggest=0                    
                    area = box[3] * box[2]
                    if area>biggest:
                        biggest=area
                        bbox=box 
                bbox[0]= 0 if bbox[0]<0 else bbox[0]
                bbox[1]= 0 if bbox[1]<0 else bbox[1]

                image_array = draw_bbox(bbox, img)
                cv2.imwrite(dest_path, image_array) # save img with box for check

                # change cordinate to yolo style                
                # print(img.shape) #(y, x, color)
                wid = round(1./img.shape[1], 6)
                hei = round(1./img.shape[0], 6) 
                bbox = [(bbox[0]+(bbox[2]/2)), (bbox[1]+(bbox[3]/2)) ,bbox[2], bbox[3]]
                bbox_yolo = [bbox[0]*wid, bbox[1]*hei, bbox[2]*wid, bbox[3]*hei]
                # print(bbox_yolo)
                text = label + bbox_yolo 
                print(text) # check text and cordinate correct
                fname=os.path.splitext(f)[0]
                tname=fname + ".txt"
                save_text=os.path.join(text_dir,tname)
                write_txt(text, save_text, sep="\t")

            else:
                for i, faces in enumerate(data): # iterate through all the faces found
                    box=faces['box']
                    if box !=[]:
                        # return all faces found in the image
                        box[0]= 0 if box[0]<0 else box[0]
                        box[1]= 0 if box[1]<0 else box[1]
                        cropped_img=img[box[1]: box[1]+box[3],box[0]: box[0]+ box[2]]
                        cropped_img=draw_bbox(box, cropped_img)
                        fname=os.path.splitext(f)[0]
                        fext=os.path.splitext(f)[1]
                        fname=fname + str(i) + fext
                        tname=fname + str(i) + ".txt"

                        save_path=os.path.join(dest_dir,fname)
                        save_text=os.path.join(text_dir,tname)

                        cv2.imwrite(save_path, cropped_img)  
                        text = label + bbox 
                        print(text)
                        write_txt(text, save_text, sep="\t")

    return undif_file_list

folder = 'put your folder name'
label = [1] # put your label number, ex) 0, 1, 2 ...

source_dir=rf'D:/00_TeamProject/_data/{folder}/images' # directory with files label
dest_dir=rf'D:/00_TeamProject/_data/{folder}/label_pic' # directory where labeled images get stored
text_dir=rf'D:/00_TeamProject/_data/{folder}/labels' # directory where label and x,y,w,h txt files get stored

uncropped_files_list=label_image(source_dir, dest_dir,1) 