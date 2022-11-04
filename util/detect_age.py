import sys
import cv2

class Detector:

    def detector( self):
        cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_alt.xml')
        ModelMean = (78.4263377603, 87.7689143745, 114.895847746)
        ageNet = cv2.dnn.readNetFromCaffe('./models/deployAge.prototxt', './models/ageNet.caffemodel')
        genderNet = cv2.dnn.readNetFromCaffe('./models/deployGender.prototxt', './models/genderNet.caffemodel')

        ageList = ['(0~2)', '(4~10)', '(10~15)', '(15~25)',
                   '(25~35)', '(50~60)', '(60~70)', '(80~)']
        genderList = ['Man', 'Female']

        cap = cv2.VideoCapture(0)
        self.flag = True
        self.detect_age = False
        self.info = genderList[1] + '/' + ageList[7]
        # self.info = genderList[1] + '/' + ageList[2]
        # self.detect_age = True
        while self.flag:
            ret, img = cap.read()

            img = cv2.resize(img, dsize=(640,640), fx = 1.0, fy = 1.0)
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
                self.info = genderList[gender] + '/' + ageList[age]
                self.detect_age = True
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), thickness=2)
                cv2.putText(img, self.info, (x, y - 15), 0, 0.5, (0, 255, 0), 1)

            # 사진 출력
            cv2.imshow('Age', img)

            if cv2.waitKey(1) & 0xFF == ord('q') or self.detect_age:
                break
        print(self.info)
        return (self.info)

if __name__ == "__main__":
    obj = Detector()
    data = obj.detector()
    age_split = str(data).split('/')[1]
    age = age_split.split("~")[0]
