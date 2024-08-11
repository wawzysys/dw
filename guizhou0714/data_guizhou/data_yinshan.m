% Define the input data matrix, where each row is [from_node, to_node, R, X]
node_num=16;
data = [
1	2	2.57	7.88
2	4	3.46	10.59
2	8	0.70	2.14
3	8	1.91	5.84
3	4	1.62	4.97
4	6	4.13	15.54
4	5	0.93	2.86
4	7	2.34	15.01
4	7	2.57	16.46
5	7	4.07	12.47
5	9	4.93	11.89
9	10	3.16	7.63
10	11	0.83	2.53
11	12	2.62	8.02
4	13	1.97	6.02
4	14	1.57	4.81
4	16	2.26	6.91
4	16	1.12	7.20
5	15	3.28	10.03
];

% Extract unique pairs of nodes
[unique_pairs, ~, ic] = unique(data(:, 1:2), 'rows', 'stable');

% Preallocate the result array

branch_data = zeros(size(unique_pairs, 1), 4);
branch_data(:, 1:2) = unique_pairs;

% Calculate the effective R and sum of X for each unique pair
for i = 1:size(unique_pairs, 1)
    indices = find(ic == i);
    R_vals = data(indices, 3);
    X_vals = data(indices, 4);
    
    % Calculate equivalent R
    branch_data(i, 3) = 1 / sum(1 ./ R_vals);
    
    % Calculate sum of X
    branch_data(i, 4) = sum(X_vals);
end

branch_data(:, 3)=branch_data(:, 3)/242;
branch_data(:, 4)=branch_data(:, 4)/242;
% % Display the result
% disp('From To R_equiv X_sum');
% disp(result);
% Define maximum power loads (Active and Reactive) for each node from the given data
max_loads = [
    24.1	7.9
    53.2	17.5
    18.7	6.1
    69.6	22.9
    27.2	8.9
    60.0	19.7
    20.0	6.6
    0.0	0.0
    0.0	0.0
    23.2	7.6
    0.0	0.0
    0.0	0.0
    0.0	0.0
    0.0	0.0
    0.0	0.0
    20.0	6.6

];

% Define the daily load profile (24 hours) as a percentage
profile = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, ... % From midnight to 6 AM
           0.4, 0.6, 0.8, 1.0, 1.0, 1.0, ... % 6 AM to Noon
           1.0, 1.0, 1.0, 1.0, 1.0, 1.0, ... % Noon to 6 PM
           0.8, 0.6, 0.4, 0.2, 0.2, 0.2];     % 6 PM to midnight

% Calculate hourly loads for each node
hourly_loads = zeros(24, size(max_loads, 1), 2); % Initialize the matrix

for i = 1:24
    hourly_loads(i, :, :) = max_loads .* profile(i);
end

% Reshape for easy viewing and manipulation
hourly_loads = permute(hourly_loads, [2, 1, 3]);

% Display the first few nodes' hourly loads (active and reactive)
% for i = 1:min(5, size(max_loads, 1)) % Only display up to 5 nodes
%     fprintf('Node %d - Active and Reactive Power:\n', i);
%     disp(squeeze(hourly_loads(i, :, :)));
% end


% Initialize the matrix with node numbers and zero capacities
nodes = (1:16)'; % Node numbers from 1 to 17
PV_capacities = zeros(16, 1); % Zero capacities initially

% Define the nodes with photovoltaic systems and their capacities
pv_nodes = [11,12,13,14,15]; % Nodes
pv_capacities = [ 50, 50, 120, 100,100]; % Corresponding capacities

% Add capacities to the nodes
for i = 1:length(pv_nodes)
    node_index = pv_nodes(i);
    PV_capacities(node_index) = PV_capacities(node_index) + pv_capacities(i);
end

WT_capacities = zeros(16, 1);
wt_nodes = [8]; % Nodes
wt_capacities = [42]; % Corresponding capacities
for i = 1:length(wt_nodes)
    node_index =wt_nodes(i);
    WT_capacities(node_index) = WT_capacities(node_index) + wt_capacities(i);
end

PG_capacities = zeros(16, 1);
pg_nodes = [1,2,3,4,5,10]; % Nodes
pg_capacities=[40,80,40,180,80,60];

for i = 1:length(pg_nodes)
    node_index =pg_nodes(i);
    PG_capacities(node_index) = PG_capacities(node_index) + pg_capacities(i);
end

