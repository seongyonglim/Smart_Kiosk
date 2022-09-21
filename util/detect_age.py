import cv2


class Detector:

    def detector( self, img, cascade, ageNet, genderNet, ModelMean, ageList, genderList):
        img = cv2.resize(img, dsize=(320,320), fx = 1.0, fy = 1.0)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(img_gray , scaleFactor=1.5 , minNeighbors=5 , minSize=(20,20))
    
        for box in faces :
            x, y, w, h = box
            face = img[int(y):int(y + h), int(x):int(x + h)].copy()
            blob = cv2.dnn.blobFromImage(face, 1, (227, 227), ModelMean, swapRB=False)
    
            genderNet.setInput(blob)
            gender_preds = genderNet.forward()
            gender = gender_preds.argmax()
    
            ageNet.setInput(blob)
            age_preds = ageNet.forward()
            age = age_preds.argmax()
            info = genderList[gender] + ' ' + ageList[age]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), thickness=2)
            cv2.putText(img, info, (x, y - 15), 0, 0.5, (0, 255, 0), 1)
    
        # 사진 출력
        cv2.imshow('Age', img)
        cv2.waitKey()
        print(info)

    def detect(self, img):
        cascade = cv2.CascadeClassifier('../models/haarcascade_frontalface_alt.xml')
        ModelMean = (78.4263377603, 87.7689143745, 114.895847746)
        ageNet = cv2.dnn.readNetFromCaffe('../models/deployAge.prototxt', '../models/ageNet.caffemodel')
        genderNet = cv2.dnn.readNetFromCaffe('../models/deployGender.prototxt', '../models/genderNet.caffemodel')

        ageList = ['(0 ~ 2)', '(4 ~ 10)', '(15 ~ 25)', '(30 ~ 35)',
                   '(40 ~ 52)', '(58 ~ 63)', '(68 ~ 73)', '(80 ~ 100)']
        genderList = ['Man', 'Female']

        self.detector(img, cascade, ageNet, genderNet, ModelMean, ageList, genderList)

img = cv2.imread('../images/Test01.jfif')




#img = cv2.imread('../images/Test10.jpg')
#cv2.imshow('facenet', img)
obj = Detector()
obj.detect(img)