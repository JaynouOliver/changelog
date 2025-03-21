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
    
    # Write to a fixed file (easier to track changes)
    with open('latest_status.txt', 'w') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
    
    print("\n=== Latest Update ===")
    print(f"🕒 Time: {data['timestamp']}")
    print(f"🆔 Release ID: {data['release_id']}")
    print(f"📝 Random Data: {data['random_data']}")
    print("==================\n")

if __name__ == "__main__":
    update_latest_status()
