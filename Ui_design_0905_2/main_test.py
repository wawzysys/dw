import shutil
import sqlite3
import time
import os
import matlab.engine
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from PyQt5.QtChart import QChartView, QChart, QLineSeries, QBarSet, QBarSeries, QScatterSeries, QCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QMouseEvent, QImage, QPixmap, QPainter, QColor, QBrush, QFont, QPen
from PyQt5.QtWidgets import QWidget, QFileDialog
from Ui_main import Ui_MainWindow
from guding import a, b
import sys
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QLabel, QVBoxLayout
import logging
from figure1 import figure1
from figure2 import figure2

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
        '''=====================增加的3个按钮和显示===================='''
        self.btn_img_4.clicked.connect(self.show_img4)
        self.btn_img_3.clicked.connect(self.show_img3)
        self.btn_img_5.clicked.connect(self.show_img5)
        self.btn_img_6.clicked.connect(self.show_img6)
        self.btn_img_7.clicked.connect(self.show_img7)
        self.btn_img_8.clicked.connect(self.show_img8)

    def on_item_clicked(self, item):
        if item.text() == '负荷调控结果':
            path1 = r'C:\Users\19160\Desktop\dw\Figure1.png'
            self.label_9.clear()
            self.showImgInLabel(path1,self.label_9)
        elif item.text() == '节点边际电价':
            path2 = r'C:\Users\19160\Desktop\dw\Figure2.png'
            self.label_9.clear()
            self.showImgInLabel(path2, self.label_9)

    def on_item_clicked_2(self, item):
        if item.text() == '系统传输容量':
            path1 = r'C:\Users\19160\Desktop\dw\Figure4.png'
            self.label_10.clear()
            self.showImgInLabel(path1, self.label_10)
        elif item.text() == '新能源消纳率':
            path2 = r'C:\Users\19160\Desktop\dw\Figure3.png'
            self.label_10.clear()
            self.showImgInLabel(path2, self.label_10)
        elif item.text() == '消纳率响应前后对比':
            path3 = r'C:\Users\19160\Desktop\dw\Figure5.png'
            self.label_10.clear()
            self.showImgInLabel(path3, self.label_10)

    def showImgInLabel(self,img_path, label):
        # 使用OpenCV读取图片
        img = cv2.imread(img_path)
        if img is None:
            print("Error: Image could not be read.")
            return
        # 获取label的尺寸
        label_width = label.width()
        label_height = label.height()
        # 获取图片的原始尺寸
        img_height, img_width, _ = img.shape
        # 计算缩放比例
        scale = min(label_width / img_width, label_height / img_height)
        # 计算新的尺寸
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        # 调整图片大小
        resized_img = cv2.resize(img, (new_width, new_height))
        # 转换颜色空间从BGR到RGB
        rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        # 转换为QImage，然后QPixmap
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(label_width, label_height, Qt.KeepAspectRatio)
        # 在QLabel上显示图片
        label.setPixmap(QPixmap.fromImage(p))




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
        # function2 = 'key_line_yinshan'
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

    def show_img4(self):
        # 弹出文件选择框
        print("show_img4")
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '', 'Image files (*.png *.jpg)')
        if file_path:
            self.show_image_in_label(file_path, self.label_4)

    def show_img3(self):
        # 弹出文件选择框
        print("show_img3")
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '', 'Image files (*.png *.jpg)')
        if file_path:
            self.show_image_in_label(file_path, self.label_3)

    def show_img5(self):
        # 弹出文件选择框
        print("show_img5")
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '', 'Image files (*.png *.jpg)')
        if file_path:
            self.show_image_in_label(file_path, self.label_5)

    def show_img6(self):
        # 弹出文件选择框
        print("show_img6")
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '', 'Image files (*.png *.jpg)')
        if file_path:
            self.show_image_in_label(file_path, self.label_6)

    def show_img7(self):
        # 弹出文件选择框
        print("show_img7")
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '', 'Image files (*.png *.jpg)')
        if file_path:
            self.show_image_in_label(file_path, self.label_7)

    def show_img8(self):
        # 弹出文件选择框
        print("show_img8")
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '', 'Image files (*.png *.jpg)')
        if file_path:
            self.show_image_in_label(file_path, self.label_8)

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

        # 使用图片
        print("开始创建图表对象")
        chart = QChart()

        # 加载图片使用 OpenCV
        print("正在加载图片")
        img = cv2.imread(r"C:\Users\19160\Desktop\dw\Figure4.png")
        if img is None:
            print("加载图片失败，请检查路径")
            return
        else:
            print(f"图片加载成功，图片尺寸: {img.shape[1]} x {img.shape[0]}")

        # 将图片缩放到640x480
        target_width = 640
        target_height = 480
        print(f"正在缩放图片到 {target_width} x {target_height}")
        resized_img = cv2.resize(img, (target_width, target_height),
                                 interpolation=cv2.INTER_AREA)
        print(f"缩放后的图片尺寸: {resized_img.shape[1]} x {resized_img.shape[0]}")

        # 将颜色从BGR转换为RGB
        resized_img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        # 将 OpenCV 图像转换为 QImage
        height, width, channel = resized_img_rgb.shape
        bytes_per_line = 3 * width
        q_img = QImage(resized_img_rgb.data, width, height, bytes_per_line,
                       QImage.Format_RGB888)

        # 设置图表背景为缩放后的图片
        chart.setBackgroundBrush(QBrush(QPixmap.fromImage(q_img)))
        print("设置图表背景")

        # 创建图表视图，并将其设置为窗口的中心部件
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # 设置 chart_view 的固定大小为 640x480
        chart_view.setFixedSize(target_width, target_height)

        # 添加图表视图到布局
        if hasattr(self, 'verticalLayout_20'):
            print("找到布局 verticalLayout_20，添加视图")
            self.verticalLayout_20.addWidget(chart_view)
            self.verticalLayout_20.update()  # 强制刷新布局
            self.repaint()  # 刷新窗口，确保布局已经完成
        else:
            print("未找到 verticalLayout_20，确保您的窗口中有这个布局。")

        # 如果存在旧的视图，则删除
        if hasattr(self, 'current_chart_view') and self.current_chart_view:
            print("删除旧的图表视图")
            self.current_chart_view.deleteLater()

        # 更新当前视图
        self.current_chart_view = chart_view
        print("图表视图已更新")
        print(
            f"图表视图尺寸: {self.current_chart_view.size().width()} x {self.current_chart_view.size().height()}"
        )

        # file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'
        # if os.path.exists(file_path):

        #     # 加载 Figure 3 数据
        #     file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'
        #     figure4_data = pd.read_excel(file_path, sheet_name='Figure4')
        #     nodes_figure4 = figure4_data['节点编号']
        #     PP1 = figure4_data['消纳率']
        #     bus_r_labels_figure4 = figure4_data['节点名称']

        #     # 创建 QBarSet 并添加数据
        #     bar_set = QBarSet("消纳率")
        #     bar_set.append(PP1.tolist())

        #     # 创建 QBarSeries 并将 QBarSet 添加进去
        #     bar_series = QBarSeries()
        #     bar_series.append(bar_set)
        #     bar_series.setBarWidth(0.9)
        #     bar_set.setColor(QColor("blue"))
        #     bar_set.setBorderColor(QColor("black"))

        #     # 创建图表对象
        #     chart = QChart()
        #     chart.addSeries(bar_series)
        #     chart.setTitle("新能源消纳率")
        #     chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色
        #     chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色
        #     chart.legend().setVisible(False)  # 隐藏图例（如果只显示一组数据）

        #     # 设置 X 轴
        #     axisX = QCategoryAxis()
        #     for i, label in enumerate(bus_r_labels_figure4):
        #         axisX.append(label, nodes_figure4[i])
        #     axisX.setLabelsAngle(45)
        #     axisX.setTitleText("节点编号")
        #     axisX.setTitleBrush(QColor("green"))
        #     axisX.setLabelsBrush(QColor("green"))
        #     chart.addAxis(axisX, Qt.AlignBottom)
        #     bar_series.attachAxis(axisX)

        #     # 设置 Y 轴
        #     axisY = QValueAxis()
        #     axisY.setTitleText("消纳率/%")
        #     axisY.setTitleBrush(QColor("green"))
        #     axisY.setLabelsBrush(QColor("green"))
        #     axisY.setRange(0, max(PP1) + 5)
        #     chart.addAxis(axisY, Qt.AlignLeft)
        #     bar_series.attachAxis(axisY)
        # else:
        #     print("文件不存在，采用示例图片")
        #     # 创建一个折线系列并添加数据
        #     series = QLineSeries()
        #     series.append(0, 6.1)
        #     series.append(1, 6.5)
        #     series.append(2, 6.3)
        #     series.append(3, 6.2)
        #     series.append(4, 6.1)
        #     series.append(5, 6.4)
        #     series.append(6, 6.3)
        #     series.append(7, 6.2)
        #     series.append(8, 6.5)
        #     series.append(9, 6.8)
        #     series.setColor(QColor(255, 0, 0))
        #     #
        #     series1 = QLineSeries()
        #     series1.append(0, 5.6)
        #     series1.append(1, 6.8)
        #     series1.append(2, 5.7)
        #     series1.append(3, 6.3)
        #     series1.append(4, 6.1)
        #     series1.append(5, 5.9)
        #     series1.append(6, 6.2)
        #     series1.append(7, 6.8)
        #     series1.append(8, 6.4)
        #     series1.append(9, 6.0)
        #     series1.setColor(QColor(0, 0, 255))

        #     # 创建图表对象，并添加系列
        #     chart = QChart()
        #     chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色
        #     chart.legend().setFont(QFont("SansSerif", 10, QFont.Bold))
        #     chart.legend().setLabelColor(QColor(0, 255, 0))  # 设置图例文字颜色为绿色
        #     chart.setTitle("示例动态图形")
        #     chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色
        #     chart.legend().show()
        #     chart.addSeries(series)
        #     chart.addSeries(series1)
        #     chart.createDefaultAxes()
        #     # 设置坐标轴颜色（这里以X轴为例）
        #     chart.axisX().setTitleText("X坐标轴")
        #     chart.axisX().setTitleBrush(QBrush(QColor(0, 255,
        #                                               0)))  # 设置X轴标题文字颜色为绿色
        #     chart.axisX().setGridLineVisible(True)
        #     chart.axisX().setGridLineColor(QColor(0, 255,
        #                                           0))  # 设置X轴网格线颜色为绿色（可选）
        #     chart.axisY().setTitleText("Y坐标轴")
        #     chart.axisY().setTitleBrush(QBrush(QColor(0, 255,
        #                                               0)))  # 设置Y轴标题文字颜色为绿色
        #     chart.axisY().setGridLineVisible(True)
        #     chart.axisY().setGridLineColor(QColor(0, 255,
        #                                           0))  # 设置Y轴网格线颜色为绿色（可选）

        # 创建图表视图，并将其设置为窗口的中心部件
        # if self.current_chart_view:
        #     self.verticalLayout_9.removeWidget(self.current_chart_view)
        #     self.current_chart_view.deleteLater()
        # self.current_chart_view = QChartView(chart)
        # self.current_chart_view.setRenderHint(QPainter.Antialiasing)
        # self.verticalLayout_20.addWidget(self.current_chart_view)

    def show_example_drawing_4(self):
        # 种类1
        # 加载数据
        # file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'
        # figure5_SL_data = pd.read_excel(file_path, sheet_name='Figure5_SL')
        # figure5_SLmax_data = pd.read_excel(file_path,
        #                                    sheet_name='Figure5_SLmax')
        # figure5_key_l_data = pd.read_excel(file_path,
        #                                    sheet_name='Figure5_key_l')

        # nodes_figure5 = figure5_SL_data['线路编号']
        # SL = figure5_SL_data['传输容量']
        # SLmax = figure5_SLmax_data['容量限值']
        # key_l = figure5_key_l_data['关键线路编号']
        # key_l_SL = figure5_key_l_data['关键线路容量']
        # branch_labels = figure5_SL_data['线路名称']

        # # 创建图表对象
        # chart = QChart()
        # chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色
        # chart.setTitle("系统线路传输容量")
        # chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色

        # # 创建线路传输容量的折线系列
        # line_series_SL = QLineSeries()
        # line_series_SL.setName("线路传输容量")
        # for i, val in enumerate(SL):
        #     line_series_SL.append(nodes_figure5[i], val)
        # line_series_SL.setColor(QColor("blue"))

        # # 创建线路容量限值的折线系列
        # line_series_SLmax = QLineSeries()
        # line_series_SLmax.setName("线路容量限值")
        # for i, val in enumerate(SLmax):
        #     line_series_SLmax.append(nodes_figure5[i], val)
        # line_series_SLmax.setColor(QColor("red"))
        # line_series_SLmax.setPen(QColor("red"))

        # # 创建关键线路的散点系列
        # scatter_series_key_l = QScatterSeries()
        # scatter_series_key_l.setName("关键线路")
        # scatter_series_key_l.setMarkerSize(10)
        # for i, val in enumerate(key_l_SL):
        #     scatter_series_key_l.append(key_l[i], val)
        # scatter_series_key_l.setColor(QColor("red"))

        # # 将系列添加到图表中
        # chart.addSeries(line_series_SL)
        # chart.addSeries(line_series_SLmax)
        # chart.addSeries(scatter_series_key_l)

        # # 创建 X 轴
        # axisX = QCategoryAxis()
        # for i, label in enumerate(branch_labels):
        #     axisX.append(label, nodes_figure5[i])
        # axisX.setLabelsAngle(45)
        # axisX.setTitleText("线路编号")
        # axisX.setTitleBrush(QColor("green"))
        # axisX.setLabelsBrush(QColor("green"))
        # chart.addAxis(axisX, Qt.AlignBottom)
        # line_series_SL.attachAxis(axisX)
        # line_series_SLmax.attachAxis(axisX)
        # scatter_series_key_l.attachAxis(axisX)

        # # 创建 Y 轴
        # axisY = QValueAxis()
        # axisY.setTitleText("S(MVA)")
        # axisY.setTitleBrush(QColor("green"))
        # axisY.setLabelsBrush(QColor("green"))
        # chart.addAxis(axisY, Qt.AlignLeft)
        # line_series_SL.attachAxis(axisY)
        # line_series_SLmax.attachAxis(axisY)
        # scatter_series_key_l.attachAxis(axisY)

        # # 设置图例
        # chart.legend().setFont(QFont("SansSerif", 10, QFont.Bold))
        # chart.legend().setLabelColor(QColor(0, 255, 0))  # 设置图例文字颜色为绿色
        # chart.legend().setBackgroundVisible(False)  # 隐藏图例背景
        # 种类2
        # 加载数据
        file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'
        if os.path.exists(file_path):
            font = QFont("SimSun", 12)  # 可以根据需要调整字体和大小
            font.setBold(True)  # 设置字体为加粗
            figure5_SL_data = pd.read_excel(file_path, sheet_name='Figure5_SL')
            figure5_SLmax_data = pd.read_excel(file_path,
                                               sheet_name='Figure5_SLmax')
            figure5_key_l_data = pd.read_excel(file_path,
                                               sheet_name='Figure5_key_l')

            nodes_figure5 = figure5_SL_data['线路编号']
            SL = figure5_SL_data['传输容量']
            SLmax = figure5_SLmax_data['容量限值']
            key_l = figure5_key_l_data['关键线路编号']
            key_l_SL = figure5_key_l_data['关键线路容量']
            # 创建图表对象
            chart = QChart()
            chart.setTitle("系统线路传输容量")
            chart.setTitleFont(font)  # 设置标题字体
            chart.setTitleBrush(QBrush(QColor(255, 255, 255)))  # 设置标题文字颜色为绿色
            chart.setBackgroundBrush(QColor("black"))  # 设置背景为黑色
            chart.legend().setLabelColor(QColor(255, 255, 255))  # 设置图例文字颜色为绿色
            chart.legend().setFont(QFont("SimSum", 10, QFont.Bold))

            # 创建并添加线路传输容量的折线系列
            line_series_SL = QLineSeries()
            line_series_SL.setName("线路传输容量")
            for i, val in enumerate(SL):
                line_series_SL.append(nodes_figure5[i], val)
            pen = QPen(QColor(22, 206, 184))  # 设置颜色
            pen.setWidth(3)  # 设置线的宽度为3，数值越大线越粗
            line_series_SL.setPen(pen)
            # line_series_SL.setColor(QColor(22, 206, 184))

            # 创建并添加线路容量限值的折线系列
            line_series_SLmax = QLineSeries()
            line_series_SLmax.setName("线路容量限值")
            for i, val in enumerate(SLmax):
                line_series_SLmax.append(nodes_figure5[i], val)
            pen = QPen(QColor(255, 161, 109))  # 设置颜色
            pen.setWidth(3)  # 设置线的宽度为3，数值越大线越粗
            line_series_SLmax.setPen(pen)
            # line_series_SLmax.setColor(QColor(255, 161, 109))

            # 创建并添加关键线路的散点系列
            scatter_series_key_l = QScatterSeries()
            scatter_series_key_l.setName("关键线路")
            scatter_series_key_l.setMarkerSize(10)
            for i, val in enumerate(key_l_SL):
                scatter_series_key_l.append(key_l[i], val)
            scatter_series_key_l.setColor(QColor(255, 161, 109))

            # 添加系列到图表
            chart.addSeries(line_series_SL)
            chart.addSeries(line_series_SLmax)
            chart.addSeries(scatter_series_key_l)

            # 创建坐标轴并设置标签
            chart.createDefaultAxes()
            chart.axisX().setTitleText("线路编号")
            chart.axisX().setTitleBrush(QColor("white"))
            chart.axisX().setLabelsBrush(QColor("white"))
            chart.axisY().setTitleText("S(MVA)")
            chart.axisY().setTitleBrush(QColor("white"))
            chart.axisY().setLabelsBrush(QColor("white"))
        else:
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
            chart.axisX().setTitleBrush(QBrush(QColor(0, 255,
                                                      0)))  # 设置X轴标题文字颜色为绿色
            chart.axisY().setTitleText("Y坐标轴")
            chart.axisY().setTitleBrush(QBrush(QColor(0, 255,
                                                      0)))  # 设置Y轴标题文字颜色为绿色

            # 设置图例
            chart.legend().setFont(QFont("SansSerif", 10, QFont.Bold))
            chart.legend().setLabelColor(QColor(0, 255, 0))  # 设置图例文字颜色为绿色
            chart.legend().show()
        # 示例
        # # 设置图像路径
        # image_path = r'C:\Users\19160\Desktop\dw\Figure4.png'

        # # 使用 OpenCV 读取图片
        # image = cv2.imread(image_path)

        # # 改变图片大小，例如宽度设置为800，高度设置为600
        # resized_image = cv2.resize(image, (800, 760))

        # # 将图片从BGR格式转换为RGB格式
        # resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        # # 将OpenCV的图像转换为QImage
        # height, width, channel = resized_image.shape
        # bytes_per_line = 3 * width
        # qimage = QImage(resized_image.data, width, height, bytes_per_line,
        #                 QImage.Format_RGB888)

        # # 将QImage转换为QPixmap
        # pixmap = QPixmap(qimage)

        # # 创建一个 QLabel 来显示图片
        # label = QLabel(self)
        # label.setPixmap(pixmap)

        # # 如果之前有图表视图，先移除它
        # if self.current_chart_view:
        #     self.verticalLayout_9.removeWidget(self.current_chart_view)
        #     self.current_chart_view.deleteLater()

        # # 更新 current_chart_view 为新建的 QLabel
        # self.current_chart_view = label

        # # 将 QLabel 添加到布局中
        # self.verticalLayout_21.addWidget(self.current_chart_view)

        # # 确保图片显示正常
        # self.current_chart_view.setScaledContents(True)

        # 创建一个柱状图系列并添加数据
        # set0 = QBarSet("检测值")
        # set0 << 2 << 4 << 3 << 4 << 1 << 6

        # series = QBarSeries()
        # series.append(set0)

        if self.current_chart_view:
            self.verticalLayout_9.removeWidget(self.current_chart_view)
            self.current_chart_view.deleteLater()
        # 创建图表视图，并将其设置为窗口的中心部件
        self.current_chart_view = QChartView(chart)
        self.current_chart_view.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout_21.addWidget(self.current_chart_view)

    def show_example_drawing5(self):

        # 加载数据
        file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'
        if os.path.exists(file_path):
            font = QFont("SimSun", 12)  # 可以根据需要调整字体和大小
            font.setBold(True)  # 设置字体为加粗
            figure6_PP1_PPP_data = pd.read_excel(file_path,
                                                 sheet_name='Figure6_PP1_PPP')
            nodes_figure6_PP1_PPP = figure6_PP1_PPP_data['节点编号']
            PP1_figure6 = figure6_PP1_PPP_data['响应前消纳率']
            PPP = figure6_PP1_PPP_data['响应后消纳率']
            bus_r_labels_figure6 = figure6_PP1_PPP_data['节点名称']

            # 创建 QBarSet 并添加数据
            bar_set_PP1 = QBarSet("响应前")
            bar_set_PP1.append(PP1_figure6.tolist())

            bar_set_PPP = QBarSet("响应后")
            bar_set_PPP.append(PPP.tolist())

            # 创建 QBarSeries 并将 QBarSet 添加进去
            bar_series = QBarSeries()
            bar_series.append(bar_set_PP1)
            bar_series.append(bar_set_PPP)

            # 设置颜色
            bar_set_PP1.setColor(QColor(22, 206, 184))
            bar_set_PP1.setBorderColor(QColor("black"))
            bar_set_PPP.setColor(QColor(255, 161, 109))
            bar_set_PPP.setBorderColor(QColor("black"))

            # 创建图表对象
            chart = QChart()
            chart.addSeries(bar_series)
            chart.setTitleFont(font)
            chart.setTitle("新能源消纳率前后对比")
            chart.setTitleBrush(QBrush(QColor(255, 255, 255)))  # 设置标题文字颜色为绿色
            chart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))  # 设置背景为黑色
            chart.legend().setFont(QFont("SimSum", 10, QFont.Bold))
            chart.legend().setLabelColor(QColor(255, 255, 255))  # 设置图例文字颜色为绿色
            chart.legend().setBackgroundVisible(False)  # 隐藏图例背景

            # 设置 X 轴
            axisX = QCategoryAxis()

            # 计算步长，确保不会除以零
            label_count = len(bus_r_labels_figure6)
            step = max(1, label_count // 10)  # 至少为1，避免除以0

            for i, label in enumerate(bus_r_labels_figure6):
                if i % step == 0:  # 每隔step个标签显示一次
                    axisX.append(label, nodes_figure6_PP1_PPP[i])

            axisX.setLabelsAngle(60)  # 增加标签角度以减少重叠

            axisX.setTitleText("节点编号")
            axisX.setTitleFont(font)
            axisX.setTitleBrush(QColor(255, 255, 255))
            axisX.setLabelsBrush(QColor(255, 255, 255))
            chart.addAxis(axisX, Qt.AlignBottom)
            bar_series.attachAxis(axisX)

            # 设置 Y 轴
            axisY = QValueAxis()
            axisY.setTitleText("消纳率/%")
            axisX.setTitleFont(font)
            axisY.setTitleBrush(QColor(255, 255, 255))
            axisY.setLabelsBrush(QColor(255, 255, 255))
            axisY.setRange(0, max(PPP.max(), PP1_figure6.max()) + 5)
            chart.addAxis(axisY, Qt.AlignLeft)
            bar_series.attachAxis(axisY)
        else:
            print("文件不存在，采用示例数据")
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
            chart.setTitle("示例动态图形5")
            chart.setTitleBrush(QBrush(QColor(0, 255, 0)))  # 设置标题文字颜色为绿色
            chart.legend().show()
            chart.addSeries(series)
            chart.addSeries(series1)
            chart.createDefaultAxes()
            # 设置坐标轴颜色（这里以X轴为例）
            chart.axisX().setTitleText("X坐标轴")
            chart.axisX().setTitleBrush(QBrush(QColor(0, 255,
                                                      0)))  # 设置X轴标题文字颜色为绿色
            chart.axisX().setGridLineVisible(True)
            chart.axisX().setGridLineColor(QColor(0, 255,
                                                  0))  # 设置X轴网格线颜色为绿色（可选）
            chart.axisY().setTitleText("Y坐标轴")
            chart.axisY().setTitleBrush(QBrush(QColor(0, 255,
                                                      0)))  # 设置Y轴标题文字颜色为绿色
            chart.axisY().setGridLineVisible(True)
            chart.axisY().setGridLineColor(QColor(0, 255,
                                                  0))  # 设置Y轴网格线颜色为绿色（可选）

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
