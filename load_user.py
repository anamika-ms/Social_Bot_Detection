import ijson
import pandas as pd
from tqdm import tqdm

file_path = r"C:\Users\anami\OneDrive\Desktop\Main Project\Dataset\TwiBot-22\user.json"

selected_rows = []

with open(file_path, 'r', encoding='utf-8') as f:
    users = ijson.items(f, 'item')

    for user in tqdm(users, desc="Reading users"):
        selected_rows.append({
            "id": user.get("id"),
            "followers_count": user.get("followers_count"),
            "following_count": user.get("following_count"),
            "statuses_count": user.get("statuses_count"),
            "favourites_count": user.get("favourites_count"),
            "verified": user.get("verified")
        })

        if len(selected_rows) >= 50000:   # LIMIT for now (safe)
            break

df = pd.DataFrame(selected_rows)
df.to_csv("twibot22_behavioral_sample.csv", index=False)

print("Saved twibot22_behavioral_sample.csv")
