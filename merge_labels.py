import pandas as pd

# paths
BEHAVIORAL = "twibot22_behavioral.csv"
LABELS = r"C:\Users\anami\OneDrive\Desktop\Main Project\Dataset\TwiBot-22\label.csv"

df_features = pd.read_csv(BEHAVIORAL)
df_labels = pd.read_csv(LABELS)

# label mapping (bot=1, human=0)
df_labels["label"] = df_labels["label"].map({"bot": 1, "human": 0})

# merge
df = df_features.merge(df_labels, on="id", how="inner")

print("Final shape:", df.shape)
print(df.head())

df.to_csv("twibot22_final.csv", index=False)
print("Saved twibot22_final.csv")
