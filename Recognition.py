
from easyocr import Reader
import arabic_reshaper
import cv2
import os

def PlateOCR(imagePath):
    #_______________ reading and preprocessing the target image______________
    car = cv2.imread(imagePath)
    car = cv2.resize(car, (800, 600))
    gray = cv2.cvtColor(car, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.Canny(blur, 10, 200)
    #cv2.imshow('Image', edged)
    cv2.waitKey(0)
    cont, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key = cv2.contourArea, reverse = True)[:5]

    #________________ Search about plate shape
    plate_cnt=(0,0,0,0)
    for c in cont:
        arc = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * arc, True)
        if len(approx) == 4:
            plate_cnt = approx
            break

    (x, y, w, h) = cv2.boundingRect(plate_cnt)
    plate = gray[y:y + h, x:x + w]

    #_________________plate number detection or OCR
    reader = Reader(['en','ar'],  gpu=False, verbose=False)
    detection = reader.readtext(plate)
    #print(detection)
    #print(len(detection))
    plateData=[]
    accuracy=0.0
    outPath=''
    outName=imagePath.split('/')[-1]
    accuracyAvg=0
    if len(detection) == 0:
        text = "I can't detect the painting,\n please re-upload the image in high quality"
        plateData=text
        cv2.putText(car, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
        outPath='OutPlates/'+str(outName)+'.jpg'
        cv2.imwrite(outPath, car)
        #cv2.imshow('Image', car)
        cv2.waitKey(0)
    else:
        cv2.drawContours(car, [plate_cnt], -1, (0, 255, 0), 3)
        text = f"{detection[0][1]} {detection[0][2] * 100:.2f}%"
        text = arabic_reshaper.reshape(text)
        cv2.putText(car, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        #print(text)
        for i in range(len(detection)):
            plateData.append(str(detection[i][1]))
            accuracy=+accuracy+ float(detection[i][2])
        accuracyAvg=round(accuracy/len(detection))*100
        outPath='OutPlates/'+str(outName)+str(detection[0][1])+'.jpg'
        cv2.imwrite(outPath, car)
        cv2.waitKey(0)
        plateData="""
                    {}""".format("\n".join(plateData))
    return str(plateData), outPath, accuracyAvg

'''
plateData, outPath, accuracyAvg=PlateOCR('D:/Job Task/3-Task Smart Life/cars/01.jpg')

print(plateData)
print(outPath)
print(accuracyAvg)

'''