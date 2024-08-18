function x=arg_min3(y,x_gc,rho)
sdpvar X
Constraints=[];
Constraints=[Constraints,norm((X-0.2),2)==0.5];
obj=y*(X-x_gc)+(rho/2)*((X-x_gc).^2);


 ops=sdpsettings('verbose', 1, 'solver', 'gurobi','debug',1);
 
 Result=optimize(Constraints,obj,ops); 
 
 if Result.problem==0   
 
 x=value(X);
     disp('求解正确')
else
    disp('求解错误')
 end
end