%node update

%%

P_who_sel=sdpvar(nb,T,'full');
P_who_buy=sdpvar(nb,T,'full');
Q_who_sel=sdpvar(nb,T,'full');
Q_who_buy=sdpvar(nb,T,'full');

%失负荷量
SL_DSO=sdpvar(J,T,'full');
SQ_DSO=sdpvar(J,T,'full');

%潮流相关变量
Pf=sdpvar(nl,T,'full');%线路有功
% V_theta=sdpvar(nb,T,'full');%电压相角

Qf=sdpvar(nl,T,'full');
U=sdpvar(nb,T,'full');%电压


Cons_MP = [];
Cons_MP_dual=cell(nb,T); 
 Cons_MP= [Cons_MP , -P_limit<= Pf(1,:)<=P_limit];
 for t=1:T
 Cons_MP= [Cons_MP , -P_limit<=sum(P_who_buy(1:nb,t))<=P_limit];
end
    for line=1:nl 
        Cons_MP= [Cons_MP , -Line_max(line)<= Pf(line,:)<=Line_max(line)];%（72)*X_line_sp(line,1)*X_line_sp(line,1)
        Cons_MP= [Cons_MP , -Line_max(line)<= Qf(line,:)<=Line_max(line)];%（72)*X_line_sp(line,1)*X_line_sp(line,1)
    end
  for line=1:nl
     for t=1:T
    Cons_MP  = [Cons_MP ,U(mpc.branch(line,2),t )-U(mpc.branch(line,3),t )+2*(R_line(line)* Pf(line,t )+X_line(line)* Qf(line,t ))/2000<=0]; %(66)*X_line_sp(line,1)
    Cons_MP  = [Cons_MP ,U(mpc.branch(line,2),t )-U(mpc.branch(line,3),t )+2*(R_line(line)* Pf(line,t )+X_line(line)* Qf(line,t ))/2000>=0]; %(66)*X_line_sp(line,1)
     end
  end
  
for bus=1:nb
 Cons_MP  = [Cons_MP , 0.92.^2<=U(bus,:)<=1.08.^2];%（71)
end
 Cons_MP  = [Cons_MP ,U(1,:)==1];

 
 %penalty 约束（43）
% Cons_MP  = [Cons_MP ,0<=P_who_sel(j+1,:)<=P_op_sel(j,:),0<=P_who_buy(j+1,:)<=P_op_buy(j,:)];
% Cons_MP  = [Cons_MP ,0<=Q_who_sel(j+1,:)<=Q_op_sel(j,:),0<=Q_who_buy(j+1,:)<=Q_op_buy(j,:)];

bus=1;
  Cons_MP  = [Cons_MP ,0<=P_who_sel(bus,:),0<=P_who_buy(bus,:)];
   Cons_MP  = [Cons_MP ,0<=Q_who_sel(bus,:),0<=Q_who_buy(bus,:)];

  for bus=2:nb
%       if bus~=j+1
    Cons_MP  = [Cons_MP ,0<=P_who_sel(bus,:)<=P_op_sel(bus-1,:),0<=P_who_buy(bus,:)<=P_op_buy(bus-1,:)];
    Cons_MP  = [Cons_MP ,0<=Q_who_sel(bus,:)<=Q_op_sel(bus-1,:),0<=Q_who_buy(bus,:)<=Q_op_buy(bus-1,:)];
%       end
  end
% %交易量  
for j=1:J
for t=1:T
 Cons_MP  = [Cons_MP , -P_who_sel(j+1,t)+P_who_buy(j+1,t)+P2P(j,t)+P_gen(j,t)+PV_gen(j,t)==pload(j,t)+P_b(j,t)-SL_DSO(j,t)];%
  Cons_MP  = [Cons_MP ,-Q_who_sel(j+1,t)+Q_who_buy(j+1,t)+Q_gen(j,t)==qload(j,t)-SQ_DSO(j,t)];
end
end
  %

