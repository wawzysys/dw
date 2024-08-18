% clc
% clear
% close all
% 计算灵敏度因子PTDF
% k：线损系数,busnum,branch,branchnum,xij,rij,nb：平衡节点
function [SFpp,SFqp,SFpq,SFqq]=PTDF(k,busnum,branch,branchnum,xij,rij,nb)
    A=zeros(busnum,branchnum);%节支关联矩阵
    Ym=zeros(branchnum,1);%支路导纳
    g=zeros(busnum,busnum);%支路电导
    b=zeros(busnum,busnum);%支路电纳
    for j=1:branchnum
        A(branch(j,1),j)=1;
        A(branch(j,2),j)=-1;
        Ym(j)=1/(rij(j)+1i*xij(j));
        g(branch(j,1),branch(j,2))=real(Ym(j));
        b(branch(j,1),branch(j,2))=imag(Ym(j));
    end
    Y=A*diag(Ym)*A';%节点导纳矩阵
    G=real(Y);%节点导纳矩阵实部
    B=imag(Y);%节点导纳矩阵虚部

%     nb=1;%平衡节点
    G(nb,:)=[];G(:,nb)=[];%去除参考节点行和列
    B(nb,:)=[];B(:,nb)=[];
    J=[G,-B;-B,-G];
    Jinv=inv(J);%对雅可比矩阵求逆
    K=Jinv(1:busnum-1,1:busnum-1);
    L=Jinv(1:busnum-1,busnum:2*(busnum-1));
    M=Jinv(busnum:2*(busnum-1),1:busnum-1);
    N=Jinv(busnum:2*(busnum-1),busnum:2*(busnum-1));
    %增加参考节点所在行与列补零
    K=[K(1:nb-1,:);zeros(1,busnum-1);K(nb:busnum-1,:)];%加行
    K=[K(:,1:nb-1),zeros(busnum,1),K(:,nb:busnum-1)];%加列
    L=[L(1:nb-1,:);zeros(1,busnum-1);L(nb:busnum-1,:)];%加行
    L=[L(:,1:nb-1),zeros(busnum,1),L(:,nb:busnum-1)];%加列
    M=[M(1:nb-1,:);zeros(1,busnum-1);M(nb:busnum-1,:)];%加行
    M=[M(:,1:nb-1),zeros(busnum,1),M(:,nb:busnum-1)];%加列
    N=[N(1:nb-1,:);zeros(1,busnum-1);N(nb:busnum-1,:)];%加行
    N=[N(:,1:nb-1),zeros(busnum,1),N(:,nb:busnum-1)];%加列
    %% SF->PTDF
    %SF
    SFpp=zeros(branchnum,busnum);
    SFqp=zeros(branchnum,busnum);
    SFpq=zeros(branchnum,busnum);
    SFqq=zeros(branchnum,busnum);
    for j=1:branchnum
        m=branch(j,1);n=branch(j,2);
        for i=1:busnum
            SFpp(j,i)=g(m,n)*(K(m,i)-K(n,i))-b(m,n)*(M(m,i)-M(n,i))+k*g(m,n)*(M(m,i)-M(n,i));
            SFqp(j,i)=-b(m,n)*(K(m,i)-K(n,i))-g(m,n)*(M(m,i)-M(n,i))-k*b(m,n)*(M(m,i)-M(n,i));
            SFpq(j,i)=g(m,n)*(L(m,i)-L(n,i))-b(m,n)*(N(m,i)-N(n,i))+k*g(m,n)*(N(m,i)-N(n,i));
            SFqq(j,i)=-b(m,n)*(L(m,i)-L(n,i))-g(m,n)*(N(m,i)-N(n,i))-k*b(m,n)*(N(m,i)-N(n,i));
        end
    end
    %PTDF
    PTDFpp=zeros(branchnum,busnum*busnum);
    PTDFqp=zeros(branchnum,busnum*busnum);
    PTDFpq=zeros(branchnum,busnum*busnum);
    PTDFqq=zeros(branchnum,busnum*busnum);
    count_b=zeros(busnum,busnum);%表征i节点注入，j节点流出
    c_b=0;
    for i=1:busnum
        for j=1:busnum
            c_b=c_b+1;
            count_b(i,j)=c_b;
            PTDFpp(:,c_b)=SFpp(:,i)-SFpp(:,j);
            PTDFqp(:,c_b)=SFqp(:,i)-SFqp(:,j);
            PTDFpq(:,c_b)=SFpq(:,i)-SFpq(:,j);
            PTDFqq(:,c_b)=SFqq(:,i)-SFqq(:,j);
        end
    end
end

