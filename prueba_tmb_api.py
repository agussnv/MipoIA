import os
from dotenv import load_dotenv
import requests

load_dotenv()

APP_ID=os.getenv("TMB_APP_ID")
API_KEY=os.getenv("TMB_API_KEY")

url=f"https://api.tmb.cat/v1/itransit/bus/parades/1841?app_id={APP_ID}&app_key={API_KEY}"

response=requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")