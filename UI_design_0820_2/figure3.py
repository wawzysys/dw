import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams


def figure3():
    # 设置字体
    rcParams['font.family'] = 'SimHei'
    rcParams['axes.unicode_minus'] = False  # 正确显示负号
    # 读取Excel文件
    file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'

    # Figure 3 数据
    figure4_data = pd.read_excel(file_path, sheet_name='Figure4')
    nodes_figure4 = figure4_data['节点编号']
    PP1 = figure4_data['消纳率']
    bus_r_labels_figure4 = figure4_data['节点名称']
    print(bus_r_labels_figure4)

    # 绘制 Figure 3: 新能源消纳率图
    plt.figure(figsize=(10, 6), facecolor='black')
    bars = plt.bar(nodes_figure4, PP1, color='blue', edgecolor='black')
    plt.xlabel('节点编号', fontsize=12, color='green')
    plt.ylabel('消纳率/%', fontsize=12, color='green')
    plt.title('新能源消纳率', fontsize=14, color='green')
    plt.xticks(nodes_figure4,
               bus_r_labels_figure4,
               rotation=45,
               fontsize=10,
               color='green')
    plt.yticks(fontsize=10, color='green')
    plt.grid(True, linestyle='--', alpha=0.7, color='green')
    plt.gca().set_facecolor('black')
    plt.tight_layout()

    # 在柱状图上添加数值标签
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2,
                 yval + 1,
                 f'{yval:.2f}%',
                 ha='center',
                 va='bottom',
                 fontsize=10,
                 color='green')

    plt.legend(['消纳率'],
               fontsize=10,
               loc='upper left',
               facecolor='black',
               edgecolor='black',
               labelcolor='green')
    plt.savefig('Figure3.png', dpi=300)


figure3()
