import face_recognition
import cv2
import os, os.path
import json
# Get a reference to webcam #2 
#my webcam is 2 number way
#video_capture = cv2.VideoCapture(1)
#debug info OpenCV version
print ("OpenCV version: " + cv2.__version__)

#image path and valid extensions
imageDir = "/home/mrkahraman/Desktop/graduationproject/test1/image/" #specify your path here
image_path_list = []
valid_image_extensions = [".jpg", ".jpeg", ".png", ".tif", ".tiff"] #specify your vald extensions here
valid_image_extensions = [item.lower() for item in valid_image_extensions]

#create a list all files in directory and
#append files with a vaild extention to image_path_list
for file in os.listdir(imageDir):
    extension = os.path.splitext(file)[1]
    if extension.lower() not in valid_image_extensions:
        continue
    image_path_list.append(os.path.join(imageDir, file))

#loop through image_path_list to open each image
for imagePath in image_path_list:
    newlist=[];
    name = '';
    name, ext = (os.path.basename(imagePath)).split('.')
    name_image = face_recognition.load_image_file(imagePath)
    name_face_encoding = face_recognition.face_encodings(name_image)[0]
    for index in range(len(name_face_encoding)):
        newlist.append(name_face_encoding[index]); 
    # = {name:newlist}
    with open('list.json', 'r') as F:    
            data = json.loads(F.read())
    #data ={'':''}
    #new_data = {name:newlist}
    data[name] = newlist
        
               
        #data['x'].append({name:newlist})
    with open('list.json', 'w') as F:
            F.write(json.dumps(data))
print("image installed successfully")            
