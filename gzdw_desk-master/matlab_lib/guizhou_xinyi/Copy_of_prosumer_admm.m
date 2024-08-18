
yalmip('clear')
clear pen_pro
%% -----------------------------0、设置参数-----------------------------------%%

%% 0.4 迭代参数初始化

%电力市场
c_ng_ij=0.1*ones(N,J,T,K);
p_ng=zeros(N,J,T,K);

%lp-box
X_gc1=zeros(J,1);
X_gc2=zeros(J,1);
X_gc3=zeros(J,1);

y_1=zeros(J,K);%相当于价格对偶
y_2=zeros(J,K);
y_3=zeros(J,K);

% 其他参数
rho=0.3;% 价格对偶的tunning parameters
rho_1=0.3;
rho_2=0.3;
rho_3=0.3;

k=1;
flag2=1;
Cons_pro=cell(J,1);
Result=cell(J,1);

while flag2==1
    k=k+1;
%% ————————————————1.ADMM-----------------------------------------------%%
%% 1.1 定义变量
%电力市场
P_op_i=sdpvar(N,T,'full');%和运营商交易量
P_op_i_s=sdpvar(N,T,'full');%交易者向运营商售出
P_op_i_b=sdpvar(N,T,'full');%交易者向运营商购入
Q_op_i=sdpvar(N,T,'full');%和运营商交易量
Q_op_i_s=sdpvar(N,T,'full');%交易者向运营商售出
Q_op_i_b=sdpvar(N,T,'full');%交易者向运营商购入

P_ng_i=sdpvar(J,J,T,'full');%交易者 i的交易量，
PV_generaton=sdpvar(J,T,'full');%prosumer i的光伏发电量
PG_gen=sdpvar(J,T,'full');
QG_gen=sdpvar(J,T,'full');
SOC=sdpvar(J,T,'full'); %prosumer i的储能SOC
P_b_i=sdpvar(J,T,'full');%prosumer i的储能充放电功率

Cost_op=sdpvar(J,T,'full');%交易者和运营商之间交易收益/成本
Cost_ng=sdpvar(J,T,'full');%交易者之间交易收益/成本
 
X_gc=sdpvar(J,1,'full');

SLP=sdpvar(N,T,'full');
SLQ=sdpvar(N,T,'full');

%潮流
V = sdpvar(nb,T);%电压的平方（节点数）
I = sdpvar(nl,T);%电流的平方（支路数）

P = sdpvar(nl,T);%线路有功
Q = sdpvar(nl,T);%线路无功

for j=1:J
    Cons_pro{j}=[];
%     Cons_pro{j}=[Cons_pro{j},Pin(bus,t)+PV_generaton(j,t)-P_b_i(j,t)== pload(bus,t)];
    for t=1:T
    Cons_pro{j}=[Cons_pro{j},pload(j,t)+P_b_i(j,t)==PV_generaton(j,t)+PG_gen(j,t)+sum(P_ng_i(j,:,t))+P_op_i(j,t)+SLP(j,t)];%平衡
    Cons_pro{j}=[Cons_pro{j},qload(j,t)==QG_gen(j,t)+Q_op_i(j,t)+SLQ(j,t)];%平衡
    end
   Cons_pro{j}=[Cons_pro{j}, 0<=SLP(j,:)<=pload(j,:), 0<=SLQ(j,:)<=qload(j,:)];
   % Cons_pro{j}=[Cons_pro{j}, SLP(j,:)==SL_D(j,:), SLQ(j,:)==SQ_D(j,:)];
    Cons_pro{j}=[Cons_pro{j},0<=PV_generaton(j,:)<=PV_perunit(j,:)*PV_cap(j)];
   Cons_pro{j}=[Cons_pro{j},0<= PG_gen(j,:)<=PG_cap(j),0<= QG_gen(j,:)<=PG_cap(j)];
    Cons_pro{j}=[Cons_pro{j},0<=abs(P_b_i(j,:))<=SOC_cap];%
    
    for t=1:(T-1)
        Cons_pro{j}=[Cons_pro{j},SOC(j,t+1)==SOC(j,t)+0.95*P_b_i(j,t)];
    end
    for t=2:T-1
         Cons_pro{j}=[Cons_pro{j},0.1<=SOC(j,t)<=0.95];
    end
     Cons_pro{j}=[Cons_pro{j},SOC(j,T)==SOC(j,1)];
     
    for t=1:T 
      Cost_op(j,t)=0.67*(PG_gen(j,t)+QG_gen(j,t))+DLMP(j+1,t,k_pmp)*((P_op_i_b(j,t)+0.9*P_op_i_s(j,t))+(Q_op_i_b(j,t)+0.9*Q_op_i_s(j,t)));
      Cost_ng(j,t)=sum(c_ng_ij(j,:,t,k).*(P_ng_i(j,:,t)-(p_ng(j,:,t,k)-p_ng(:,j,t,k)')/2)+k_pmp.^2*rho*(P_ng_i(j,:,t)-(p_ng(j,:,t,k)-p_ng(:,j,t,k)')/2).^2);%
      Cost_SL(j,t)=mpc.miu_b(j)*SLP(j,t)+mpc.miu_b(j)*SLQ(j,t);
    end
    Cons_pro{j}=[Cons_pro{j},P_ng_i(j,j,:)==0];
    Cons_pro{j}=[Cons_pro{j},P_op_i(j,:)==P_op_i_s(j,:)+P_op_i_b(j,:)];% 
    Cons_pro{j}=[Cons_pro{j},P_op_i_s(j,:)<=0];%
    Cons_pro{j}=[Cons_pro{j},P_op_i_b(j,:)>=0];%
     Cons_pro{j}=[Cons_pro{j},Q_op_i(j,:)==Q_op_i_s(j,:)+Q_op_i_b(j,:)];% 
    Cons_pro{j}=[Cons_pro{j},Q_op_i_s(j,:)==0];%
    Cons_pro{j}=[Cons_pro{j},Q_op_i_b(j,:)>=0];%

     Cons_pro{j}=[Cons_pro{j},-P_op_i_s(j,:)>=P_DSO_sel(j,:),-Q_op_i_s(j,:)>=Q_DSO_sel(j,:)];
      Cons_pro{j}=[Cons_pro{j},P_op_i_b(j,:)>=P_DSO_buy(j,:),Q_op_i_b(j,:)>=Q_DSO_buy(j,:)];
      
      Cons_pro{j}=[Cons_pro{j},P_ng_i(j,:,:)==0];
      
