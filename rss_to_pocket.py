import feedparser
import requests
import os

# File to track added URLs
TRACKER_FILE = 'added_urls.txt'

def load_added_urls():
    """Load URLs from the tracker file."""
    if not os.path.exists(TRACKER_FILE):
        return set()
    with open(TRACKER_FILE, 'r') as file:
        return set(file.read().splitlines())

def add_to_pocket(url, title, added_urls):
    """Add a URL to Pocket if not already added."""
    if url in added_urls:
        print(f"URL already added to Pocket: {url}")
        return
    # Pocket API call as before
    # On successful add, append the URL to the tracker file
    with open(TRACKER_FILE, 'a') as file:
        file.write(url + '\n')
    print(f"Successfully added and tracked {title}")

def main():
    added_urls = load_added_urls()
    
    rss_feeds = [
        'https://github.blog/category/engineering/feed/',
        'https://engineering.fb.com/feed/',
        # Add more RSS feed URLs here
    ]
    
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            latest_post = feed.entries[0]  # Assuming the first entry is the latest
            add_to_pocket(latest_post.link, latest_post.title, added_urls)

if __name__ == '__main__':
    main()
