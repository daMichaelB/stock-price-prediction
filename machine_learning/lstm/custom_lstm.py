import torch
from fastai.tabular import TabularModel
from torch import nn, FloatTensor, DoubleTensor


class CustomLSTM(nn.Module):

    def __init__(self, input_dim, hidden_dim, batch_size, output_dim=1,
                 num_layers=2):
        super(CustomLSTM, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.batch_size = batch_size
        self.num_layers = num_layers

        # Define the LSTM layer
        self.lstm = nn.LSTM(self.input_dim, self.hidden_dim, self.num_layers)

        # Tabular Model
        self.tabular = TabularModel([], self.hidden_dim + 13, 1, [128, 128])

    def forward(self, input):
        # Forward pass through LSTM layer
        # shape of lstm_out: [input_size, batch_size, hidden_dim]
        # shape of self.hidden: (a, b), where a and b both
        # have shape (num_layers, batch_size, hidden_dim).
        input_lstm = input[:, 0:100].unsqueeze(0).type(FloatTensor)
        input_tabular = input[:, 100:].type(FloatTensor)
        lstm_out, self.hidden = self.lstm(input_lstm)

        concat_tensor = torch.cat((lstm_out, input_tabular.unsqueeze(0)), 2)
        y_pred = self.tabular(None, concat_tensor.squeeze(0))

        return y_pred.type(DoubleTensor)