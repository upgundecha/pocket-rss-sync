import requests
from datetime import datetime, timedelta
import os

# Your Pocket access token and consumer key
POCKET_CONSUMER_KEY = os.environ.get('POCKET_CONSUMER_KEY')
POCKET_ACCESS_TOKEN = os.environ.get('POCKET_ACCESS_TOKEN')

def get_unread_items():
    """Retrieve list of unread Pocket items."""
    retrieve_url = 'https://getpocket.com/v3/get'
    params = {
        'consumer_key': POCKET_CONSUMER_KEY,
        'access_token': POCKET_ACCESS_TOKEN,
        'state': 'unread',
        'detailType': 'simple',
    }
    response = requests.post(retrieve_url, json=params)
    if response.status_code == 200:
        return response.json().get('list', {})
    else:
        print(f"Failed to retrieve items. Status code: {response.status_code}")
        return {}

def archive_old_items(items):
    """Archive items that have been unread for more than a month."""
    one_month_ago = datetime.now() - timedelta(days=30)
    actions = []
    
    for item_id, item_details in items.items():
        # Pocket returns time added as a timestamp string
        time_added = datetime.fromtimestamp(int(item_details['time_added']))
        if time_added < one_month_ago:
            actions.append({'action': 'archive', 'item_id': item_id})
    
    if actions:
        modify_url = 'https://getpocket.com/v3/send'
        data = {
            'consumer_key': POCKET_CONSUMER_KEY,
            'access_token': POCKET_ACCESS_TOKEN,
            'actions': actions,
        }
        response = requests.post(modify_url, json=data)
        if response.status_code == 200:
            print(f"Archived {len(actions)} items.")
        else:
            print(f"Failed to archive items. Status code: {response.status_code}")

def main():
    unread_items = get_unread_items()
    if unread_items:
        archive_old_items(unread_items)
    else:
        print("No unread items or failed to retrieve items.")

if __name__ == '__main__':
    main()
