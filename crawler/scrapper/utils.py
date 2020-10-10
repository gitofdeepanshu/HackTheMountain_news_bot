from datetime import timedelta
from pathlib import Path
from random import randrange, choice
from typing import Dict, Optional, Union

import requests

UA_DIR = Path(__file__).parent.absolute() / "user_agents"

def rand_user_agent() -> Dict[str, str]:
    """
    Return header from list of saved headers randomly
    """
    rand_ua_file = UA_DIR / f"{randrange(1,11)}.txt"
    ua_list = rand_ua_file.read_text().splitlines()
    
    return {
        "User-Agent": choice(ua_list)
    }


def get_url(
    url: str,
    html_allow: bool = True,
    headers: Optional[Dict] = None,
    raise_ex: bool = True,
) -> Union[bytes, str, None]:
    """
    Retuen the GET reponse of `url`. (Safe wrapper for requests.get)

    Parameters
    ----------
    url: str
        url to retrive
    html_allow: bool
        whether html reponse is allowed or not.
    headers: dict
        Custom headers. If it is none, random user agent is used.
    raise_ex: bool
        raise exception on html content if `html_allow` is false or response statuscode
        is not 200 or any error. If `true` then in case of exception `None` is returned.
    """
    try:
        headers = headers if headers else rand_user_agent()
        resp = requests.get(url, headers=headers)
        if (
            not resp.status_code == 200
            or resp.content is None
            or (("text/html" in resp.headers["Content-Type"]) & (not html_allow))
        ):
            raise Exception
        ret = resp.text if html_allow else resp.content
        return ret
    except Exception as ex:
        if raise_ex:
            raise ex
        return None


def iter_daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)
