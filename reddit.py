import os
import praw
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

subreddits = ["startups", "SaaS", "entrepreneur", "smallbusiness", "sideproject"]


async def summarize(text):
    prompt = f"Summarize the following text, focusing on any startup ideas or business concepts. If there are no clear startup ideas, respond with 'No startup idea found.': {text}"

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes startup ideas and business concepts.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error in summarize: {e}")
        return "Error in summarization"


async def generate_unique_idea(context):
    prompt = f"Based on the following startup ideas and business concepts, generate a unique and innovative startup idea that hasn't been mentioned before: {context}"

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative assistant that generates unique startup ideas.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error in generate_unique_idea: {e}")
        return "Error in idea generation"


async def process_post(post):
    try:
        full_text = f"{post.title}\n\n{post.selftext}"
        summary = await summarize(full_text)

        if (
            "No startup idea found" not in summary
            and "Error in summarization" not in summary
        ):
            return summary
    except Exception as e:
        logging.error(f"Error processing post {post.id}: {e}")
    return None


async def search_subreddit(subreddit_name, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    tasks = []
    for post in subreddit.new(limit=limit):
        tasks.append(process_post(post))

    results = await asyncio.gather(*tasks)
    return [result for result in results if result is not None]


async def main():
    output_file = "unique_startup_ideas.txt"
    ideas_per_subreddit = 5

    for subreddit_name in subreddits:
        try:
            logging.info(f"Searching subreddit: {subreddit_name}")
            all_summaries = await search_subreddit(subreddit_name)
            logging.info(f"Found {len(all_summaries)} summaries in r/{subreddit_name}")

            for i in range(0, len(all_summaries), 3):
                batch = all_summaries[i : i + 3]
                context = "\n\n".join(batch)
                unique_idea = await generate_unique_idea(context)

                if unique_idea and unique_idea != "Error in idea generation":
                    with open(output_file, "a") as f:
                        f.write(
                            f"Idea inspired by r/{subreddit_name}:\n{unique_idea}\n\n"
                        )
                    logging.info(
                        f"Unique idea from r/{subreddit_name} (batch {i//3 + 1}) appended to {output_file}"
                    )

                    ideas_per_subreddit -= 1
                    if ideas_per_subreddit <= 0:
                        break
                else:
                    logging.warning(
                        f"No valid unique idea generated for r/{subreddit_name} (batch {i//3 + 1}). Skipping."
                    )

            if ideas_per_subreddit > 0:
                logging.info(f"Generated all possible ideas for r/{subreddit_name}")

        except Exception as e:
            logging.error(f"Error processing subreddit {subreddit_name}: {e}")

        ideas_per_subreddit = 5


if __name__ == "__main__":
    asyncio.run(main())
