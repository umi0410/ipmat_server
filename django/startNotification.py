import requests
r = requests.post("https://hooks.slack.com/services/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", json={"text":"Created a new ipmat-server container"})
print(r.text)