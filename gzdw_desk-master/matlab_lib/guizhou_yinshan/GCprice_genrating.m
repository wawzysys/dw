function [P_s,c_GC]=GCprice_genrating(NN,alpa,mu,sigmal)
% NN=1000
% alpa=0.95


price=normrnd(mu,sigmal,5*NN,1);
[a,c_GC]=kmeans(price,NN);

P_s=zeros(1,NN);
for i=1:5*NN
    for j=1:NN
      if(a(i)==j)
          P_s(j)=P_s(j)+1;
      end
    end
end
P_s = P_s ./ (5*NN);
sum(P_s)
P_s=reshape(P_s,[NN,1]);
% %价格VAR
% [C_GC,Nn] = sort(c_GC); 
% C_GC2 = C_GC - c_GC(end);
% VaR_price =C_GC2(alpa*1000);
end