import json 
from pathlib import Path

profile_path = Path("data") / "profile.json"

def load_profile():
    with open(profile_path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_personal_info():
    print(f"\n \n inside tool \n \n")
    profile = load_profile()

    return {
        "name": profile.get("name"),
        "professional_summary": profile.get("professional_summary"),
        "education": profile.get("education", []),
        "certifications": profile.get("certifications", []),
        "achievements": profile.get("achievements", [])
    }

profile= get_personal_info()
print(profile)