from noshow_iq.preprocess import load_and_clean, get_features_and_target
from noshow_iq.model import train

df = load_and_clean("noshow_iq/data/KaggleV2-May-2016.csv")
X, y = get_features_and_target(df)
train(X, y)
print("Model trained successfully!")