%   if k_pmp==1
%     pen_pro(j)=0;
%   else
  pen_pro(j)= abs(1.5*sum(((-P_op_i_s(j,:)-P_DSO_sel(j,:)+P_op_i_b(j,:)-P_DSO_buy(j,:))+(-Q_op_i_s(j,:)-Q_DSO_sel(j,:)+Q_op_i_b(j,:)-Q_DSO_buy(j,:)))));
%   end
 objection_prosumer(j)=sum(Cost_op(j,:))+sum(Cost_ng(j,:))+sum(Cost_SL(j,:));
end 

 ops=sdpsettings('verbose', 1, 'solver', 'gurobi','debug',1);
for j=1:J
Result{j}=optimize(Cons_pro{j}, objection_prosumer(j),ops);%+100*pen_pro(j)
if Result{j}.problem==0   
     obj_prosumer(j)=value(objection_prosumer(j));
     penalty_pro(j)=value(pen_pro(j));
    p_ng(j,:,:,k+1)=value(P_ng_i(j,:,:));
    P_op(j,:)=value(P_op_i(j,:));
    P_op_sel(j,:)=max(value(-P_op_i_s(j,:)),0);
    P_op_buy(j,:)=value(P_op_i_b(j,:));
    Q_op(j,:)=value(Q_op_i(j,:));
    Q_op_sel(j,:)=value(-Q_op_i_s(j,:));
    Q_op_buy(j,:)=value(Q_op_i_b(j,:));
    P_p2p(j,:,:)=value(P_ng_i(j,:,:));
    PV_gen(j,:)=value(PV_generaton(j,:));
    P_gen(j,:)=value(PG_gen(j,:));
    Q_gen(j,:)=value(QG_gen(j,:));
    P_b(j,:)=value(P_b_i(j,:));
    SL_pro(j,:)=value(SLP(j,:));
    SQ_pro(j,:)=value(SLQ(j,:));
    for t=1:T
    P2P(j,t)=value(sum(P_ng_i(j,:,t)));
    end
end   
     
     
    for j=1:J
        for t=1:T
        c_ng_ij(j,:,t,k+1)=max(0,c_ng_ij(j,:,t,k)+rho*(p_ng(j,:,t,k+1)+p_ng(:,j,t,k+1)')/2);    
        end  
    end
     
     
     
end

for t=1:T
stop_2(t)=(max(max(abs(p_ng(:,:,t,k+1)+p_ng(:,:,t,k+1)')))>=0.5)||(max(max(abs(p_ng(:,:,t,k)-p_ng(:,:,t,k+1))))>=0.5);
end

if (max(stop_2)==1)
    flag2=1;            
else
   flag2=flag2+1;
end
    if k>=K
   break
end
    
end
Cov_bilv=value(sum(penalty_pro))/(1.5*nb*T);