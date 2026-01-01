import ijson
import pandas as pd
from tqdm import tqdm

# ===== PATHS (change ONLY if your path is different) =====
USER_JSON_PATH = r"C:\Users\anami\OneDrive\Desktop\Main Project\Dataset\TwiBot-22\user.json"
OUTPUT_CSV = "twibot22_behavioral.csv"

rows = []

with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
    users = ijson.items(f, 'item')

    for user in tqdm(users, desc="Reading users"):
        metrics = user.get("public_metrics", {})

        rows.append({
            "id": user.get("id"),
            "followers_count": metrics.get("followers_count", 0),
            "following_count": metrics.get("following_count", 0),
            "statuses_count": metrics.get("tweet_count", 0),
            "verified": int(user.get("verified", False))
        })

        # LIMIT for first evaluation (safe & fast)
        if len(rows) >= 50000:
            break

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)

print("Saved:", OUTPUT_CSV)
print(df.head())
