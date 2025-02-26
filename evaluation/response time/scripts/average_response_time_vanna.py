import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime

def measure_response_time_post(base_url, data, headers=None):
    start_time = time.time()
    url_0 = f"{base_url}/generate_sql"
    url_1 = f"{base_url}/run_sql"
    url_2 = f"{base_url}/generate_plotly_figure"
    url_3 = f"{base_url}/generate_followup_questions"

    response = requests.get(url_0, params=data)

    if response.status_code == 200:
        try:
            vanna_id = response.json().get("id")
            if not vanna_id:
                raise ValueError("no ID returned.")
        except Exception as e:
            exit(1)
    else:
        exit(1)

    a = requests.get(url_1, params={"id": vanna_id})
    b = requests.get(url_2, params={"id": vanna_id})
    c = requests.get(url_3, params={"id": vanna_id})

    end_time = time.time()
    return end_time - start_time, c.status_code

def calculate_api_response_time_post(api_url, simultaneous_requests, total_requests, filename, message, headers):
    response_times = []
    with ThreadPoolExecutor(max_workers=simultaneous_requests) as executor:
        request_data = [{"question": message[i % len(message)]} for i in range(total_requests)]
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
    api_url = "http://108.59.81.219:58439/api/v0"
    message = [
        "What are the top 10 artists by sales?",
        "What are the total sales per year by country?",
        "Who is the top selling artist in each genre? Show the sales numbers.",
        "How do the employees rank in terms of sales performance?",
        "Which 5 cities have the most customers?",
    ]
    headers = {"Content-Type": "application/json"}
    simultaneous_requests = 4
    total_requests = simultaneous_requests * 25
    filename = "res/vanna-response-time.log"

    log(filename, "Starting API response time calculation")
    log(filename, f"++Configuration++")
    log(filename, f"API URL: {api_url}")
    log(filename, f"Headers: {headers}")
    log(filename, f"Simultaneous Requests: {simultaneous_requests}")
    log(filename, f"Total Requests: {total_requests}")
    log(filename, "")
    calculate_api_response_time_post(api_url, simultaneous_requests, total_requests, filename, message, headers=headers)
