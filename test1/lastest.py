import face_recognition
import cv2
import os, os.path
import json
import sqlite3
import datetime
import re

conn = sqlite3.connect('/home/mrkahraman/Desktop/graduationproject/Faceweb/mysite/db.sqlite3')
c = conn.cursor()



now = datetime.datetime.now()
#c.execute("SELECT * FROM pages_student WHERE user_id=(SELECT id FROM auth_user WHERE username = ?)", (name,))
student=c.execute("SELECT user_id FROM pages_student")
dayname = now.strftime("%A")
date = now.strftime("%Y-%m-%d")
oldname1 = None
oldname2 = None
counter1 = 0
counter2 = 0
row = student.fetchall()
query = c.execute("SELECT * FROM pages_attendance WHERE attendance_date = ?",(date,)).fetchall()
if query:
    print("Attendance table was existed")
    
else:
    print("Attendance table is created")
    for index in range(len(row)):
        username = c.execute("SELECT username FROM auth_user WHERE id = ?", (row[index][0],)).fetchone()
        classroom = c.execute("SELECT classroom FROM pages_student WHERE user_id = ?", (row[index][0],)).fetchone()
        time = c.execute("SELECT l_time FROM pages_timetable WHERE dayname = ? AND classroom = ? ", (dayname, classroom[0],)).fetchall() 
        for row2 in time:
                lessons = c.execute("SELECT lesson FROM pages_timetable WHERE dayname = ? AND classroom = ? AND l_time = ?", (dayname, classroom[0], row2[0],)).fetchone()
                teacher = c.execute("SELECT teacher_id FROM pages_teacherlesson WHERE classroom = ? AND lesson = ?", (classroom[0], lessons[0],)).fetchone()
                c.execute("INSERT INTO pages_attendance(id,student_id, teacher_id, lessons, attendance_date, timing, status, classroom ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",(None, username[0], teacher[0], lessons[0], date, row2[0], "Absent", classroom[0],))
                conn.commit()






# Get a reference to webcam #2 
#my webcam is 2 number way
video_capture = cv2.VideoCapture(1)
#debug info OpenCV version
print ("OpenCV version: " + cv2.__version__)

'''#image path and valid extensions
imageDir = "/home/mrkahraman/Desktop/test/" #specify your path here
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
    
    new_data = {name:newlist}
    data[name] = newlist
        
               
        #data['x'].append({name:newlist})
    with open('list.json', 'w') as F:
            F.write(json.dumps(data))
'''
with open('list.json', 'r') as F:
    B = json.loads(F.read())

known_face_encodings = [];
known_face_names = [];
for x in B:
    known_face_encodings.append(B[x])
    known_face_names.append(x)
    






while True:
    
    
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"
       

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            print("finding name =", name)
            #print(detect_list)
            #print(known_face_names)

            
            
            
            if oldname1 is None:
                oldname1 = name
                print("oldname1 =", oldname1)
                    
            elif oldname1 is not None and oldname2 is None and name != oldname1:
                oldname2 = name
                print("oldname2 =", oldname2)

            if name == oldname1:
                counter1 += 1
                counter2 -= 1
                print("counter1 =", counter1)
                print("counter2 =", counter2)

            if name == oldname2:
                counter2 += 1
                counter1 -= 1
                print("counter1 =", counter1)
                print("counter2 =", counter2)

            clock = now.strftime("%H.%M")
            timing = ""
            print(clock)
            if (clock >= '09.00' and clock <= '09.50'):
                timing = "09.00"
            elif  (clock >= '10.00' and clock <= '10.50'):
                timing = "10.00"
            elif (clock >= '11.00' and clock <= '11.50'):
                timing = "11.00"
            print(timing)
            if counter1 >= 10 and counter1 > counter2:
                name = oldname1
                counter1 = 0
                counter2 = 0
                if name != "Unknown":
                    print(name)
                    #find_classroom = c.execute("SELECT classroom FROM pages_student WHERE user_id=(SELECT id FROM auth_user WHERE username = ?)", (name,)).fetchone()
                    #print(find_classroom[0])
                    print(timing)
                    c.execute("UPDATE pages_attendance set status = 'Came' WHERE student_id = ? AND attendance_date = ? AND timing = ?  ",(name, date, timing,))
                    conn.commit()
                           

            elif counter2 >=10 and counter2 > counter1:
                name = oldname2
                counter1 = 0
                counter2 = 0
                if name != "Unknown":
                    print(name)
                    #find_classroom = c.execute("SELECT classroom FROM pages_student WHERE user_id=(SELECT id FROM auth_user WHERE username = ?)", (name,)).fetchone()
                    #print(find_classroom[0])
                    c.execute("UPDATE pages_attendance set status = 'Came' WHERE student_id = ? AND attendance_date = ? AND timing = ?",(name, date, timing,))
                    conn.commit()
                            

                    


        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


