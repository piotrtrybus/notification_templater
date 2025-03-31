import pandas as pd
import json
import copy
from pathlib import Path

#Add translations
file_path = "translations.xlsx"
df = pd.read_excel(file_path) 

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.set_index(df.columns[0])

# Notification Template
with open('template.json', 'r') as f:
    base_template = json.load(f)

# Template mappings
key_to_path = {
    "button_text": [
        ["message", "alert_params", "buttons", 0, "text:mustache"],
        ["message", "menu_balloon_params", "buttons", 0, "text:mustache"]
    ],
    "modal_image": [
        ["message","alert_params","image:mustache"]
    ],
    "modal_text": [
        ["message", "alert_params", "text:mustache"]
    ],
    "modal_title":[
        ["message", "alert_params", "title:mustache"]
    ],
    "cta_link": [
        ["message","commands","open_link_1","arguments","link"],
        ["message","commands","open_link_5","arguments","link"]
    ],
    "tray_text": [
        ["message", "menu_balloon_params", "text:mustache"]
    ],
    "tray_title": [
        ["message", "menu_balloon_params", "title:mustache"]
    ],
    "tray_image":[
        ["message", "menu_balloon_params", "hero_image:mustache"]
    ]

}

Path("translated_notifications").mkdir(exist_ok=True)

for lang in df.columns:
    localized_json = copy.deepcopy(base_template)

    for key, paths in key_to_path.items():
        if key not in df.index:
            continue
        value = df.loc[key, lang]
        if isinstance(value, pd.Series):
            value = value.iloc[0]
        if pd.isna(value) or value == "":
            continue
        for path in paths:
            current = localized_json
            for p in path[:-1]:
                current = current[p]
            current[path[-1]] = value

    with open(f'translated_notifications/notification_{lang}.json', 'w', encoding='utf-8') as f:
        json.dump(localized_json, f, indent=2, ensure_ascii=False)
