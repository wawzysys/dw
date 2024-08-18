% 对应节点调整负荷对新能源消纳的促进
% 输入的参数太多了
function [per_res,ddp,PPP] = Load_up(d_min,d_max,Pd,Qd,SFpp,SFpq,SFqp,SFqq,PP1,Res_node,res_num,bus_r,busnum,branchnum,rij,xij,Pr_max,SLmax,branch,nb)
ddp=[];
PPP=[];
I1=1:busnum;

for k=1:length(I1)
    bus_c=I1(k);
%     bus_c=k;
    % 变量
    Pr=sdpvar(1,busnum);%新能源发电机组实际输出
    Pi=sdpvar(1,busnum);%各节点取出的有功
    Qi=sdpvar(1,busnum);%各节点取出的无功
    Vi=sdpvar(1,busnum);%节点电压
    PLL=sdpvar(1,branchnum);%线路有功潮流
    QLL=sdpvar(1,branchnum);%线路无功潮流
    dp=sdpvar(1,busnum);%不受限制的负荷调整量
    Constraints=[];
    
    %% 目标函数
    F=-sum(Pr);%消纳新能源最多
%     F=-Pr(13)
    
    %% 约束条件
    %功率守恒约束
    Constraints = [Constraints,Pi==Pd'-Pr+dp,Qi==Qd'];%只控制新能源有功输出
    
    %潮流约束
    Constraints = [Constraints,PLL'==-(SFpp*Pi'+SFpq*Qi'),QLL'==-(SFqp*Pi'+SFqq*Qi')];
    
    %调整负荷约束
    Constraints = [Constraints,dp(bus_c)<=d_max,dp(bus_c)>=d_min,dp(1:bus_c-1)==0,dp(bus_c+1:busnum)==0];%所有节点都存在同一个上限值
    
    %电压约束
    Constraints=[Constraints,Vi(nb)==1];
    for i=1:branchnum
       Constraints=[Constraints,Vi(branch(i,1))-Vi(branch(i,2))==rij(i).*PLL(i)+xij(i).*QLL(i)];
    end
    Constraints =[Constraints,0.95<=Vi,Vi<=1.05];%118系统下需要改负荷，电压下限不行
    
    %新能源出力约束
    Constraints = [Constraints,Pr>=zeros(1,busnum),Pr<=Pr_max];
    
    %潮流限值约束
    Constraints = [Constraints,PLL(1:branchnum).^2+QLL(1:branchnum).^2<=SLmax.^2];
    
    %% 求解
    ops = sdpsettings('solver', 'gurobi', 'verbose', 2, 'debug', 1);
    result=optimize(Constraints,F,ops);
    if result.problem == 0 % problem =0 代表求解成功
        disp('求解成功') 
        res_P=-value(F)/sum(Pr_max);%总的消纳率
        PP2=zeros(1,res_num);%进行预先定义，不然没法进行并行运算
        for i=1:res_num
            PP2(i)=value(Pr(bus_r(i)))/Pr_max(bus_r(i))*100;%各节点的一个新能源消纳率，根据各节点新能源消纳率找出薄弱点   
        end
        ddp=[ddp,value(dp(bus_c))];
        PPP=[PPP;PP2];
    else
        disp('求解出错')
    end
    per_res(k)=PP2(Res_node)-PP1(Res_node);
end
end