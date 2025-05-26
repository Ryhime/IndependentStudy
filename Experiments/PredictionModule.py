import networkx as nx
import torch
from torch_geometric.utils import from_networkx

from SimpleNetworkDelay import run_simulation
from torch_geometric.loader import DataLoader
import matplotlib.pyplot as plt
import numpy as np
from torch_geometric.nn import BatchNorm

delays, graphs = run_simulation(1000)
plt.scatter(range(len(delays)), delays)
plt.title("Line Graph with Custom X")
plt.xlabel("Time (s)")
plt.ylabel("Measurement")
plt.grid(True)
plt.savefig("Actual.png")
graph_data = []

def resize_array(arr, length):
    if (len(arr) == length): return arr
    elif (len(arr) > length): return arr[-10:]
    else: return np.concat((arr, [0] * (length - len(arr))))

for G, d in zip(graphs, delays):
    data = from_networkx(G)
    data.x = torch.tensor([resize_array(G.nodes[n]["inQueueHistory"], 10) for n in G.nodes()], dtype=torch.float)
    data.y = torch.tensor([d], dtype=torch.float)
    graph_data.append(data)

loader = DataLoader(graph_data, shuffle=True, batch_size=64)

import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool

class GCN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.lin = nn.Linear(hidden_channels, out_channels)
        self.norm = BatchNorm(hidden_channels)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = self.norm(x)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = self.norm(x)
        x = F.relu(x)
        x = global_mean_pool(x, batch)  # Aggregate node features to graph level
        x = self.lin(x)
        return x


import torch.nn as nn

# Initialize the model, optimizer, and loss function
model = GCN(in_channels=10, hidden_channels=280, out_channels=1)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = nn.MSELoss()  # Use L1Loss() for MAE

model.train()
for epoch in range(100):
    for batch in loader:
        optimizer.zero_grad()
        out = model(batch.x, batch.edge_index, batch.batch)
        # Ensure out and batch.y have the same shape
        loss = criterion(out.view(-1), batch.y.view(-1))
        loss.backward()
        optimizer.step()
    print(loss)
# Get predictions and graph
ordered_loader = DataLoader(graph_data, shuffle=False, batch_size=32)
values = []
for batch in ordered_loader:
    out = model(batch.x, batch.edge_index, batch.batch)
    values.extend(list(out.detach().numpy().flatten()))

plt.scatter(range(len(delays)), delays)
plt.title("Line Graph with Custom X")
plt.xlabel("Time (s)")
plt.ylabel("Measurement")
plt.grid(True)
plt.savefig("Actual.png")

plt.scatter(range(len(values)), values)
plt.title("Line Graph with Custom X")
plt.xlabel("Time (s)")
plt.ylabel("Measurement")
plt.grid(True)
plt.savefig("Prediction.png")