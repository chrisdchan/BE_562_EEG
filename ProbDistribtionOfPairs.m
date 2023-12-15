MST=load('mst.csv');%load MST
load('sub-01_task-rsvp_parsed.mat');%Load subject-> most likely need to do a for loop for each subject
MSTcut= triu(MST,1);%only finds pair on upper triangle of the matrix, can use numpy according to chatgpt
[r1,c1]= find(MSTcut==1);
pairs= [r1,c1];%Determines every pair


parsedTable= struct2table(parsed);
[rSize,cSize]= size(parsedTable);
classes= parsedTable.visible;

class0Index= find(classes==0);
class1Index= find(classes==1);
class0Total= length(class0Index);
class1Total= length(class1Index);

jointMean0=zeros(length(pairs),1);
jointMean1=zeros(length(pairs),1);
jointStDev0=zeros(length(pairs),1);
jointStDev1=zeros(length(pairs),1);

for k= 1:length(pairs) %for each pair determine the means and stdev for each class between pairs
    node1=pairs(k,1);
    node2= pairs(k,2);

    node1Data0= parsedTable.data(class0Index,node1); 
    node2Data0= parsedTable.data(class0Index,node2);
 
    node1Data1= parsedTable.data(class1Index,node1);
    node2Data1= parsedTable.data(class1Index,node2);

    concatData0= cat(1,node1Data0, node2Data0);
    concatData1= cat(1,node1Data1, node2Data1);
    jointMean0(k)= mean(concatData0);
    jointMean1(k)= mean(concatData1);
    jointStDev0(k)=std(concatData0);
    jointStDev1(k)=std(concatData1);
    
end

jointMatrix=[jointMean0, jointStDev0, jointMean1, jointStDev1];