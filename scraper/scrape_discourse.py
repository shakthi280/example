import requests
from datetime import datetime
import time
import json

base_url = "https://discourse.onlinedegree.iitm.ac.in"
category_id = 34
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 4, 14)

def get_all_topic_ids():
    topic_ids = []
    page = 0
    while True:
        url = f"{base_url}/c/courses/tds-kb/{category_id}.json?page={page}"
        res = requests.get(url)
        if res.status_code != 200:
            break
        topics = res.json()["topic_list"]["topics"]
        if not topics:
            break
        for topic in topics:
            created_at = datetime.strptime(topic["created_at"][:10], "%Y-%m-%d")
            if start_date <= created_at <= end_date:
                topic_ids.append(topic["id"])
        page += 1
        time.sleep(0.5)
    return topic_ids

def get_posts(topic_id):
    url = f"{base_url}/t/{topic_id}.json"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    data = res.json()
    posts = data["post_stream"]["posts"]
    return [{"username": p["username"], "content": p["cooked"]} for p in posts]

# Run the scraper
all_data = {}
topic_ids = get_all_topic_ids()
for tid in topic_ids:
    all_data[tid] = get_posts(tid)
    time.sleep(0.5)

# Save to file
with open("scraper/discourse_tds_posts.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(all_data)} threads to discourse_tds_posts.json")



