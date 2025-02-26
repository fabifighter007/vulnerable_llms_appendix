import re

# Raw log data
log_data = """
[2025-02-09 19:39:59] Request completed in 1.27 seconds with status code 200
[2025-02-09 19:39:59] Request completed in 1.30 seconds with status code 200
[2025-02-09 19:39:59] Request completed in 1.54 seconds with status code 200

<TRUNCATED>

[2025-02-09 19:42:09] Request completed in 2.05 seconds with status code 200
[2025-02-09 19:42:10] Request completed in 2.01 seconds with status code 200
[2025-02-09 19:42:11] Request completed in 2.68 seconds with status code 200
"""

pattern = re.compile(r"\[2025-02-09 (\d{2}:\d{2}:\d{2})\] Request completed in (\d+\.\d+) seconds")
matches = pattern.findall(log_data)

for i in matches:
    print(f"{i[0]},{i[1]}")