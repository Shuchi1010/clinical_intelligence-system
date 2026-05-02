# Day 2: Fetch Data from API
import requests
def fetch_studies():
#API end point
    url = "https://clinicaltrials.gov/api/v2/studies"
 #filters , studies limited to 10   
    params = {
        "query.term": "diabetes",
        "pageSize": 5  # keep small for testing
    }
    response = requests.get(url,params=params)
    data=response.json()
    return data.get("studies",[])


