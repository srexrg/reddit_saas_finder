# Reddit Startup Idea Generator

This Python script scrapes startup-related subreddits, summarizes posts containing startup ideas, and generates unique startup ideas based on the collected information.

## Features

- Scrapes multiple startup-related subreddits
- Summarizes posts using OpenAI's GPT model
- Generates unique startup ideas based on summarized content
- Asynchronous processing for improved performance
- Outputs results to a text file

## Prerequisites

- Python
- Reddit API credentials
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/srexrg/reddit_saas_finder.git
   cd reddit_saas_finder
   ```

2. Install required packages:
   ```
   pip install praw
   ```

3. Create a `.env` file in the project root and add your API credentials:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   REDDIT_USERNAME=your_username
   REDDIT_PASSWORD=your_password
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

Run the script:
```
python reddit.py
```

The script will process posts from the specified subreddits and generate unique startup ideas. The results will be saved in `unique_startup_ideas.txt`.

## Configuration

You can modify the following variables in the script:

- `subreddits`: List of subreddits to scrape
- `ideas_per_subreddit`: Number of unique ideas to generate per subreddit

## License

[MIT License](LICENSE)

## Disclaimer

This script is for educational purposes only. Make sure to comply with Reddit's API terms of service when using this script.


