import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
   
    os.makedirs("outputs", exist_ok=True)

    try:
        df = pd.read_csv("data/trends_analysed.csv")
        print(f"Loaded {len(df)} rows for visualization.")
    except FileNotFoundError:
        print("Error: data/trends_analysed.csv not found. Please run Task 3 first.")
        return

    top_10 = df.nlargest(10, 'score').sort_values('score', ascending=True)

    top_10['short_title'] = top_10['title'].apply(lambda x: x if len(x) <= 50 else x[:47] + "...")

    plt.figure(figsize=(10, 6))
    plt.barh(top_10['short_title'], top_10['score'], color='skyblue')
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.tight_layout()  
    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()
    print("Saved Chart 1 -> outputs/chart1_top_stories.png")

    category_counts = df['category'].value_counts()

    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'][:len(category_counts)]

    plt.figure(figsize=(8, 6))
    plt.bar(category_counts.index, category_counts.values, color=colors)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")
    plt.xticks(rotation=45) 
    plt.tight_layout()
    plt.savefig("outputs/chart2_categories.png")
    plt.close()
    print("Saved Chart 2 -> outputs/chart2_categories.png")

    plt.figure(figsize=(8, 6))

    popular_df = df[df['is_popular'] == True]
    non_popular_df = df[df['is_popular'] == False]

    plt.scatter(popular_df['score'], popular_df['num_comments'], 
                color='green', label='Popular (Above Avg)', alpha=0.7)

    plt.scatter(non_popular_df['score'], non_popular_df['num_comments'], 
                color='gray', label='Non-Popular', alpha=0.5)
    
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/chart3_scatter.png")
    plt.close()
    print("Saved Chart 3 -> outputs/chart3_scatter.png")

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight='bold')

    axes[0, 0].barh(top_10['short_title'], top_10['score'], color='skyblue')
    axes[0, 0].set_title("Top 10 Stories by Score")
    axes[0, 0].set_xlabel("Score")

    axes[0, 1].bar(category_counts.index, category_counts.values, color=colors)
    axes[0, 1].set_title("Stories per Category")
    axes[0, 1].set_ylabel("Count")
    axes[0, 1].tick_params(axis='x', rotation=45)

    axes[1, 0].scatter(popular_df['score'], popular_df['num_comments'], color='green', label='Popular', alpha=0.7)
    axes[1, 0].scatter(non_popular_df['score'], non_popular_df['num_comments'], color='gray', label='Non-Popular', alpha=0.5)
    axes[1, 0].set_title("Score vs Comments")
    axes[1, 0].set_xlabel("Score")
    axes[1, 0].set_ylabel("Comments")
    axes[1, 0].legend()

    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig("outputs/dashboard.png")
    plt.close()
    print("Saved Dashboard -> outputs/dashboard.png")
    print("\nTask 4 Complete! All charts successfully generated.")

if __name__ == "__main__":
    main()