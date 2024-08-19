%% 关键线路辨识-实际兴义地区数据
clc
clear
close all
%% 参数设置
baseMVA=1;%取1MVA
bus=xlsread('case0714-兴义变.xlsx',1,'B2:B18');%节点
bus_name=table2array(readtable('case0714-兴义变.xlsx','Sheet',1,'Range','A1:A18'));%变电站名称
nb=1;%平衡节点
busnum=size(bus,1);
branch=xlsread('case0714-兴义变.xlsx',2,'C2:D29');%支路
branch_name=table2array(readtable('case0714-兴义变.xlsx','Sheet',2,'Range','A1:A29'));%输电线路名称
branchnum=size(branch,1);
xij=xlsread('case0714-兴义变.xlsx',2,'J2:J29');%线路电抗实际值
rij=xlsread('case0714-兴义变.xlsx',2,'I2:I29');%线路电阻实际值
L220=[3,4,13,14,24];%存在220KV的输电线路
Vbase=110*ones(branchnum,1);%电压基准值
for i=1:size(L220,2)
    Vbase(L220(i))=220;
end

SLmax=80.*ones(1,branchnum);
SLmax(10)=20;
SLmax(20)=30;
SLmax(21)=20;
SLmax(26)=30;
SLmax(27)=30;
SLmax(22)=60;
SLmax(24)=60;

xij=xij*(baseMVA*1e6)./(Vbase.*1e3).^2;%线路电抗标幺值
rij=rij*(baseMVA*1e6)./(Vbase.*1e3).^2;

%如果为时变状态，则改变Pd、Qd和Prmax即可
Pd=xlsread('case0714-兴义变.xlsx',1,'D2:D18');%各节点有功负荷标幺值
Qd=xlsread('case0714-兴义变.xlsx',1,'E2:E18');%各节点无功负荷标幺值
bus_r=xlsread('case0714-兴义变.xlsx',3,'C2:C6');%新能源发电连接的节点号
res_num=size(bus_r,1);%连接新能源节电数
Prmax=xlsread('case0714-兴义变.xlsx',3,'K2:K6');%各新能源机组最大输出有功功率kw->p.u.
Pr_max=zeros(1,busnum);
for i=1:res_num
    Pr_max(bus_r(i))=Pr_max(bus_r(i))+Prmax(i);
end
res_num=res_num-1;

Constraints = [];

%计算分布因子
[SFpp,SFqp,SFpq,SFqq]=PTDF(0,busnum,branch,branchnum,xij,rij,nb);%取不同的值，结果还不一样，0.087,K，L分别为节点电压对有功和无功的灵敏度


%% 变量
Pr=sdpvar(1,busnum);%新能源发电机组实际输出
Pi=sdpvar(1,busnum);%各节点取出的有功
Qi=sdpvar(1,busnum);%各节点取出的无功
Vi=sdpvar(1,busnum);%节点电压的平方
lij=sdpvar(1,branchnum);%线路电流的平方
PLL=sdpvar(1,branchnum);%线路有功潮流
QLL=sdpvar(1,branchnum);%线路无功潮流
%% 目标函数
F=-sum(Pr);%消纳新能源最多

%% 约束条件
%功率守恒约束
Constraints = [Constraints,Pi==Pd'-Pr,Qi==Qd'];%只控制新能源有功输出

%潮流约束
Constraints = [Constraints,PLL'==-(SFpp*Pi'+SFpq*Qi'),QLL'==-(SFqp*Pi'+SFqq*Qi')];

%电压约束
Constraints=[Constraints,Vi(nb)==1];
for i=1:branchnum
   Constraints=[Constraints,Vi(branch(i,1))-Vi(branch(i,2))==rij(i).*PLL(i)+xij(i).*QLL(i)];%电压约束
end

Constraints = [Constraints,0.95<=Vi,Vi<=1.05];

%新能源出力约束
Constraints = [Constraints,Pr>=zeros(1,busnum),Pr<=Pr_max];

%潮流限值约束
Constraints = [Constraints,PLL(1:branchnum).^2+QLL(1:branchnum).^2<=SLmax.^2];

%% 求解
ops = sdpsettings('solver', 'gurobi', 'verbose', 2, 'debug', 1,'gurobi.NonConvex',2);
result=optimize(Constraints,F,ops);
if result.problem == 0 % problem =0 代表求解成功
    disp('求解成功') 
    res_P=-value(F)/sum(Pr_max)%总的消纳率
    for i=1:res_num
        PP1(i)=value(Pr(bus_r(i)))/Pr_max(bus_r(i))*100;%各节点的一个新能源消纳率，根据各节点新能源消纳率找出薄弱点
    end
    PP1
else
    disp('求解出错')
end

