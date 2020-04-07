from fastai.callbacks import SaveModelCallback
from fastai.vision import *
from fastai.basic_train import Learner
from torch.nn import LSTM
import fastai.metrics

from inputfiles.stock_symbols import MSCI_WORLD_SYMBOLS, DAX_SYMBOLS
from machine_learning.lstm.custom_lstm import CustomLSTM
from machine_learning.lstm.data import DataLoader
import streamlit as st

DAY_COUNT = 100
BS = 32

st.title("Training of LSTM model")
stock_symbols = MSCI_WORLD_SYMBOLS + DAX_SYMBOLS

stock_symbol = st.sidebar.selectbox('Select stocks:', (stock_symbols))
model_name = f"{stock_symbol}_bestmodel"


def get_learner(data, model, pretrained=False):
    learn = Learner(data, model, loss_func=torch.nn.MSELoss(size_average=False),
                    metrics=[mean_squared_error])
    if pretrained: learn.freeze()
    return learn


model = CustomLSTM(DAY_COUNT, 50, batch_size=BS, output_dim=1, num_layers=1)
data = DataLoader(stock_symbol, DAY_COUNT, BS).get_databunch()

learn = get_learner(data, model)
if os.path.isfile(Path("./models/")/f"{model_name}.pth"):
    learn.load(model_name)
else:
    learn.fit_one_cycle(100, max_lr=0.01, callbacks=[
        SaveModelCallback(learn, every='improvement', name=model_name)
    ])

y_pred_valid = learn.get_preds(ds_type=DatasetType.Valid)

df = pd.DataFrame({"Prediction": y_pred_valid[0].numpy().flatten().tolist(),
                   "Actual": learn.data.valid_ds.y.flatten().tolist()},
                  columns=["Prediction", "Actual"]).astype(float)

st.line_chart(df)


PRED_DAYS = 40
st.markdown(f'# Predict next {PRED_DAYS} days')
learn.model = learn.model.eval()
start_index = st.slider("Start Day", 0, len(data.valid_ds)-PRED_DAYS, 0)
X_init = data.valid_ds.X[start_index]
y_pred_list, y_target_list = list(), list()
for i in range(PRED_DAYS):
    input = np.concatenate((X_init.flatten(), data.valid_ds.tabular[start_index+i].astype(int)))
    y_pred = learn.model(torch.from_numpy(input).unsqueeze(0))
    y_pred_list.append(float(y_pred.detach().numpy()))
    y_target_list.append(float(data.valid_ds.y[start_index + i]))
    X_init = np.append(np.delete(X_init, 0), y_pred.detach().numpy())

df = pd.DataFrame({"Prediction": y_pred_list,
                   "Actual": y_target_list},
                  columns=["Prediction", "Actual"]).astype(float)

st.line_chart(df)
