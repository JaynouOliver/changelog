import requests
import json
from datetime import datetime

def update_repository():
    # Get a random post from JSONPlaceholder
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    data = response.json()
    
    # Add timestamp to the data
    data['timestamp'] = datetime.now().isoformat()
    
    # Create a new file with the data
    filename = f"data/update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Ensure data directory exists
    import os
    os.makedirs('data', exist_ok=True)
    
    # Write the data to file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Created file: {filename}")
    return filename

if __name__ == "__main__":
    update_repository()
