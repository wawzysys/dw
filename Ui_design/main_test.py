import shutil
import sqlite3
import time
import os
import matlab.engine
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from PyQt5.QtChart import QChartView, QChart, QLineSeries, QBarSet, QBarSeries
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QMouseEvent, QImage, QPixmap, QPainter, QColor, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QFileDialog
from Ui_main import Ui_MainWindow
from guding import a, b
import sys
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题


class MatlabWorker(QThread):

    def __init__(self, function):
        super().__init__()
        self.function = function

    def run(self):
        self.function()


class myWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.current_chart_view = None
        self.resize(1450, 950)
        # 设置按钮的点击事件
        self.btn_max.clicked.connect(self.maximize_window)
        self.btn_min.clicked.connect(self.minimize_window)
        self.btn_close.clicked.connect(self.close)
        #显示示例图形
        # self.show_example_drawing()
        # self.show_example_drawing2()
        #stackWidget切换
        self.pushButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_2.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        #复制文件
        self.btn_load_1.clicked.connect(self.copy_file1)
        self.btn_load_2.clicked.connect(self.copy_file2)
        #显示图像
        self.btn_img_1.clicked.connect(self.show_img1)
        self.btn_img_2.clicked.connect(self.show_img2)
        #预留接口
        self.btn_predict_1.clicked.connect(self.run_pred_1)
        self.btn_predict_2.clicked.connect(self.run_pred_2)

        # 连接itemClicked信号到槽函数
        self.listWidget.itemClicked.connect(self.on_item_clicked)
        self.listWidget_2.itemClicked.connect(self.on_item_clicked_2)

    def on_item_clicked(self, item):
        if item.text() == '负荷调控结果':
            self.show_example_drawing()
            print('a')
        elif item.text() == '节点边际电价':
            self.show_example_drawing2()
            print('b')

    def on_item_clicked_2(self, item):
        if item.text() == '系统传输容量':
            self.show_example_drawing_3()
            print('c')
        elif item.text() == '新能源消纳率':
            self.show_example_drawing_4()
            print('d')
        elif item.text() == '消纳率响应前后对比':
            self.show_example_drawing5()
            print('e')

    def pred_1(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        #更改路径
        relative_matlab_path = '../guizhou0714'
        absolute_matlab_path = os.path.join(current_dir, relative_matlab_path)
        eng = matlab.engine.start_matlab()
        print("开始运行1")
        eng.addpath(absolute_matlab_path, nargout=0)
        #执行脚本
        function1 = 'main'
        eng.run(function1, nargout=0)
        print("预留接口1")

    def pred_2(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        #更改路径即可
        relative_matlab_path = '../gzdw_desk-master/matlab_lib/code_shiji'
        # C:\Users\19160\Desktop\dw\gzdw_desk-master\matlab_lib\code_shiji\key_line_xinyi.m
        absolute_matlab_path = os.path.join(current_dir, relative_matlab_path)
        eng = matlab.engine.start_matlab()
        eng.addpath(absolute_matlab_path, nargout=0)
        print("开始运行2")
        #更改脚本名字
        function2 = 'key_line_xinyi'
        # 执行脚本
        eng.run(function2, nargout=0)
        # eng.main(nargout=0)
        print("预留接口2")

    def run_pred_1(self):
        self.thread_1 = MatlabWorker(self.pred_1)
        self.thread_1.start()

    def run_pred_2(self):
        self.thread_2 = MatlabWorker(self.pred_2)
        self.thread_2.start()

    def show_img1(self):
        # 弹出文件选择框
        print("show_img1")
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '', 'Image files (*.png *.jpg)')
        if file_path:
            self.show_image_in_label(file_path, self.label_image_1)

    def show_img2(self):
        print("show_img2")
        # 弹出文件选择框
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '', 'Image files (*.png *.jpg)')
        if file_path:
            self.show_image_in_label(file_path, self.label_image_2)

    def show_image_in_label(self, path, label):
        print("show_image_in_label")
        # 使用OpenCV读取图片
        frame = cv2.imread(path)
        if frame is None:
            print(f"Error: Unable to load image at {path}")
            return
        # 获取标签的尺寸
        label_width = label.width()
        label_height = label.height()
        # 计算缩放比例以保持图像的宽高比
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]
        frame_ratio = frame_width / frame_height
        label_ratio = label_width / label_height
        if frame_ratio > label_ratio:
            # 如果图像的宽高比大于标签的宽高比，则根据标签的高度来计算新的宽度
            new_width = int(label_height * frame_ratio)
            new_height = label_height
        else:
            # 否则，根据标签的宽度来计算新的高度
            new_width = label_width
            new_height = int(label_width / frame_ratio)
            # 调整图像大小
        frame = cv2.resize(frame, (new_width, new_height))
        print("original:", frame.shape[0], frame.shape[1])
        # 视频色彩转换为RGB，因为OpenCV默认使用BGR格式
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 将numpy数组转换为QImage
        qImage = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0],
                              frame.strides[0], QtGui.QImage.Format_RGB888)
        # 在标签中显示QImage，保持长宽比例
        pixmap = QtGui.QPixmap.fromImage(qImage)
        label.setPixmap(
            pixmap.scaled(label_width, label_height,
                          QtCore.Qt.KeepAspectRatio))

    def copy_file1(self):
        # 弹出文件选择框
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '',
                                                   'All Files (*)')
        if file_path:
            # 目标目录
            target_dir = './copy_file_path'
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # 构造新的文件名
            file_name = os.path.basename(file_path)
            # new_file_name = f'copy_{file_name}'
            new_file_name = f'gzdw_data1'
            target_path = os.path.join(target_dir, new_file_name)
            # 复制文件
            shutil.copy(file_path, target_path)
        print("copy_file1")

    def copy_file2(self):
        # 弹出文件选择框
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '',
                                                   'All Files (*)')
        if file_path:
            # 目标目录
            target_dir = './copy_file_path_2'
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

                # 构造新的文件名
            file_name = os.path.basename(file_path)
            # new_file_name = f'copy_{file_name}'
            new_file_name = f'gzdw_data2'
            target_path = os.path.join(target_dir, new_file_name)
            # 复制文件
            shutil.copy(file_path, target_path)
        print("copy_file2")

    def show_example_drawing(self):
        # 创建一个折线系列并添加数据
        series = QLineSeries()
        series.append(0, 6.1)
        series.append(1, 6.5)
        series.append(2, 6.3)
        series.append(3, 6.2)
        series.append(4, 6.1)
        series.append(5, 6.4)
        series.append(6, 6.3)
        series.append(7, 6.2)
        series.append(8, 6.5)
        series.append(9, 6.8)
        series.setColor(QColor(255, 0, 0))
        #
        series1 = QLineSeries()
        series1.append(0, 5.6)
        series1.append(1, 6.8)
        series1.append(2, 5.7)
        series1.append(3, 6.3)
        series1.append(4, 6.1)
        series1.append(5, 5.9)
        series1.append(6, 6.2)
        series1.append(7, 6.8)
        series1.append(8, 6.4)
        series1.append(9, 6.0)
        series1.setColor(QColor(0, 0, 255))

        # 创建图表对象，并添加系列
        chart = QChart()
        chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色
        chart.legend().setFont(QFont("SansSerif", 10, QFont.Bold))
        chart.legend().setLabelColor(QColor(0, 255, 0))  # 设置图例文字颜色为绿色
        chart.setTitle("示例动态图形")
        chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色
        chart.legend().show()
        chart.addSeries(series)
        chart.addSeries(series1)
        chart.createDefaultAxes()
        # 设置坐标轴颜色（这里以X轴为例）
        chart.axisX().setTitleText("X坐标轴")
        chart.axisX().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置X轴标题文字颜色为绿色
        chart.axisX().setGridLineVisible(True)
        chart.axisX().setGridLineColor(QColor(0, 255, 0))  # 设置X轴网格线颜色为绿色（可选）
        chart.axisY().setTitleText("Y坐标轴")
        chart.axisY().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置Y轴标题文字颜色为绿色
        chart.axisY().setGridLineVisible(True)
        chart.axisY().setGridLineColor(QColor(0, 255, 0))  # 设置Y轴网格线颜色为绿色（可选）
        # 创建图表视图，并将其设置为窗口的中心部件
        # 创建或更新图表视图
        if self.current_chart_view:
            self.verticalLayout_9.removeWidget(self.current_chart_view)
            self.current_chart_view.deleteLater()
        # 删除旧视图释放资源
        self.current_chart_view = QChartView(chart)
        self.current_chart_view.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout_9.addWidget(self.current_chart_view)

    def show_example_drawing2(self):
        # 创建一个柱状图系列并添加数据
        set0 = QBarSet("检测值")
        set0 << 2 << 4 << 3 << 4 << 1 << 6

        series = QBarSeries()
        series.append(set0)

        # 创建图表对象，并添加系列
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("示例柱状图")
        chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色
        chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色

        # 设置坐标轴
        chart.createDefaultAxes()
        chart.axisX().setTitleText("X坐标轴")
        chart.axisX().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置X轴标题文字颜色为绿色
        chart.axisY().setTitleText("Y坐标轴")
        chart.axisY().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置Y轴标题文字颜色为绿色

        # 设置图例
        chart.legend().setFont(QFont("SansSerif", 10, QFont.Bold))
        chart.legend().setLabelColor(QColor(0, 255, 0))  # 设置图例文字颜色为绿色
        chart.legend().show()
        if self.current_chart_view:
            self.verticalLayout_9.removeWidget(self.current_chart_view)
            self.current_chart_view.deleteLater()
        # 创建图表视图，并将其设置为窗口的中心部件
        self.current_chart_view = QChartView(chart)
        self.current_chart_view.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout_10.addWidget(self.current_chart_view)

    def show_example_drawing_3(self):
        # 创建一个折线系列并添加数据
        series = QLineSeries()
        series.append(0, 6.1)
        series.append(1, 6.5)
        series.append(2, 6.3)
        series.append(3, 6.2)
        series.append(4, 6.1)
        series.append(5, 6.4)
        series.append(6, 6.3)
        series.append(7, 6.2)
        series.append(8, 6.5)
        series.append(9, 6.8)
        series.setColor(QColor(255, 0, 0))
        #
        series1 = QLineSeries()
        series1.append(0, 5.6)
        series1.append(1, 6.8)
        series1.append(2, 5.7)
        series1.append(3, 6.3)
        series1.append(4, 6.1)
        series1.append(5, 5.9)
        series1.append(6, 6.2)
        series1.append(7, 6.8)
        series1.append(8, 6.4)
        series1.append(9, 6.0)
        series1.setColor(QColor(0, 0, 255))

        # 创建图表对象，并添加系列
        chart = QChart()
        chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色
        chart.legend().setFont(QFont("SansSerif", 10, QFont.Bold))
        chart.legend().setLabelColor(QColor(0, 255, 0))  # 设置图例文字颜色为绿色
        chart.setTitle("示例动态图形")
        chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色
        chart.legend().show()
        chart.addSeries(series)
        chart.addSeries(series1)
        chart.createDefaultAxes()
        # 设置坐标轴颜色（这里以X轴为例）
        chart.axisX().setTitleText("X坐标轴")
        chart.axisX().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置X轴标题文字颜色为绿色
        chart.axisX().setGridLineVisible(True)
        chart.axisX().setGridLineColor(QColor(0, 255, 0))  # 设置X轴网格线颜色为绿色（可选）
        chart.axisY().setTitleText("Y坐标轴")
        chart.axisY().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置Y轴标题文字颜色为绿色
        chart.axisY().setGridLineVisible(True)
        chart.axisY().setGridLineColor(QColor(0, 255, 0))  # 设置Y轴网格线颜色为绿色（可选）

        # 创建图表视图，并将其设置为窗口的中心部件
        if self.current_chart_view:
            self.verticalLayout_9.removeWidget(self.current_chart_view)
            self.current_chart_view.deleteLater()
        self.current_chart_view = QChartView(chart)
        self.current_chart_view.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout_20.addWidget(self.current_chart_view)

    def show_example_drawing_4(self):
        # 创建一个柱状图系列并添加数据
        set0 = QBarSet("检测值")
        set0 << 2 << 4 << 3 << 4 << 1 << 6

        series = QBarSeries()
        series.append(set0)

        # 创建图表对象，并添加系列
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("示例柱状图")
        chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色
        chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色

        # 设置坐标轴
        chart.createDefaultAxes()
        chart.axisX().setTitleText("X坐标轴")
        chart.axisX().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置X轴标题文字颜色为绿色
        chart.axisY().setTitleText("Y坐标轴")
        chart.axisY().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置Y轴标题文字颜色为绿色

        # 设置图例
        chart.legend().setFont(QFont("SansSerif", 10, QFont.Bold))
        chart.legend().setLabelColor(QColor(0, 255, 0))  # 设置图例文字颜色为绿色
        chart.legend().show()
        if self.current_chart_view:
            self.verticalLayout_9.removeWidget(self.current_chart_view)
            self.current_chart_view.deleteLater()
        # 创建图表视图，并将其设置为窗口的中心部件
        self.current_chart_view = QChartView(chart)
        self.current_chart_view.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout_21.addWidget(self.current_chart_view)

    def show_example_drawing5(self):
        # 创建一个柱状图系列并添加数据
        set0 = QBarSet("检测值")
        set0 << 2 << 4 << 3 << 4 << 1 << 6

        series = QBarSeries()
        series.append(set0)

        # 创建图表对象，并添加系列
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("示例柱状图")
        chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色
        chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色

        # 设置坐标轴
        chart.createDefaultAxes()
        chart.axisX().setTitleText("X坐标轴")
        chart.axisX().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置X轴标题文字颜色为绿色
        chart.axisY().setTitleText("Y坐标轴")
        chart.axisY().setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置Y轴标题文字颜色为绿色

        # 设置图例
        chart.legend().setFont(QFont("SansSerif", 10, QFont.Bold))
        chart.legend().setLabelColor(QColor(0, 255, 0))  # 设置图例文字颜色为绿色
        chart.legend().show()
        if self.current_chart_view:
            self.verticalLayout_9.removeWidget(self.current_chart_view)
            self.current_chart_view.deleteLater()
        # 创建图表视图，并将其设置为窗口的中心部件
        self.current_chart_view = QChartView(chart)
        self.current_chart_view.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout_21.addWidget(self.current_chart_view)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if (event.buttons() & Qt.LeftButton) and self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_pos = None

    def maximize_window(self):
        self.showMaximized()

    def minimize_window(self):
        self.showMinimized()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test = myWindow()
    test.showMaximized()
    sys.exit(app.exec_())
