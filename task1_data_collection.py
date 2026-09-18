import requests
import json
import os
import time
import datetime

HEADERS = {"User-Agent": "TrendPulse/1.0"}

CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def fetch_top_story_ids():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:500]
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return []

def fetch_story_details(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return {}

def main():
    os.makedirs("data", exist_ok=True)

    print("Fetching top 500 story IDs...")
    top_ids = fetch_top_story_ids()

    if not top_ids:
        print("No story IDs fetched. Exiting.")
        return

    all_collected_stories = []
    story_cache = {}


    for category, keywords in CATEGORIES.items():
        print(f"Scanning for '{category}' stories...")
        category_count = 0

        for story_id in top_ids:
            if category_count >= 25:
                break

            if story_id not in story_cache:
                story_data = fetch_story_details(story_id)
                story_cache[story_id] = story_data
            else:
                story_data = story_cache[story_id]

            title = story_data.get('title', '')
            title_lower = str(title).lower()

            matched = False
            for keyword in keywords:
                if keyword in title_lower:
                    matched = True
                    break

            if matched:
                formatted_story = {
                    "post_id": story_data.get("id"),
                    "title": story_data.get("title"),
                    "category": category,
                    "score": story_data.get("score"),
                    "num_comments": story_data.get("descendants"),
                    "author": story_data.get("by"),
                    "collected_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_collected_stories.append(formatted_story)
                category_count += 1

        print(f" -> Found {category_count} stories for {category}.")
        time.sleep(2)

    date_str = datetime.datetime.now().strftime("%Y%m%d")
    filepath = f"data/trends_{date_str}.json"

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_collected_stories, f, indent=4)

    print(f"\nCollected {len(all_collected_stories)} stories. Saved to {filepath}")

if __name__ == "__main__":
    main()