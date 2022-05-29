from datetime import datetime
import os
import face_recognition
from sklearn import svm

def markAttendance(name):
    with open('C:/Users/VANDANA/Desktop/MARKED_ ATTENDANCE.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'\n{name}, {time}, {date}')

def f_recognize(dir, test):
    # logging.debug("hello from f_recog")
    # Training the SVC classifier
    # The training data would be all the 
    # face encodings from all the known 
    # images and the labels are their names
    print("Inside f_recognize")
    encodings = []
    names = []
  
    # Training directory
    if dir[-1]!='/':
        dir += '/'
    train_dir = os.listdir(dir)
  
    # Loop through each person in the training directory
    for person in train_dir:
        pix = os.listdir(dir + person)
  
        # Loop through each training image for the current person
        for person_img in pix:
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file(
                dir + person + "/" + person_img)
            face_bounding_boxes = face_recognition.face_locations(face)
  
            # If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image 
                # with corresponding label (name) to the training data
                encodings.append(face_enc)
                names.append(person)
            else:
                print(person + "/" + person_img + " can't be used for training")
  
    # Create and train the SVC classifier
    clf = svm.SVC(gamma ='scale')
    clf.fit(encodings, names)
    print(names)

    test_image = face_recognition.load_image_file(test)

    face_locations = face_recognition.face_locations(test_image)
    no = len(face_locations)
    print("Number of faces detected: ", no)
  
    print("Found:")
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(test_image)[i]
        name = clf.predict([test_image_enc])
        print(name[0])
        markAttendance(name)
    return name[0]

if __name__ == "__main__":
    f_recognize('./images/train/','./images/ez.jpg')
