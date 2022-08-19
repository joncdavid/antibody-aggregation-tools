function [M] = calcBindingSiteProbabilities(fname)
numRuns = 100;
numMb4nPerRun = 5;
maxNumMb4n = numMb4nPerRun * numRuns;
M = csvread(fname);
M = M(1:15,:);


C0 = sum(M(:,1))
C1 = sum(M(:,2))
C2 = sum(M(:,3))
C3 = sum(M(:,4))

C10 = sum( M(:,5) )
C20 = sum( M(:,6) )
C30 = sum( M(:,7) )

C01 = sum( M(:,8) )
C21 = sum( M(:,9) )
C31 = sum( M(:,10) )

C02 = sum( M(:,11) )
C12 = sum( M(:,12) )
C32 = sum( M(:,13) )

C03 = sum( M(:,14) )
C13 = sum( M(:,15) )
C23 = sum( M(:,16) )

%% calculate single binding site probabilities

P0 = C0 / maxNumMb4n
P1 = C1 / maxNumMb4n
P2 = C2 / maxNumMb4n
P3 = C3 / maxNumMb4n

%% input file format (columns)
%% fmt: C0,C1,C2,C3, C10,C20,C30, C01,C21,C31, C02,C12,C32, C03,C13,C23
%% idx:  1, 2, 3, 4,   5,  6,  7,   8,  9, 10,  11, 12, 13,  14, 15, 16

%% calculate conditional binding site probabilities

P10 = C10 / C0
P20 = C20 / C0
P30 = C30 / C0

P01 = C01 / C1
P21 = C21 / C1
P31 = C31 / C1

P02 = C02 / C2
P12 = C12 / C2
P32 = C32 / C2

P03 = C03 / C3
P13 = C13 / C3
P23 = C23 / C3


%% violin plot from...
%% http://github.com/bastibe/Violinplot-Matlab/
%% pairs: 10,20,30, 21,31, 32
%% index:  5, 6, 7,  9,10, 13
hFig = figure;
VData = [M(:,1:4), M(:,5:7), M(:,9:10), M(:,13)];
cats = {'B0', 'B1', 'B2', 'B3', 'B10', 'B20', 'B30', 'B21', 'B31', 'B32'};
violinplot(VData, cats, 'ShowMean', true, 'ShowData', true, ...
           'ShowNOtches', true);
ylim([0 inf]);
ylabel('Count', 'FontSize', 20);
xlabel('Single and Pair Binding Sites', 'FontSize', 20);
saveas(hFig,'violinPlot-mb4n-radius15.png');

end