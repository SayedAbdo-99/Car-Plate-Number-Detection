from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import sys

from GUI import *

from PyQt5.uic import loadUiType

from os import path

from Recognition import PlateOCR

selectimage,_ = loadUiType('GUI/selectimage.ui')
finalresult,_ = loadUiType('GUI/finalresult.ui')


class SelectImage(QWidget, selectimage):
    def __init__(self , parent=None):
        super(SelectImage , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttoms()

    def Handel_UI(self):
        self.setWindowTitle("Select Image")
        self.setFixedSize(800,800)
            
    def Handel_Buttoms(self):
        self.btnBrowse.clicked.connect(self.Browse)
        self.btntestdisk.clicked.connect(self.TestDiskImage)
        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_Style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_15.clicked.connect(self.Apply_QDarkBlue_Style)
        self.btncancel.clicked.connect(self.close)

    def Apply_DarkOrange_Style(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Apply_QDark_Style(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Apply_DarkGray_Style(self):
        style = open('themes/qdarkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Apply_QDarkBlue_Style(self):
        style = open('themes/darkblu.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    def Browse(self):
        save_location = QFileDialog.getOpenFileName()
        #print(save_location[0])
        imagePath=save_location[0]
        self.lePath.setText(str(save_location[0]))
        #print(self.lePath.text())
        if self.lePath.text() !='':
            self.lb1.setPixmap(QPixmap(imagePath))
        else:
            QMessageBox.warning(self , "Data Error" , "You Must Select The Image File")

    def TestDiskImage(self):
        plateData, platePath, accuracyAvg = PlateOCR(str(self.lePath.text()))
        self.app = QApplication(sys.argv)
        self.window2 = FinalResult(plateData=plateData,platePath=platePath,accuracy=accuracyAvg)
        self.hide()
        self.window2.show()
        self.app.exec_()


class FinalResult(QWidget, finalresult):
    def __init__(self , parent=None,plateData='',platePath='',accuracy=0.0):
        super(FinalResult , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttoms()
        
        self.lb_image.setPixmap(QPixmap(platePath)) 
        self.p1.setText(str(accuracy)+"%")
        self.finalresult.setText(plateData)
        
    def Handel_UI(self):
        self.setWindowTitle("Final Results Report")
        self.setFixedSize(650,800)
        
    def Handel_Buttoms(self):        
        self.pushButton_6.clicked.connect(self.NewTest)
        self.btncancel.clicked.connect(self.close)
        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_Style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_15.clicked.connect(self.Apply_QDarkBlue_Style)

    def NewTest(self):
        self.app = QApplication(sys.argv)
        self.window2 = SelectImage()
        self.hide()
        self.window2.show()
        self.app.exec_()

    def Apply_DarkOrange_Style(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_QDark_Style(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_DarkGray_Style(self):
        style = open('themes/qdarkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_QDarkBlue_Style(self):
        style = open('themes/darkblu.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    try: 
        app = QApplication(sys.argv)
        window = SelectImage()
        window.show()
        app.exec_()
        
    except:
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()