import sys

import cv2
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSignal

import GetM1Result
import GetM2Result
from M2ResultWindow import M2ResultWindow


class M2Dialog1(QDialog): #导入运行数据（成功or失败）
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./M2Dialog1.ui",self)

class M2Dialog2(QDialog): #查看运行评估结果
    def __init__(self,gzdw_data):
        super().__init__()
        self.gzdw_data = gzdw_data
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./M2Dialog2.ui",self)
        self.button_show = self.ui.show_btn
        self.button_show.clicked.connect(self.show_result)
        print("")

    def show_result(self):
        self.result_window = M2ResultWindow(self.gzdw_data)
        self.result_window.show()
        print("show")

from MainWindow import Ui_MainWindow
# 主窗口类
class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.statusbar = None
        self.gzdw_data = "xinyi"

        self.init_ui()


    def init_ui(self):
        self.ui = uic.loadUi("./MainWindow.ui",self)

        self.comboBox = self.ui.comboBox_M1Result

        self.comboBox.currentIndexChanged.connect(
            lambda: self.choose_result_image(self.comboBox.currentText()))

        self.statusbar = self.ui.statusbar

        self.m2_dialog2 = M2Dialog2(self.gzdw_data)
        #================================================
        self.button_run1 = self.ui.m1_run1
        #self.button_run2 = self.ui.m1_run2

        self.button_m2_btn1 = self.ui.m2_btn1
        self.button_m2_btn2 = self.ui.m2_btn2
        self.button_m2_btn3 = self.ui.m2_btn3

        self.label1 = self.ui.m1_p1
        #self.label2 = self.ui.m1_p2
        #self.label3 = self.ui.m1_p3
        self.label4 = self.ui.m2_p1

        self.action1 = self.ui.action1
        self.action2 = self.ui.action2
        #data_select_xinyin
        self.action_data_select_xinyi = self.ui.data_select_xinyi
        self.action_data_select_yinshan = self.ui.data_select_yinshan

        #===========================================
        self.action1.triggered.connect(self.open1)
        self.action2.triggered.connect(self.open2)
        self.action_data_select_xinyi.triggered.connect(lambda: self.select_data("xinyi"))
        self.action_data_select_yinshan.triggered.connect(lambda: self.select_data("yinshan"))

        self.button_run1.clicked.connect(self.m1_run1_f)
        #self.button_run2.clicked.connect(self.m1_run2_f)

        self.button_m2_btn1.clicked.connect(self.m2_run1_f)
        self.button_m2_btn2.clicked.connect(self.m2_run2_f)
        self.button_m2_btn3.clicked.connect(self.m2_run3_f)

    def choose_result_image(self,text):
        if(text == "系统线路传输容量"):
            self.show_imge_LC()
        elif(text == "新能源消纳率"):
            self.show_imge_REC()
        elif(text == "新能源消纳率响应前后"):
            self.show_imge_REC_Change()

    def show_imge_LC(self):
        self.resize_image_to_fit_label(self.img_LC_path, self.label1)

        print("show-image-LC")

    def show_imge_REC(self):

        self.resize_image_to_fit_label(self.img_REC_path, self.label1)
        print("show-image-REC")

    def show_imge_REC_Change(self):
        self.resize_image_to_fit_label(self.img_REC_change_path, self.label1)

        print("show-image-REC-Change")
    def select_data(self,data):
        self.gzdw_data = data
        print("using data: "+self.gzdw_data)
    def m2_run1_f(self): #导入电网数据
        self.gzdw_data_img_path = "image/"+self.gzdw_data+".png"
        self.gzdw_data_img = QPixmap(self.gzdw_data_img_path)
        self.label4.setPixmap(self.gzdw_data_img)
        self.label4.setScaledContents(True)
        #print("m2_run1")

    #显示运行数据成功窗口
    def m2_run2_f(self): #导入运行数据
        self.m2_dialog1 = M2Dialog1()
        self.m2_dialog1.show()

    def m2_run3_f(self): #运行评估
        print("run3")

        #self.getM2Result = GetM2Result(self,self.gzdw_data)

        self.thread_m2_matlab = GetM2Result.runMatlab(self.gzdw_data)
        #self.showStateBarMessgeM2ResultFinished()
        self.thread_m2_matlab.start()
        self.thread_m2_matlab.begin.connect(self.showStateBarMessgeM2ResultRuning)
        self.thread_m2_matlab.finished.connect(self.showStateBarMessgeM2ResultFinished)

    def showStateBarMessgeM2ResultRuning(self):
            self.statusbar.showMessage("matlab程序正在运行，耗时较长，请稍等")

    def showStateBarMessgeM2ResultFinished(self):
            self.statusbar.showMessage("运行成功！请查看结果！")
            self.openM2ResultDialog()
            print("")
    def openM2ResultDialog(self):

        self.m2_dialog2 = M2Dialog2(self.gzdw_data)
        self.m2_dialog2.show()
        print("")

    def m1_run1_f(self): # 新能源消纳|线路传输容量
        self.thread_run_m1_matlab = GetM1Result.runMatlab(self.gzdw_data)
        self.showStateBarMessgeM1ResultFinished() #直接显示图片，测试时使用


        self.thread_run_m1_matlab.start() #开启matlab运行线程
        self.thread_run_m1_matlab.begin.connect(self.showStateBarMessgeM1ResultRuning)
        self.thread_run_m1_matlab.finished.connect(self.showStateBarMessgeM1ResultFinished)



    def showStateBarMessgeM1ResultRuning(self):
            self.statusbar.showMessage("matlab程序正在运行，耗时较长，请稍等")

    def showStateBarMessgeM1ResultFinished(self):
            self.statusbar.showMessage("运行成功！请查看结果！")
            self.img_LC_path = 'LC_'+self.gzdw_data+'.png'
            self.img_REC_path = 'REC_'+self.gzdw_data+'.png'
            self.img_REC_change_path = 'REC_change_'+self.gzdw_data+'.png'
            print(self.img_LC_path,type(self.img_LC_path))

            print(self.img_LC_path+" "+self.img_REC_path+" "+self.img_REC_change_path)

            # img_LC = QPixmap(self.img_LC_path)
            # img_REC = QPixmap(self.img_REC_path)
            # img_REC_change = QPixmap(self.img_REC_change_path)



            self.label1.setAlignment(Qt.AlignCenter)
            #self.label2.setAlignment(Qt.AlignCenter)
            #self.label3.setAlignment(Qt.AlignCenter)

            # self.label3.setScaledContents(True)
            # self.label1.setScaledContents(True)
            # self.label2.setScaledContents(True)

            '''======================================================'''
            # self.label1.setPixmap(img_LC)
            # self.label2.setPixmap(img_REC)
            # self.label3.setPixmap(img_REC_change)
            self.resize_image_to_fit_label(self.img_LC_path,self.label1)
            #self.resize_image_to_fit_label(self.img_REC_path, self.label2)
            #self.resize_image_to_fit_label(self.img_REC_change_path, self.label3)



    def resize_image_to_fit_label(self, image_path, label):
        # 读取图片
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV默认使用BGR，转换为RGB以供Qt使用
        h, w, _ = image.shape
        # 获取label的尺寸
        label_width = label.width()
        label_height = label.height()
        # 计算缩放比例
        scale_w = label_width / w
        scale_h = label_height / h
        scale = min(scale_w, scale_h)  # 选择较小的比例以保持原始比例
        # 调整图片尺寸
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        # 将图片转换为QPixmap并设置为label的Pixmap
        h, w, _ = resized_image.shape
        bytes_per_line = 3 * w
        q_image = QImage(resized_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))






    def open1(self): #打开模块1
        self.stackedWidget.setCurrentIndex(0)


    def open2(self): #打开模块2
        self.stackedWidget.setCurrentIndex(1)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
