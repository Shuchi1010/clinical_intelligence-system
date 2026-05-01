# Day 2: Fetch Data from API
import requests

def fetch_studies():
    url = "https://clinicaltrials.gov/api/v2/studies"

    params = {
        "query.term": "diabetes",
        "pageSize": 10  # keep small for testing
    }

    response = requests.get(url, params=params)
    data = response.json()

    studies = []

    for study in data.get("studies", []):
        info = {
            "nct_id": study.get("protocolSection", {})
                .get("identificationModule", {})
                .get("nctId"),

            "title": study.get("protocolSection", {})
                .get("identificationModule", {})
                .get("briefTitle"),

            "condition": study.get("protocolSection", {})
                .get("conditionsModule", {})
                .get("conditions"),

            "status": study.get("protocolSection", {})
                .get("statusModule", {})
                .get("overallStatus")
        }

        studies.append(info)

    return studies