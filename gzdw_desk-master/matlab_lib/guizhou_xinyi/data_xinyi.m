% Define the input data matrix, where each row is [from_node, to_node, R, X]
node_num=17;
data = [
    1, 2, 2.55, 5.925;
    1, 2, 2.55, 5.925;
    1, 3, 3.9832, 20.76243;
    1, 3, 3.47688, 16.3308;
    1, 4, 1.4943, 3.47205;
    1, 5, 0.598, 1.7848;
    1, 5, 0.598, 1.7848;
    1, 6, 1.2922, 3.85672;
    1, 6, 1.4209, 4.24084;
    1, 7, 2.6, 7.76;
    1, 8, 1.0166, 2.3621;
    1, 8, 0.6766, 1.5721;
    1, 10, 1.3893, 6.5255;
    1, 10, 1.42032, 6.6712;
    1, 12, 6.2577, 14.53995;
    1, 16, 0.51, 1.185;
    3, 4, 2.3681, 5.50235;
    3, 13, 0.91, 2.716;
    3, 13, 1.5912, 4.74912;
    3, 15, 1.911, 5.7036;
    7, 10, 3.519, 8.1765;
    8, 9, 4.25, 9.875;
    8, 17, 0.51, 1.185;
    10, 11, 1.5, 2.3621;
    13, 14, 1.5, 2.3621;
    13, 15, 1.5, 2.3621;
    14, 15, 1.5, 2.3621;
    16, 17, 1.5, 2.3621;
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
    181.0, 36.20;
    33.3, 6.66;
    100.4, 20.08;
    35.80, 7.16;
    68.00, 13.60;
    80.80, 16.16;
    0.00, 0.00;
    10.9, 2.18;
    0.00, 0.00;
    80.0, 16.00;
    0.00, 0.00;
    25.00, 5.00;
    63.20, 12.64;
    25.60, 5.12;
    0.00, 0.00;
    35.75, 7.15;
    40.00, 8.00;
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
nodes = (1:17)'; % Node numbers from 1 to 17
PV_capacities = zeros(17, 1); % Zero capacities initially

% Define the nodes with photovoltaic systems and their capacities
pv_nodes = [7, 9, 11, 15, 15]; % Nodes
pv_capacities = [50, 120, 200, 40, 0]; % Corresponding capacities

% Add capacities to the nodes
for i = 1:length(pv_nodes)
    node_index = pv_nodes(i);
    PV_capacities(node_index) = PV_capacities(node_index) + pv_capacities(i);
end

WT_capacities = zeros(17, 1);
wt_nodes = [15]; % Nodes
wt_capacities = [15]; % Corresponding capacities
for i = 1:length(wt_nodes)
    node_index =wt_nodes(i);
    WT_capacities(node_index) = WT_capacities(node_index) + wt_capacities(i);
end