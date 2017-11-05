function coeff=pearson(X,Y)
 if length(X) ~= length(Y)  
     error('两个数值数列的维数不相等');    
 end 
fenzi = sum(X .* Y) - (sum(X) * sum(Y)) / length(X);  
fenmu = sqrt((sum(X .^2) - sum(X)^2 / length(X)) * (sum(Y .^2) - sum(Y)^2 / length(X)));  
coeff = fenzi / fenmu; 
return 