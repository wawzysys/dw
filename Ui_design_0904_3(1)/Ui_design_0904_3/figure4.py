import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams


def figure4():
    rcParams['font.family'] = 'SimHei'
    rcParams['axes.unicode_minus'] = False  # 正确显示负号
    file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'

    # 读取数据
    figure5_SL_data = pd.read_excel(file_path, sheet_name='Figure5_SL')
    figure5_SLmax_data = pd.read_excel(file_path, sheet_name='Figure5_SLmax')
    figure5_key_l_data = pd.read_excel(file_path, sheet_name='Figure5_key_l')

    nodes_figure5 = figure5_SL_data['线路编号']
    SL = figure5_SL_data['传输容量']
    SLmax = figure5_SLmax_data['容量限值']
    key_l = figure5_key_l_data['关键线路编号']
    key_l_SL = figure5_key_l_data['关键线路容量']
    branch_labels = figure5_SL_data['线路名称']

    # 绘制图形
    plt.figure(figsize=(5.103, 4.123), dpi=300, facecolor='black')  # 设置图像大小和DPI
    plt.plot(nodes_figure5, SL, label='线路传输容量', marker='o', color='blue', linewidth=1.5)
    plt.plot(nodes_figure5, SLmax, label='线路容量限值', linestyle='-', color='red', linewidth=1.5)
    plt.scatter(key_l, key_l_SL, color='red', label='关键线路', zorder=5)
    plt.xlabel('线路编号', fontsize=12, color='white')
    plt.ylabel('S(MVA)', fontsize=12, color='white')
    plt.title('系统线路传输容量', fontsize=14, color='white')
    plt.xticks(nodes_figure5, branch_labels, rotation=45, fontsize=10, color='white')
    plt.yticks(fontsize=10, color='white')
    plt.legend(fontsize=10, loc='upper left', facecolor='black', edgecolor='black', labelcolor='white')
    plt.grid(True, linestyle='-', alpha=0.7, color='white')
    plt.gca().set_facecolor('black')
    plt.tight_layout()
    plt.savefig('Figure4.png', facecolor='black')  # 确保保存时背景色为黑色
    plt.show()

figure4()
