import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

def figure5():
    # 设置字体
    rcParams['font.family'] = 'SimHei'
    rcParams['axes.unicode_minus'] = False  # 正确显示负号
    
    # 读取Excel文件
    file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'
    
    # 读取数据
    figure6_PP1_PPP_data = pd.read_excel(file_path, sheet_name='Figure6_PP1_PPP')
    nodes_figure6_PP1_PPP = figure6_PP1_PPP_data['节点编号']
    PP1_figure6 = figure6_PP1_PPP_data['响应前消纳率']
    PPP = figure6_PP1_PPP_data['响应后消纳率']
    bus_r_labels_figure6 = figure6_PP1_PPP_data['节点名称']

    # 绘制图形
    plt.figure(figsize=(5.103, 4.123), dpi=300, facecolor='black')  # 精确设置图像尺寸和DPI
    bar_width = 0.4
    index = nodes_figure6_PP1_PPP - 1
    bars1 = plt.bar(index, PP1_figure6, bar_width, label='响应前', color='blue', edgecolor='black')
    bars2 = plt.bar(index + bar_width, PPP, bar_width, label='响应后', color='orange', edgecolor='black')
    
    plt.xlabel('节点编号', fontsize=12, color='white')
    plt.ylabel('消纳率/%', fontsize=12, color='white')
    plt.title('兴义新能源消纳率前后对比', fontsize=14, color='white')
    plt.xticks(index + bar_width / 2, bus_r_labels_figure6, rotation=45, fontsize=10, color='white')
    plt.yticks(fontsize=10, color='white')
    plt.legend(fontsize=10, loc='upper left', facecolor='black', edgecolor='black', labelcolor='white')
    plt.grid(True, linestyle='-', alpha=0.7, color='white')
    plt.gca().set_facecolor('black')

    # 在柱状图上添加数值标签
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom', fontsize=10, color='white')

    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom', fontsize=10, color='white')

    # 设置边框颜色
    ax = plt.gca()
    ax.set_facecolor('black')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # 调整子图边界以形成白色边框效果
    plt.savefig('Figure5.png', facecolor='black', bbox_inches='tight')  # 保存图像，确保背景色为黑色，边框为白色
    plt.show()

figure5()
