import feedparser
import requests
import os

# File to track added URLs
TRACKER_FILE = 'added_urls.txt'

POCKET_CONSUMER_KEY = os.environ.get('POCKET_CONSUMER_KEY')
POCKET_ACCESS_TOKEN = os.environ.get('POCKET_ACCESS_TOKEN')

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
 
    api_url = 'https://getpocket.com/v3/add'
    headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    data = {
        'url': url,
        'title': title,
        'consumer_key': POCKET_CONSUMER_KEY,
        'access_token': POCKET_ACCESS_TOKEN,
        'tags': 'engieering-blogs'
    }
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Successfully added {title} to Pocket.")
        # On successful add, append the URL to the tracker file
        with open(TRACKER_FILE, 'a') as file:
            file.write(url + '\n')
            print(f"Successfully added and tracked {title}")
    else:
        print(f"Failed to add {title} to Pocket. Status code: {response.status_code}")

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
