import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
# def picture_1():


def picture_2():
    # 设置字体
    rcParams['font.family'] = 'SimHei'
    rcParams['axes.unicode_minus'] = False  # 正确显示负号
    # 读取Excel文件
    file_path = r'C:\Users\19160\Desktop\dw\plot_data2.xlsx'

    # Figure 4 数据
    figure4_data = pd.read_excel(file_path, sheet_name='Figure4')
    nodes_figure4 = figure4_data['节点编号']
    PP1 = figure4_data['消纳率']
    bus_r_labels_figure4 = figure4_data['节点名称']
    print(bus_r_labels_figure4)

    # Figure 5 数据
    figure5_SL_data = pd.read_excel(file_path, sheet_name='Figure5_SL')
    figure5_SLmax_data = pd.read_excel(file_path, sheet_name='Figure5_SLmax')
    figure5_key_l_data = pd.read_excel(file_path, sheet_name='Figure5_key_l')
    nodes_figure5 = figure5_SL_data['线路编号']
    SL = figure5_SL_data['传输容量']
    SLmax = figure5_SLmax_data['容量限值']
    key_l = figure5_key_l_data['关键线路编号']
    key_l_SL = figure5_key_l_data['关键线路容量']
    branch_labels = figure5_SL_data['线路名称']

    # Figure 6 数据
    figure6_PP1_PPP_data = pd.read_excel(file_path,
                                         sheet_name='Figure6_PP1_PPP')
    nodes_figure6_PP1_PPP = figure6_PP1_PPP_data['节点编号']
    PP1_figure6 = figure6_PP1_PPP_data['响应前消纳率']
    PPP = figure6_PP1_PPP_data['响应后消纳率']
    bus_r_labels_figure6 = figure6_PP1_PPP_data['节点名称']

    # 绘制 Figure 4: 新能源消纳率图
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
    plt.savefig('Figure4.png', dpi=300)
    # plt.show()

    # 绘制 Figure 5: 系统线路传输容量图
    plt.figure(figsize=(10, 6), facecolor='black')
    plt.plot(nodes_figure5,
             SL,
             label='线路传输容量',
             marker='o',
             color='blue',
             linewidth=1.5)
    plt.plot(nodes_figure5,
             SLmax,
             label='线路容量限值',
             linestyle='--',
             color='red',
             linewidth=1.5)
    plt.scatter(key_l, key_l_SL, color='red', label='关键线路', zorder=5)
    plt.xlabel('线路编号', fontsize=12, color='green')
    plt.ylabel('S(MVA)', fontsize=12, color='green')
    plt.title('系统线路传输容量', fontsize=14, color='green')
    plt.xticks(nodes_figure5,
               branch_labels,
               rotation=45,
               fontsize=10,
               color='green')
    plt.yticks(fontsize=10, color='green')
    plt.legend(fontsize=10,
               loc='upper left',
               facecolor='black',
               edgecolor='black',
               labelcolor='green')
    plt.grid(True, linestyle='--', alpha=0.7, color='green')
    plt.gca().set_facecolor('black')
    plt.tight_layout()

    plt.savefig('Figure5.png', dpi=300)
    # plt.show()

    # 绘制 Figure 6: 响应前后新能源消纳率对比图
    plt.figure(figsize=(10, 6), facecolor='black')
    bar_width = 0.4
    index = nodes_figure6_PP1_PPP - 1
    bars1 = plt.bar(index,
                    PP1_figure6,
                    bar_width,
                    label='响应前',
                    color='blue',
                    edgecolor='black')
    bars2 = plt.bar(index + bar_width,
                    PPP,
                    bar_width,
                    label='响应后',
                    color='orange',
                    edgecolor='black')
    plt.xlabel('节点编号', fontsize=12, color='green')
    plt.ylabel('消纳率/%', fontsize=12, color='green')
    plt.title('新能源消纳率前后对比', fontsize=14, color='green')
    plt.xticks(index + bar_width / 2,
               bus_r_labels_figure6,
               rotation=45,
               fontsize=10,
               color='green')
    plt.yticks(fontsize=10, color='green')
    plt.legend(fontsize=10,
               loc='upper left',
               facecolor='black',
               edgecolor='black',
               labelcolor='green')
    plt.grid(True, linestyle='--', alpha=0.7, color='green')
    plt.gca().set_facecolor('black')
    plt.tight_layout()

    # 在柱状图上添加数值标签
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2,
                 yval + 1,
                 f'{yval:.2f}%',
                 ha='center',
                 va='bottom',
                 fontsize=10,
                 color='green')

    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2,
                 yval + 1,
                 f'{yval:.2f}%',
                 ha='center',
                 va='bottom',
                 fontsize=10,
                 color='green')

    plt.savefig('Figure6.png', dpi=300)
    # plt.show()


picture_2()
