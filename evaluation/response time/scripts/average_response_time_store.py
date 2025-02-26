import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime

def measure_response_time_post(api_url, data, headers=None):
    start_time = time.time()
    response = requests.post(api_url, json=data, headers=headers)
    end_time = time.time()
    return end_time - start_time, response.status_code

def calculate_api_response_time_post(api_url, simultaneous_requests, total_requests, filename, message, headers):
    response_times = []
    with ThreadPoolExecutor(max_workers=simultaneous_requests) as executor:
        request_data = [{"user_id": "Tom", "message": message[i % len(message)]} for i in range(total_requests)]
        futures = [executor.submit(measure_response_time_post, api_url, data, headers) for data in request_data]

        for future in as_completed(futures):
            try:
                response_time, status_code = future.result()
                response_times.append(response_time)
                log(filename, f"Request completed in {response_time:.2f} seconds with status code {status_code}")

            except Exception as e:
                print(f"Request failed: {e}")
                log(filename, f"Request failed: {e}")

    if response_times:
        average_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
    else:
        average_time = min_time = max_time = 0

    print(f"Average Response Time: {average_time:.2f} seconds")
    print(f"Minimum Response Time: {min_time:.2f} seconds")
    print(f"Maximum Response Time: {max_time:.2f} seconds")

    log(filename, "")
    log(filename, f"++Result++")
    log(filename, f"Average Response Time: {average_time:.2f} seconds")
    log(filename, f"Minimum Response Time: {min_time:.2f} seconds")
    log(filename, f"Maximum Response Time: {max_time:.2f} seconds")


def log(file, content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {content}\n"

    with open(file, "a") as f:
        f.write(log_message)


if __name__ == "__main__":
    api_url = "http://108.59.81.219:8080/store-service/chat"
    message = [
        "I'd like to order one apple.",
        "Can I have 2 bananas and 1 orange, please?",
        "Can you show me my previous orders?",
        "I received an apple in bad condition. Please help.",
        "I'd like to buy an orange.",
        "Hello, how are you doing?",
        "Can I get a list of all my previous purchases?",
        "The bananas I received were too ripe. Can I get a refund?",
        "Hi, can i see the items before buying one?",
        "Order 2 oranges and 4 apples for me."
    ]
    headers = {"Content-Type": "application/json"}
    simultaneous_requests = 2
    total_requests = simultaneous_requests * 25
    filename = "res/store-response-time.log"

    log(filename, "Starting API response time calculation")
    log(filename, f"++Configuration++")
    log(filename, f"API URL: {api_url}")
    log(filename, f"Headers: {headers}")
    log(filename, f"Simultaneous Requests: {simultaneous_requests}")
    log(filename, f"Total Requests: {total_requests}")
    log(filename, "")
    calculate_api_response_time_post(api_url, simultaneous_requests, total_requests, filename, message, headers=headers)
