from fastai.vision import *
from pathlib import Path

LABELS_FILE = Path("./../../data")

df = pd.read_csv(LABELS_FILE/'labels.csv', header='infer')
df.columns = ["name", "label"]

# get databunch: see also https://forums.fast.ai/t/label-delim-error-with-imagedatabunch-from-df-when-used-with-float-labels-regression-task/39661/5
data = ImageList.from_df(df, "").split_by_rand_pct().label_from_df(cols=1,label_cls=FloatList).databunch()
learn = cnn_learner(data, models.resnet18, metrics=accuracy)

learn.fit(1)