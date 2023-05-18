import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader
import time

from utils.osm import sparce_ids

# Example input and output arrays
keys = sparce_ids

sort_indexes = np.argsort(keys)
N = len(keys)
input_array = np.array(keys)[sort_indexes]
output_array = np.arange(0, N) / (N - 1)

input_array_normalized = (input_array - np.min(input_array)) / (np.max(input_array) - np.min(input_array))

# Convert input and output arrays to PyTorch tensors
input_tensor = torch.from_numpy(input_array_normalized).unsqueeze(1).float()
output_tensor = torch.from_numpy(output_array).unsqueeze(1).float()

# Create a TensorDataset
dataset = TensorDataset(input_tensor, output_tensor)

# Set batch size and create a DataLoader for batching
batch_size = 1
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Define the model
model = torch.nn.Sequential(
    torch.nn.Linear(1, 32),
    torch.nn.ReLU(),
    torch.nn.Linear(32, 32),
    torch.nn.ReLU(),
    torch.nn.Linear(32, 1)
)

# Define the loss function and optimizer
loss_function = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Set the number of epochs
num_epochs = 30

start_time = time.time()
# Training loop
for epoch in range(num_epochs):
    for batch_inputs, batch_outputs in dataloader:
        # Zero the gradients
        optimizer.zero_grad()
        # Forward pass
        predictions = model(batch_inputs)
        # Calculate the loss
        loss = loss_function(predictions, batch_outputs)
        # Backpropagation
        loss.backward()
        # Update the model parameters
        optimizer.step()

    # Print the loss for monitoring
    #print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}")

training_time = time.time() - start_time
print("PyTorch training time:", training_time, "seconds")
# After training, you can use the trained model for predictions
# by passing new input data through the model.

