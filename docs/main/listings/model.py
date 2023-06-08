import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
from indexes.models.abs_model import AbstractModel

class PTModel(AbstractModel):

    def __init__(self, layers_num):
        self.pt_model = torch.nn.Sequential(
            torch.nn.Linear(1, 32),
            torch.nn.ReLU(),
            *([torch.nn.Linear(32, 32), torch.nn.ReLU()] * layers_num),
            torch.nn.Linear(32, 1)
        )

    def build(self):
        self.loss_function = torch.nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.pt_model.parameters(), lr=1e-2)

    def train(self, keys, positions):
        self.N = len(keys)
        input_tensor = torch.from_numpy(keys).unsqueeze(1).float()
        output_tensor = torch.from_numpy(positions).unsqueeze(1).float()

        dataset = TensorDataset(input_tensor, output_tensor)

        batch_size = 32
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        num_epochs = 30
        for epoch in range(num_epochs):
            mean_ae = 0
            max_ae = 0

            epoch_loss = 0.0
            for i, (batch_inputs, batch_outputs) in enumerate(dataloader):
                self.optimizer.zero_grad()
                predictions = self.pt_model(batch_inputs)
                loss = self.loss_function(predictions, batch_outputs)
                loss.backward()
                self.optimizer.step()

                epoch_loss += loss.item()
                print(f"{i}/{len(dataloader)}, Loss: {epoch_loss / (i + 1):.3e}", end='\r')

            epoch_loss /= len(dataset)
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.3e}")

            if epoch_loss < 1e-5:
                break
