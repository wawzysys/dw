yalmip('clear')
clc;
clear;
K_pmp=20;
K=100;%max_iteration
mpc=reliability_6nodes_test_system;
N=mpc.node_num-1 ;%三个交易者
J=mpc.node_num-1 ;
T = 24;
%% 0.1 电力交易参数
%负荷数据


nb =mpc.node_num;
nl=mpc.branch_num;

pload=mpc.Pload;%节点有功负荷
qload=mpc.Qload;%节点无功负荷

r=mpc.branch(:,3);
x=mpc.branch(:,4);

DLMP=0.5*ones(nb,T,K_pmp);


%光伏
[PV_perunit]=read_data';
PV_cap=mpc.PV_cap;
PG_cap=0.8*mpc.WT_cap;
SOC_cap=0;


for n=1:nl
Line_busout(n)=mpc.branch(n,2);
Line_busin(n)=mpc.branch(n,3);
R_line(n)=mpc.branch(n,4);
X_line(n)=mpc.branch(n,5);
end

for bus=1:nb  
Bus_lineout{bus}=find(mpc.branch(:,2)==bus)';
Bus_linein{bus}=find(mpc.branch(:,3)==bus)';
end
Line_max=0.9*[180;140;140;180;160;180;160;140;140;180;160;160;160;140;140;120;130;100;100;100;100];
Vmax=1.08;
Vmin=0.92;
c_imp=10*[0.040;0.037 ;0.036 ;	0.030 ;	0.033 ;	0.034 ;	0.035 ;	0.036 ;	0.041 ;0.046;0.053 ;0.057;0.063;0.067;	0.071;	0.075 ;	0.071; 	0.066 ;	0.058 ;	0.054 ;0.050 ;0.046 ;0.043 ;0.042];

%% -----------------------------------Prosuemr iteration-----------------------------------%%
% 正态分布+Kmeans 生成 1000个价格 和对应概率场景
NN=10;
alpa=0.9;
beta=0.1;
mu =0.1;%预期年收益率为10%，mu为每日的收益率
sigmal = 0.030;%预期年波动率为30%，每年250个交易日，预期日波动率为sigma
[P_s,c_GC]=GCprice_genrating(NN,alpa,mu,sigmal);

P_DSO_buy=zeros(nb,T);
P_DSO_sel=zeros(nb,T);
Q_DSO_buy=zeros(nb,T);
Q_DSO_sel=zeros(nb,T);
SL_D=zeros(J,T);
SQ_D=zeros(J,T);

P_limit=mpc.Plimits;
%%
k_pmp=1;
flag1=1;
   Copy_of_prosumer_admm;
while flag1==1
  
    Copy_of_MP;
    
      DLMP(:,:,k_pmp+1)=DLMP_test;
      
    prosumer_admm;
if Cov_bilv<=0.3
    break
end
if k_pmp>=K_pmp
    break
end
 k_pmp=k_pmp+1;
end


  % Create a heatmap
figure;
heatmap( DLMP(:,:,k_pmp+1));
% Customize the heatmap (optional)
xlabel('小时(h)');
ylabel('节点');
title('节点边际电价(CNY/kWh)');
colormap jet; % Change the colormap to 'jet' (optional)
colorbar; % Show colorbar  
% Save the heatmap as a PNG file
output_DLMP = 'DLMPs.png';
saveas(gcf, output_DLMP);
xlswrite('DLMPs.xlsx',DLMP(:,:,k_pmp+1));

heatmap(SL_D);
% Customize the heatmap (optional)
xlabel('小时(h)');
ylabel('节点');
title('负荷调控结果(MWh)');
colormap winter; % Change the colormap to 'jet' (optional)
colorbar; % Show colorbar  
% Save the heatmap as a PNG file
output_Loadshedding = 'Loadshedding.png';
saveas(gcf, output_Loadshedding);
xlswrite('Loadshedding.xlsx',SL_D);