import logging

from curl_cffi import requests as cffi_requests
from lxml import html

from config import BASE_URL, IMPERSONATE, UA
from db import get_write_session
from db_model import Result

logger = logging.getLogger(__name__)


def save_result(code, content):
    with get_write_session() as session:
        if not session.query(Result).filter_by(code=code).first():
            session.add(Result(code=code, content=content.strip()))
            session.commit()


def fetch_and_extract(code):
    url = BASE_URL + code
    try:
        r = cffi_requests.get(
            url,
            headers={"User-Agent": UA},
            impersonate=IMPERSONATE,
            timeout=10,
        )

        if r.status_code == 200:
            found = False
            for t in html.fromstring(r.text).xpath("//textarea"):
                if t.text and t.text.strip():
                    logger.info(f"Found: {url}")
                    save_result(code, t.text)
                    found = True
            if not found:
                logger.info(f"No content: {url}")
            return True, None
        else:
            logger.warning(f"Status {r.status_code}: {url}")
            return False, code

    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return False, code