% [model, recoverymodel] = export(Constraints, F, sdpsettings('solver','Gurobi+')); %查冲突约束
% IIS=gurobi_iis(model);%这个报错说明模型是可行的
% gurobi_write(model, 'mymodel.lp');
%% 绘图
% figure(1)
% plot(1:busnum,value(Vi))%电压关系
% xlabel('节点（n）') 
% ylabel('V(p.u.)')
% legend('V');  % 添加线段标签
% 
% figure(2)%线路容量
% PLL=value(PLL);
% QLL=value(QLL);
% SLL=PLL.^2+QLL.^2;
% plot(1:branchnum,sqrt(SLL),"LineWidth",1.5)
% hold on
% stairs(1:branchnum,SLmax.*ones(1,branchnum),'r--',"LineWidth",1.5)%限值
% xlim([1,branchnum])
% ylim([1,100])
% xlabel('线路（n）') 
% ylabel('S(MVA)')
% legend('SL','SLmax');  % 添加线段标签

%% 关键线路辨识
bus_rn=find(PP1==min(PP1));%新能源消纳的薄弱点的编号
res_node=bus_r(bus_rn);%新能源消纳的薄弱点的节点
PLL=value(PLL);
QLL=value(QLL);
SLL=PLL.^2+QLL.^2;%线路容量的平方
dS=sqrt((PLL'.*1e6+SFpp(:,res_node)).^2+(QLL'.*1e6+SFqp(:,res_node)).^2)-sqrt(SLL'.*1e12);%注入1kw
% figure(3)
% plot(1:branchnum,dS,"LineWidth",1.5)
% xlabel('线路（n）') 
% ylabel('ΔS(KVA)')
% legend('SL','SLmax');  % 添加线段标签

[dS,II]=sort(dS,'descend');%将剩余传输容量变化进行降序排序
key_l=[];
%筛选出关键线路
for i=1:branchnum
    if dS(i)>1e-2 
        key_l=[key_l,II(i)];
    end
end

%平台可视化图片
figure(4)%新能源消纳率
bar(1:res_num,PP1,'BarWidth',0.6)%新能源消纳率
for i = 1:size(PP1,2)
    %直方图上面数据对不齐，利用水平和垂直对齐 ，可以参考text函数
    text(i,PP1(i)+3,[num2str(PP1(i),3),'%'],'VerticalAlignment','middle','HorizontalAlignment','center','FontName','Times New Ronman','FontSize',12);      
end
% 将横坐标刻度标签设置为汉字
set(gca, 'xticklabels', bus_name(bus_r),'FontName','宋体','FontSize',12);
ylabel('消纳率/%','FontSize',12)
ylim([0,110])
title('新能源消纳率','FontName','宋体','FontSize',12);  % 添加线段标签
%输出图片
exportgraphics(gca,'REC_xinyi.png','Resolution',600); % 保存到工作目录下，名字为"a.png"

figure(5)%线路传输容量
SL=sqrt(SLL);
plot(1:branchnum,SL,"LineWidth",1.5)
hold on
stairs(1:branchnum,SLmax.*ones(1,branchnum),'r--',"LineWidth",1.5)%线路容量
hold on
scatter(key_l,SL(key_l),'*',"LineWidth",1.5)
xlim([1,branchnum])
xticks(1:1:branchnum)
xtickangle(0)
ylim([0,100])
xlabel('线路编号','FontName','宋体','FontSize',12) 
ylabel('S(MVA)','FontName','Times New Ronman','FontSize',12)
legend('线路传输容量','线路容量限值','关键线路');  % 添加线段标签
title('系统线路传输容量','FontName','宋体','FontSize',12);  % 添加线段标签
%输出图片
exportgraphics(gca,'LC_xinyi.png','Resolution',600); % 保存到工作目录下，名字为"a.png"

%% 分析节点排序结果
% d_min=input('输入可调负荷下限:');%-10
% d_max=input('输入可调负荷上限:');%10
d_min=-10;
d_max=10;
tic%开始计时
[per_res,ddp,PPP] = Load_up(d_min,d_max,Pd,Qd,SFpp,SFpq,SFqp,SFqq,PP1,bus_rn,res_num,bus_r,busnum,branchnum,rij,xij,Pr_max,SLmax,branch,nb);
toc%结束计时
[per_res,I1]=sort(per_res,'descend');
per_res=[I1;per_res];
figure(6)
plot(1:busnum,per_res(2,:))
title('不同节点排序新能源消纳的提升')
key_Ln=[];
%筛选出调节负荷节点
for i=1:busnum
    if per_res(2,i)>1e-2 
        key_Ln=[key_Ln,per_res(1,i)];
    end
end

figure(6)
bar(1:res_num,[PP1' PPP(key_Ln(1),:)'],'BarWidth',0.9)%新能源消纳率
for i = 1:size(PP1,2)
    %直方图上面数据对不齐，利用水平和垂直对齐 ，可以参考text函数
    text(i-0.15,PP1(i)+2,[num2str(PP1(i),3),'%'],'VerticalAlignment','middle','HorizontalAlignment','center','FontName','Times New Ronman','FontSize',6);
    text(i+0.15,PPP(key_Ln(1),i)+2,[num2str(PPP(key_Ln(1),i),3),'%'],'VerticalAlignment','middle','HorizontalAlignment','center','FontName','Times New Ronman','FontSize',6);
end
% 将横坐标刻度标签设置为汉字
set(gca, 'xticklabels', bus_name(bus_r),'FontName','宋体','FontSize',12);
ylabel('消纳率/%','FontSize',12)
ylim([0,130])
title('新能源消纳率','FontName','宋体','FontSize',12);  % 添加线段标签
legend('响应前','响应后')
%输出图片
exportgraphics(gca,'REC_change_xinyi.png','Resolution',600); % 保存到工作目录下，名字为"a.png"
%% 表格输出
delete("输出结果_兴义.xlsx")
char={'新能源消纳薄弱点：',bus_name{res_node}};
writecell(char,'输出结果_兴义.xlsx','Sheet','薄弱点','Range','A1:B1');

char={'关键输电线路','线路有功潮流（MW）','线路无功潮流(MVar)'};
writecell(char,'输出结果_兴义.xlsx','Sheet','关键线路潮流','Range','A1:C1');
writecell(branch_name(key_l),'输出结果_兴义.xlsx','Sheet','关键线路潮流','Range','A2'); 
writematrix(PLL(key_l)','输出结果_兴义.xlsx','Sheet','关键线路潮流','Range','B2'); 
writematrix(QLL(key_l)','输出结果_兴义.xlsx','Sheet','关键线路潮流','Range','C2'); 

char={'节点排序','节点名称'};
writecell(char,'输出结果_兴义.xlsx','Sheet','负荷节点排序','Range','A1:B1');
writematrix([1:length(key_Ln)]','输出结果_兴义.xlsx','Sheet','负荷节点排序','Range','A2'); 
writecell(bus_name(key_Ln),'输出结果_兴义.xlsx','Sheet','负荷节点排序','Range','B2');

% 保存绘图数据到Excel文件
output_filename = 'plot_data.xlsx';

% Figure 4 数据
PP1_data = [1:res_num; PP1]';
bus_r_labels = bus_name(bus_r);
writecell({'节点编号', '消纳率'}, output_filename, 'Sheet', 'Figure4', 'Range', 'A1:B1');
writematrix(PP1_data, output_filename, 'Sheet', 'Figure4', 'Range', 'A2');
writecell({'节点名称'}, output_filename, 'Sheet', 'Figure4', 'Range', 'C1');
writecell(bus_r_labels, output_filename, 'Sheet', 'Figure4', 'Range', 'C2');  % 这里进行转置

% Figure 5 数据
SL_data = [1:branchnum; SL]';
SLmax_data = [1:branchnum; SLmax]';
key_l_data = [key_l; SL(key_l)]';
branch_labels = branch_name;
writecell({'线路编号', '传输容量'}, output_filename, 'Sheet', 'Figure5_SL', 'Range', 'A1:B1');
writematrix(SL_data, output_filename, 'Sheet', 'Figure5_SL', 'Range', 'A2');
writecell({'线路编号', '容量限值'}, output_filename, 'Sheet', 'Figure5_SLmax', 'Range', 'A1:B1');
writematrix(SLmax_data, output_filename, 'Sheet', 'Figure5_SLmax', 'Range', 'A2');
writecell({'关键线路编号', '关键线路容量'}, output_filename, 'Sheet', 'Figure5_key_l', 'Range', 'A1:B1');
writematrix(key_l_data, output_filename, 'Sheet', 'Figure5_key_l', 'Range', 'A2');
writecell({'线路名称'}, output_filename, 'Sheet', 'Figure5_SL', 'Range', 'C1');
writecell(branch_labels, output_filename, 'Sheet', 'Figure5_SL', 'Range', 'C2');  % 这里进行转置

% Figure 6 数据（不同节点排序新能源消纳的提升）
per_res_data = [1:busnum; per_res(2,:)]';
writecell({'节点编号', '消纳提升'}, output_filename, 'Sheet', 'Figure6_per_res', 'Range', 'A1:B1');
writematrix(per_res_data, output_filename, 'Sheet', 'Figure6_per_res', 'Range', 'A2');

% Figure 6 数据（响应前后新能源消纳率对比）
PPP_data = [1:res_num; PP1; PPP(key_Ln(1),:)]';
writecell({'节点编号', '响应前消纳率', '响应后消纳率'}, output_filename, 'Sheet', 'Figure6_PP1_PPP', 'Range', 'A1:C1');
writematrix(PPP_data, output_filename, 'Sheet', 'Figure6_PP1_PPP', 'Range', 'A2');
writecell({'节点名称'}, output_filename, 'Sheet', 'Figure6_PP1_PPP', 'Range', 'D1');
writecell(bus_r_labels, output_filename, 'Sheet', 'Figure6_PP1_PPP', 'Range', 'D2');  % 这里进行转置


