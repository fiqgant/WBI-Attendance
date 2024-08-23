import cv2 
import face_recognition
import pickle


mahasiswaNama=input("Nama : ")
NIMNo=input("Nomor Induk. : ")

try:
    f=open("details.pkl","rb")

    stu_details=pickle.load(f)
    f.close()
except:
    stu_details={}
    
stu_details[NIMNo]=mahasiswaNama


f=open("details.pkl","wb")
pickle.dump(stu_details,f)
f.close()

# embeded dictorinary for storing facial encodings having registration no as a key
try:
    f=open("embed_details.pkl","rb")

    embeded=pickle.load(f)
    f.close()
except:
    embeded={}

for i in range(5):
    key = cv2. waitKey(1) #display frame for 1ms
    webcam = cv2.VideoCapture(0) #return video feed from first cam
    while True:
        check, frame = webcam.read() #capture video frame

        cv2.imshow("Capturing...", frame) #dispalying the frame
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) #resize image to 25%
        rgb_small_frame = small_frame[:, :, ::-1] # BGR to RGB conversion
        key = cv2.waitKey(1)

        if key == ord('s') : # if s key is pressed
            face_locations = face_recognition.face_locations(rgb_small_frame) # getting all faces in image 
            if face_locations != []: # if we get  any faces in image
                face_encoding = face_recognition.face_encodings(frame)[0] #getting first face found in image
                print(face_encoding)
                if NIMNo in embeded: # if student already exists than we add encoding to data else  for new student create new key with registraion no and encodings as key to that
                    embeded[NIMNo]+=[face_encoding]
                else:
                    embeded[NIMNo]=[face_encoding]
                webcam.release()
                cv2.waitKey(1)
                cv2.destroyAllWindows()     
                break
        elif key == ord('q'):
            webcam.release()
            print("Camera off.")
            cv2.destroyAllWindows()
            break
print(embeded)
f=open("embed_details.pkl","wb")
pickle.dump(embeded,f)
f.close()