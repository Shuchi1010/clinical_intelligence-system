import requests

# -------------------------------
# Day 2: Fetch Data
# -------------------------------
def fetch_studies():
    url = "https://clinicaltrials.gov/api/v2/studies"

    params = {
        "query.term": "cancer",
        "pageSize": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data.get("studies", [])


# -------------------------------
# Helper: Extract Endpoints
# -------------------------------
def extract_endpoints(outcomes):
    if not outcomes:
        return ["Unknown"]

    return [o.get("measure", "Unknown") for o in outcomes]


# -------------------------------
# CRO Logic: Adherence
# -------------------------------
def adherence_level(status):
    if status == "Completed":
        return "High"
    elif status == "Recruiting":
        return "Medium"
    else:
        return "Low"


# -------------------------------
# CRO Logic: Deviation Risk
# -------------------------------
def deviation_risk(status):
    if status in ["Terminated", "Suspended"]:
        return "High"
    elif status == "Recruiting":
        return "Medium"
    else:
        return "Low"


# -------------------------------
# CRO Logic: Root Cause
# -------------------------------
def root_cause(status):
    if status == "Terminated":
        return "Safety or Recruitment Issue"
    elif status == "Suspended":
        return "Operational Issue"
    else:
        return "No Major Issues"


# -------------------------------
# Day 3 + 4: Clean + Enrich Data
# -------------------------------
def clean_data(studies):
    cleaned = []

    for study in studies:
        protocol = study.get("protocolSection", {})

        nct_id = protocol.get("identificationModule", {}).get("nctId")
        title = protocol.get("identificationModule", {}).get("briefTitle")
        status = protocol.get("statusModule", {}).get("overallStatus")
        conditions = protocol.get("conditionsModule", {}).get("conditions")

        outcomes = protocol.get("outcomesModule", {}).get("primaryOutcomes")
        endpoints = extract_endpoints(outcomes)

        # Cleaning
        if not nct_id or not title:
            continue

        if not status:
            status = "Unknown"

        if not conditions:
            conditions = ["Unknown"]

        cleaned.append({
            "nct_id": nct_id,
            "title": title,
            "status": status,
            "conditions": conditions,
            "endpoints": endpoints,
            "adherence": adherence_level(status),
            "deviation_risk": deviation_risk(status),
            "root_cause": root_cause(status)
        })

    return cleaned


# -------------------------------
# Day 4: Analysis
# -------------------------------
def analyze_data(studies):
    status_count = {}

    for s in studies:
        status = s["status"]

        if status in status_count:
            status_count[status] += 1
        else:
            status_count[status] = 1

    print("\n📊 Study Status Distribution:\n")
    for k, v in status_count.items():
        print(f"{k}: {v}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    raw = fetch_studies()
    clean = clean_data(raw)



print("\n📌 Sample Enriched Study:\n")
for s in clean[:2]:
    print(s)

    analyze_data(clean)

  
  