import sys

import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from ui_try import Ui_Form


class QmyMainWindow(QWidget):
   def __init__(self, parent=None):
      super().__init__(parent)   #调用父类构造函数，创建窗体
      self.ui=Ui_Form()    #创建UI对象
      self.ui.setupUi(self)      #构造UI界面

      path='lllllllll.jpg'
      self.resize_image_to_fit_label(path,self.ui.label)

   def resize_image_to_fit_label(self,image_path, label):
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


if  __name__ == "__main__":        #用于当前窗体测试
   app = QApplication(sys.argv)    #创建GUI应用程序
   form=QmyMainWindow()            #创建窗体
   form.show()
   sys.exit(app.exec_())