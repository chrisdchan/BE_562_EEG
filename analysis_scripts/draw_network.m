% This script visualizes our MST
clear;

% Load parents
load('parents.mat')
parents = [parents(2:end) zeros(1,300)];
parents = parents + ones(1,599);

% Specify Children
children = 1:300;
children = [children(2:end) children];
children = children + ones(1,599);

G = digraph(parents,children);
plot(G,'Layout','layered','Sinks',2:301)
title('Visualized Maximum Spanning Tree')