% % 失负荷量               
Cons_MP  = [Cons_MP ,0<=SL_DSO<=pload(1:J,:)];
Cons_MP  = [Cons_MP ,0<=SQ_DSO<=qload(1:J,:)];    


 %节点平衡
  for bus=2:nb
          lineout=Bus_lineout{bus}; 
          linein=Bus_linein{bus}; 
    for t=1:T  
        Cons_MP_dual{bus,t}=-sum(Pf(lineout(1,:),t))+sum(Pf(linein(1,:),t))==-P_who_sel(bus,t)+P_who_buy(bus,t)+P2P(bus-1,t);%-SL_DSO(bus-1,t);
          Cons_MP  = [Cons_MP ,-sum(Qf(lineout(1,:),t))+sum(Qf(linein(1,:),t))==-Q_who_sel(bus,t)+Q_who_buy(bus,t)];%-SQ_DSO(bus-1,t)];       
    end
  end
   bus=1;
         lineout=Bus_lineout{bus}; 
          linein=Bus_linein{bus}; 
  for t=1:T
 Cons_MP_dual{bus,t}=sum(-P_who_sel(2:nb,t))+sum(P_who_buy(2:nb,t))-sum(Pf(lineout(1,:),t))+sum(Pf(linein(1,:),t))==-P_who_sel(bus,t)+P_who_buy(bus,t);
    Cons_MP  = [Cons_MP ,sum(-Q_who_sel(2:nb,t))+sum(Q_who_buy(2:nb,t))-sum(Qf(lineout(1,:),t))+sum(Qf(linein(1,:),t))==-Q_who_sel(bus,t)+Q_who_buy(bus,t)];
  end
 
%  Cons_MP  = [Cons_MP ,-100<=pen_DSO<=1000];

for bus=2:nb
% objection_MP(bus)=sum(mpc.miu_b(bus-1)*(SL_DSO(bus-1,:)+SQ_DSO(bus-1,:)));
Lost_DSO(bus)=sum(mpc.miu_b(bus-1).*(SL_DSO(bus-1,:)+SQ_DSO(bus-1,:)));
%sum(mpc.miu_b(bus-1).*((P_op_sel(bus-1,:)-P_who_sel(bus,:)+P_op_buy(bus-1,:)-P_who_buy(bus,:))+(Q_op_sel(bus-1,:)-Q_who_sel(bus,:)+Q_op_buy(bus-1,:)-Q_who_buy(bus,:))));
pen_DSO(bus)=1.5*sum(((P_op_sel(bus-1,:)-P_who_sel(bus,:)+P_op_buy(bus-1,:)-P_who_buy(bus,:))+(Q_op_sel(bus-1,:)-Q_who_sel(bus,:)+Q_op_buy(bus-1,:)-Q_who_buy(bus,:))));
objection_MP(bus)=sum(c_imp'.*(-0.9*P_who_sel(bus,:)+P_who_buy(bus,:)-0.9*Q_who_sel(bus,:)+Q_who_buy(bus,:)));
%-sum((DLMP(bus,:,k_pmp)-c_imp').*(-P_who_sel(bus,:)+P_who_buy(bus,:)-Q_who_sel(bus,:)+Q_who_buy(bus,:)));
end
bus=1;
objection_MP(bus)=sum(c_imp'.*(-0.9*P_who_sel(bus,:)+P_who_buy(bus,:)-0.9*Q_who_sel(bus,:)+Q_who_buy(bus,:)))%sum(0.2*sum(P_who_sel(2:nb,:))-sum(P_who_buy(2:nb,:))+sum(Q_who_sel(2:nb,:))-sum(Q_who_buy(2:nb,:)));
Lost_DSO(1)=0;
pen_DSO(1)=0;
 ops=sdpsettings('verbose', 1, 'solver', 'gurobi');
ops.gurobi.MIPGap=0.50000000000000;
ops.gurobi.MIPGapAbs=0.50000000000000;
Result=optimize([Cons_MP,Cons_MP_dual{1:nb,1:T}],sum(objection_MP)+sum(pen_DSO)+sum(Lost_DSO),ops);%sum(objection_MP)+sum(Lost_DSO)-sum(objection_MP)++sum(Lost_DSO)
problem=Result.problem;

if Result.problem==0
  
          disp('MP求解正确')
else
    disp('MP求解错误')
end 
for j=1:J
P_DSO_sel(j,:)=value(P_who_sel(j+1,:));
P_DSO_buy(j,:)=value(P_who_buy(j+1,:));
Q_DSO_sel(j,:)=value(Q_who_sel(j+1,:));
Q_DSO_buy(j,:)=value(Q_who_buy(j+1,:));
obj_MP(j)=value(objection_MP(j));
SL_D(j,:)=value(SL_DSO(j,:));
SQ_D(j,:)=value(SQ_DSO(j,:));
end
for bus=1:nb
    for t=1:T
        DLMP_test(bus,t)=abs(dual(Cons_MP_dual{bus,t}));
%         DLMP_test(1,t)=abs(dual(Cons_MP_dual{1,t}));
    end
end
CostLost_DSO=value(Lost_DSO);
Cov_bilv=value(sum(pen_DSO))/(1.5*nb*T);
