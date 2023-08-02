function n = getNumberValueInMatrix(matrix, value)
n = 0;
for i = 1:size(matrix, 1)
   for j = 1:size(matrix, 2)
      if matrix(i, j) == value
         n = n + 1; 
      end
   end
end
end