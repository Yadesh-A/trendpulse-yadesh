import pandas as pd
import numpy as np

def main():
    try:
        df = pd.read_csv("data/trends_clean.csv")
    except FileNotFoundError:
        print("Error: data/trends_clean.csv not found. Run Task 2 first.")
        return

    print(f"Loaded data: {df.shape}")
    print("First 5 rows:")
    print(df.head(), "\n")

    avg_score_pd = df['score'].mean()
    avg_comments_pd = df['num_comments'].mean()
    
    print(f"Average score   : {avg_score_pd:,.0f}")
    print(f"Average comments: {avg_comments_pd:,.0f}")

    print("\n--- NumPy Stats ---")

    score_array = df['score'].to_numpy()

    np_mean = np.mean(score_array)
    np_median = np.median(score_array)
    np_std = np.std(score_array)
    np_max = np.max(score_array)
    np_min = np.min(score_array)

    print(f"Mean score   : {np_mean:,.0f}")
    print(f"Median score : {np_median:,.0f}")
    print(f"Std deviation: {np_std:,.0f}")
    print(f"Max score    : {np_max:,.0f}")
    print(f"Min score    : {np_min:,.0f}")

    top_category = df['category'].value_counts().index[0]
    top_category_count = df['category'].value_counts().iloc[0]
    print(f"Most stories in: {top_category} ({top_category_count} stories)")

    max_comments_idx = df['num_comments'].idxmax()
    top_story_title = df.loc[max_comments_idx, 'title']
    top_story_comments = df.loc[max_comments_idx, 'num_comments']
    print(f'Most commented story: "{top_story_title}"  — {top_story_comments:,.0f} comments')

    df['engagement'] = df['num_comments'] / (df['score'] + 1)

    df['is_popular'] = df['score'] > np_mean

    output_filepath = "data/trends_analysed.csv"
    df.to_csv(output_filepath, index=False)
    
    print(f"\nSaved to {output_filepath}")

if __name__ == "__main__":
    main()