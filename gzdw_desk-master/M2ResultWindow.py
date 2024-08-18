from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow


class M2ResultWindow(QMainWindow): #运行评估结果界面
    def __init__(self,gzdw_data):
        super().__init__()
        self.gzdw_data = gzdw_data
        self.setGeometry(100, 100, 800,500)
        self.img_DLMP = './DLMPs_'+gzdw_data+'.png'
        self.img_Loadshedding = './Loadshedding_'+gzdw_data+'.png'
        self.init_ui()
    def init_ui(self):
        self.ui = uic.loadUi("./M2ResultWindow.ui",self)


        self.comboBox = self.ui.comboBox_M2Result


        self.label1 = self.ui.r_p1

        self.r_run1_f() # 默认显示 节点边际电价

        self.comboBox.currentIndexChanged.connect(
                            lambda: self.choose_result_image(self.comboBox.currentText()))



    def choose_result_image(self,text):
        #print(text)
        if(text == "负荷调控结果"):
            self.r_run2_f()
        elif(text == "节点边际电价"):
            self.r_run1_f()


    def r_run1_f(self): #图片 节点边际电价
        print(self.img_DLMP)
        pixmap = QPixmap(self.img_DLMP)
        self.label1.setPixmap(pixmap)
        self.label1.setScaledContents(True)

    def r_run2_f(self): #图片 负荷调控结果
        print(self.img_Loadshedding)
        pixmap = QPixmap(self.img_Loadshedding)
        self.label1.setPixmap(pixmap)
        self.label1.setScaledContents(True)