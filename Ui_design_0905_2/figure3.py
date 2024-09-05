import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import numpy as np
from PIL import Image  # 引入PIL库
def figure3():
    # 设置字体
    rcParams['font.family'] = 'SimHei'
    rcParams['axes.unicode_minus'] = False  # 正确显示负号
    
    # 读取Excel文件
    file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'
    # file_path = r'C:\Users\19160\Desktop\dw\plot_data.xlsx'

    # Figure 3 数据
    figure4_data = pd.read_excel(file_path, sheet_name='Figure4')
    nodes_figure4 = figure4_data['节点编号']
    PP1 = figure4_data['消纳率']
    bus_r_labels_figure4 = figure4_data['节点名称']

    # 绘制 Figure 3: 新能源消纳率图
    plt.figure(dpi=200, facecolor='black')  # 指定图像大小和DPI
    bars = plt.bar(nodes_figure4, PP1, color='blue', edgecolor='black')
    plt.xlabel('节点编号', fontsize=12, color='white')
    plt.ylabel('消纳率/%', fontsize=12, color='white')
    plt.title('银山新能源消纳率', fontsize=14, color='white')
    plt.xticks(nodes_figure4, bus_r_labels_figure4, rotation=45, fontsize=10, color='white')
    plt.yticks(fontsize=10, color='white')
    plt.grid(True, linestyle='-', alpha=0.7, color='white')
    plt.gca().set_facecolor('black')

    # 在柱状图上添加数值标签
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2,
                 yval + 1,
                 f'{yval:.2f}%',
                 ha='center',
                 va='bottom',
                 fontsize=10,
                 color='white')
        # 设置边框颜色
    ax = plt.gca()
    ax.set_facecolor('black')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    plt.legend(['消纳率'], fontsize=10, loc='upper left', facecolor='black', edgecolor='black', labelcolor='white')
    plt.subplots_adjust(bottom=0.2)  # 调整底部边距以防止截断
    plt.savefig('Figure3.png', dpi=200, facecolor='black')  # 保存文件
    plt.show()
    img = Image.open('Figure1.png')
    print("Image Size: ", img.size)  # 输出图像的尺寸
    img_data = np.array(img)
    print("Image Array Shape: ", img_data.shape)  # 输出图像数组的形状

figure3()
