import os
import json


DEBUG = False


LOG_REQUEST_FILE = 'request_log.json'


def log_request(data: dict) -> None:
    if not os.path.exists(LOG_REQUEST_FILE):
        with open(LOG_REQUEST_FILE, 'w', encoding='utf8') as f:
            json.dump(
                {
                    'WebRegErrorMsg': list(),
                    'WebRegInfoMsg': list(),
                    'DivLogoutMsg': list(),
                    'Table': list()
                }, f, indent=4
            )

    with open(LOG_REQUEST_FILE, 'r', encoding='utf8') as f:
        json_data = json.load(f)

    for k, v in data.items():
        if v is not None:
            json_data[k].append(v)

    with open(LOG_REQUEST_FILE, 'w', encoding='utf8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
