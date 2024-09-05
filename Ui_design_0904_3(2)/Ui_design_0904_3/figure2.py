# 读取数据，指定没有列名(header=None)，并且直接使用数字索引列
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from matplotlib.font_manager import FontProperties
from PIL import Image  # 引入PIL库
# Image Size:  (1531, 1237)
# Image Array Shape:  (1237, 1531, 4)
def figure2():
    file_path = r'C:\Users\19160\Desktop\dw\DLMPs.xlsx'
    # 读取Excel文件
    df = pd.read_excel(file_path, header=None)

    # 将DataFrame转换为numpy数组
    data = df.to_numpy()

    # 创建原始x, y坐标网格
    x = np.arange(data.shape[1])
    y = np.arange(data.shape[0])
    x, y = np.meshgrid(x, y)

    # 设置插值网格
    x_new = np.linspace(x.min(), x.max(), 300)
    y_new = np.linspace(y.min(), y.max(), 300)
    x_new, y_new = np.meshgrid(x_new, y_new)

    # 对原始数据进行插值
    z_new = griddata((x.flatten(), y.flatten()),
                     data.flatten(), (x_new, y_new),
                     method='cubic')

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 创建一个图形和一个三维轴
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 设置图形和轴的背景颜色
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')

    # 绘制曲面图
    surf = ax.plot_surface(x_new, y_new, z_new, cmap='jet', edgecolor='none')

    # 添加颜色条
    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('节点边际电价(CNY/kWh)')
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.outline.set_edgecolor('white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    # 设置轴标签和标题
    ax.set_xlabel('小时(h)')
    ax.set_ylabel('节点')
    ax.set_zlabel('电价(CNY/kWh)')
    ax.set_title('节点边际电价热力图', color='white')  # 将标题颜色设置为白色

    # 调整视角
    ax.view_init(elev=30, azim=45)  # 提高视角和旋转角度

    # 保存图形
    plt.savefig('Figure2.png', dpi=300, bbox_inches='tight', facecolor='black')

    # 显示图形
    plt.show()
        # 读取保存的图像并输出像素值和大小
    img = Image.open('Figure2.png')
    print("Image Size: ", img.size)  # 输出图像的尺寸
    img_data = np.array(img)
    print("Image Array Shape: ", img_data.shape)  # 输出图像数组的形状

figure2()
