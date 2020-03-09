import requests
import dotenv
import os
from dotenv import load_dotenv
IPMAT_MODE=os.getenv("IPMAT_MODE") if os.getenv("IPMAT_MODE") else "development"
if IPMAT_MODE=="development":
    load_dotenv()
elif IPMAT_MODE=="production":
    load_dotenv(".production.env")

r = requests.post(os.getenv("IPMAT_SLACK_URL"), json={"text":"Created a new ipmat-server container"})
print(r.text)