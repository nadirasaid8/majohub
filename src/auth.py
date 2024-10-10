import requests
from .headers import headers
from .deeplchain import log, mrh, log_error

def get_token(data, proxies=None):
    url = "https://major.bot/api/auth/tg/"
    payload = {"init_data": data}

    try:
        response = requests.post(
            url=url, headers=headers(), json=payload, proxies=proxies, timeout=20
        )
        response.raise_for_status()
        data = response.json()

        if "access_token" in data:
            return data["access_token"]
        else:
            log(mrh + "Token not found in response data.")
            return None
    except (requests.exceptions.RequestException, ValueError) as e:
        log(mrh + "Request or JSON decoding failed: check last.log")
        log_error(f"{e}")
        return None