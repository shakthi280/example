import os
import json
import openai
import requests
from openai.error import RateLimitError

# Load data
with open("scraper/tds_course_content.txt", "r", encoding="utf-8") as f:
    COURSE_CONTENT = f.read()

with open("scraper/discourse_tds_posts.json", "r", encoding="utf-8") as f:
    DISCOURSE_DATA = json.load(f)

# Use OpenRouter key and endpoint
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

def get_relevant_discourse_links(question: str, max_links=3):
    links = []
    base_url = "https://discourse.onlinedegree.iitm.ac.in/t/"
    question_lower = question.lower()
    for topic_id, posts in DISCOURSE_DATA.items():
        for post in posts:
            if question_lower in post["content"].lower():
                links.append({
                    "url": f"{base_url}{topic_id}",
                    "text": post["content"][:100].replace("\n", " ") + "..."
                })
                if len(links) >= max_links:
                    return links
    return links

def generate_answer(user_question: str):
    prompt = f"""
You are a helpful virtual TA for the Tools in Data Science (TDS) course at IIT Madras Online Degree.

Answer the following student question based on the course content and past Discourse discussions.

--- COURSE CONTENT START ---
{COURSE_CONTENT}
--- COURSE CONTENT END ---

--- STUDENT QUESTION START ---
{user_question}
--- STUDENT QUESTION END ---

Provide a concise answer based only on above content. If needed, you can refer to matching Discourse posts.
"""
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",  # or gpt-4o-mini if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        answer = response.choices[0].message["content"].strip()
        links = get_relevant_discourse_links(user_question)
        return answer, links

    except RateLimitError:
        raise RuntimeError("Proxy quota exceeded.")
    except Exception as e:
        raise RuntimeError(f"Proxy API error: {str(e)}")
