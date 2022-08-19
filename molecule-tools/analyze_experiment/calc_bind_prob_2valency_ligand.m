%% file: calc_bind_prob_2valency_ligand.m
%% author: Jon David
%% description:
%%   reads CSV file to calculate binding probabilities
%%
%% CSV file format
%% column 1: counts of binding site 0
%% column 2: counts of binding site 1
%% column 3: counts of binding site 0, given binding site 1 is also bound
%% column 4: counts of binding site 1, given binding site 0 is also bound

function [] = calc_bind_prob_2valency_ligand(fname)
numRuns = 100;
numLigandPerRun = 5;
maxNumLigand = numLigandPerRun * numRuns;
M = csvread(fname);

%% counts
C0 = sum(M(:,1))
C1 = sum(M(:,2))
C0_1 = sum( M(:,3) )  %% notation: binding site #0 given #1 is bound.
C1_0 = sum( M(:,4) )

%% calculate single binding site probabilities
P0 = C0 / maxNumLigand
P1 = C1 / maxNumLigand

%% calculate conditional binding site probabilities
P10 =  C0_1 / C0
P01 =  C1_0/ C1

end
