import pandas as pd
import glob
import os

def main():
    json_files = glob.glob("data/trends_*.json")
    
    if not json_files:
        print("Error: No JSON files found in data/ folder. Please run Task 1 first.")
        return

    latest_file = max(json_files, key=os.path.getctime)

    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}")

    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")

    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")
    

    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)

    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")

    df['title'] = df['title'].str.strip()

    csv_filepath = "data/trends_clean.csv"

    df.to_csv(csv_filepath, index=False)
    print(f"Saved {len(df)} rows to {csv_filepath}")

    print("Stories per category:")
    category_summary = df['category'].value_counts()

    print(category_summary.to_string())

if __name__ == "__main__":
    main()