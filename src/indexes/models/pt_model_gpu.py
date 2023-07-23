import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader

from indexes.models.abs_model import AbstractModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

class PTModel(AbstractModel):

    def __init__(self, layers_num):
        self.pt_model = torch.nn.Sequential(
            torch.nn.Linear(1, 32),
            torch.nn.ReLU(),
            *([torch.nn.Linear(32, 32), torch.nn.ReLU()] * layers_num),
            torch.nn.Linear(32, 1)
        )
        self.pt_model.to(device)

    def build(self):
        self.loss_function = torch.nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.pt_model.parameters(), lr=1e-2)

    def train(self, keys, positions):
        self.N = len(keys)
        input_tensor = torch.from_numpy(keys).unsqueeze(1).float().to(device)
        output_tensor = torch.from_numpy(positions).unsqueeze(1).float().to(device)

        dataset = TensorDataset(input_tensor, output_tensor)

        batch_size = 1
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        num_epochs = 30
        for epoch in range(num_epochs):
            epoch_loss = 0.0
            for i, (batch_inputs, batch_outputs) in enumerate(dataloader):
                self.optimizer.zero_grad()
                predictions = self.pt_model(batch_inputs)
                loss = self.loss_function(predictions, batch_outputs)
                loss.backward()
                self.optimizer.step()

                epoch_loss += loss.item()
                print(f"{i}/{len(dataloader)} loss: {epoch_loss / (i + 1):.3e}", end='\r')

            epoch_loss /= len(dataset)
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.3e}")

            if epoch_loss < 1e-5:
                break

        with torch.no_grad():
            predictions = self.pt_model(input_tensor)

        y_pred = predictions.cpu().numpy().reshape(-1)

        absolute_errors = np.round(np.abs(positions - y_pred) * self.N).astype(int)

        self.max_absolute_error = np.max(absolute_errors)
        self.mean_absolute_error = np.ceil(np.mean(absolute_errors)).astype(int)

    def get_max_abs_err(self):
        return self.max_absolute_error

    def get_mean_abs_err(self):
        return self.mean_absolute_error

    def __call__(self, keys):
        keys = torch.from_numpy(keys).unsqueeze(1).float().to(device)
        return self.pt_model(keys).cpu().detach().numpy().reshape(-1)

    def size(self):
        return 0

    def save(self, path):
        #self.pt_model.save(path)
        pass

