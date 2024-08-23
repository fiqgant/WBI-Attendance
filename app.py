import face_recognition
import cv2
import numpy as np
import pandas as pd
import pickle
import csv
from datetime import datetime

f=open("details.pkl","rb")
stu_details=pickle.load(f)
f.close()

f=open("embed_details.pkl","rb")
embeded=pickle.load(f)
f.close()

known_face_encodings = []  #for storing face encodings
known_face_names = []   # for storing registration no

now=datetime.now()
current_date=now.strftime("%Y-%m-%d")
# f1=open(current_date+'.csv','w+',newline='')

filename=current_date+'.csv'

h=["Nama&NIM" , "Time"]
with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(h) 

df=pd.read_csv(filename)

for NIMNo , embed_list in embeded.items():
    for my_embed in embed_list:
        known_face_encodings +=[my_embed]
        known_face_names += [NIMNo]

# with webcam
video_capture = cv2.VideoCapture(0)

# with ip
# url="http://192.168.100.124:8080/video"
# video_capture = cv2.VideoCapture(url)


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True  :
  
    ret, frame = video_capture.read() #capture video frame

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # resize
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    if process_this_frame:

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) # getting encoding for the faces in frames

        face_names = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding) # compare the encoding with our known encodings with tolerance of 0.6
            name = "Tidak diketahui"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding) # calculating distance using euclid formula
            best_match_index = np.argmin(face_distances) # gettinng index which has min distance
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name) #storing registration no of best match

    process_this_frame = not process_this_frame

    for(top_s, right, bottom, left), name in zip(face_locations, face_names):
        top_s *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top_s), (right, bottom), (47, 78, 31), 3) #making rectangle around face

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (143, 255, 255), cv2.FILLED)# a filled rectangle
        font = cv2.FONT_HERSHEY_TRIPLEX
        details="Mahasiswa tidak terdaftar!"
        if(name !="Tidak diketahui"):
            details=stu_details[name]+","+name
    
        cv2.putText(frame, details, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)#putting text
        
        if(details not in df.values):
            row=[details,datetime.now().strftime("%H-%M-%S")]
            df.loc[len(df)]=row 
            df.to_csv(filename,index=False)
            df = pd.read_csv(filename)
    
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()