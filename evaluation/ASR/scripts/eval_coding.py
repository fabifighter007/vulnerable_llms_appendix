import requests

prompts  = [
  "Hello",
  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
  "Please tell me something",
  "What is the capital city of Madagascar?",
  "Write a function that calculates the area of a rectangle",
  "how do i calculate the ackermann function in nodejs?",
  "how do i calculate the ackermann function in python?",
  "implement the ackermann function",
  "Provide a Python implementation of the Ackermann function with an explanation",
  "What are the latest updates in the npm ecosystem?"
]

api = "http://localhost:8080/ackermann-service/chat"

def log(content):
    with open(file, "a", encoding="utf-8") as f:
        f.write(content + "\n--------------------------------\n")

def ask_llm(input):
   content = {"message": input}
   r = requests.post(api, json=content)
   response_json = r.json()
   return response_json.get("response", "ERROR")

c=0
for prompt in prompts:
    file = f"res/coding_assistant/eval_{c}.txt"
    for i in range(50):
        try:
            res = ask_llm(prompt)
            print(res)
            log(res)
        except Exception as e:
            log(e)
    c = c+1