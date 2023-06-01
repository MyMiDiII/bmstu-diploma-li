import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader

from indexes.models.abs_model import AbstractModel

def calculate_absolute_errors(outputs, targets, N):
    outputs = outputs.detach().numpy().reshape(-1)
    targets = targets.detach().numpy().reshape(-1)
    absolute_errors = np.round(np.abs(outputs - targets) * N).astype(int)
    print("err", absolute_errors)

    return np.sum(absolute_errors), np.max(absolute_errors)


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
                print(f"{i}/{len(dataloader)} loss: {epoch_loss / (i + 1):.3e}", end='\r')

                add_sum, new_max = calculate_absolute_errors(predictions,
                                                             batch_inputs,
                                                             self.N)
                mean_ae += add_sum
                max_ae = max(max_ae, new_max)

            epoch_loss /= len(dataset)
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.3e}")

            self.max_absolute_error = max_ae
            self.mean_absolute_error = np.ceil(mean_ae / self.N).astype(int)

            print()
            print("mean", self.mean_absolute_error)
            print("max_ae", self.max_absolute_error)


            if epoch_loss < 1e-5:
                break


    def get_max_abs_err(self):
        return self.max_absolute_error

    def get_mean_abs_err(self):
        return self.mean_absolute_error

    def __call__(self, keys):
        keys = torch.from_numpy(keys).unsqueeze(1).float()
        return self.pt_model(keys).detach().numpy().reshape(-1)

    def size(self):
        torch.save(self.pt_model.state_dict(), 'model.pth')

        import os
        model_size_bytes = os.path.getsize('model.pth')
        os.remove('model.pth')

        return model_size_bytes

    def save(self, path):
        torch.save(self.pt_model.state_dict(), path)

