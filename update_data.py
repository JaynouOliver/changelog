import random
import string
from datetime import datetime

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def update_latest_status():
    # Generate some random data
    data = {
        'timestamp': datetime.now().isoformat(),
        'release_id': generate_random_string(),
        'status': 'success',
        'random_data': generate_random_string(20)
    }
    
    # Append to the file with a separator
    with open('latest_status.txt', 'a') as f:
        f.write('\n' + '='*50 + '\n')
        f.write(f"Update at: {data['timestamp']}\n")
        for key, value in data.items():
            if key != 'timestamp':  # Skip timestamp as we already wrote it
                f.write(f"{key}: {value}\n")
    
    print("\n=== Latest Update ===")
    print(f"🕒 Time: {data['timestamp']}")
    print(f"🆔 Release ID: {data['release_id']}")
    print(f"📝 Random Data: {data['random_data']}")
    print("==================\n")

    # Print the entire history
    print("Current History:")
    with open('latest_status.txt', 'r') as f:
        print(f.read())

if __name__ == "__main__":
    update_latest_status()
