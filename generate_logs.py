import pandas as pd
from faker import Faker
import random
import time

fake = Faker()

def generate_data(filename="network_traffic.csv", rows=50000):
    print(f"Generating {rows} rows of data... this may take a moment.")
    
    # We create a limited pool of IPs so we can see patterns later
    # Otherwise, every row would have a unique random IP
    ip_pool = [fake.ipv4_public() for _ in range(50)] 
    
    data = []
    for _ in range(rows):
        data.append({
            "timestamp": fake.date_time_this_year(),
            "source_ip": random.choice(ip_pool),
            "dest_ip": "192.168.1.1", # Internal server
            "bytes_sent": random.randint(100, 20000),
            "status_code": random.choice([200, 200, 200, 404, 500]),
            "protocol": random.choice(["TCP", "UDP", "HTTP"])
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Success! {filename} created.")

if __name__ == "__main__":
    generate_data()