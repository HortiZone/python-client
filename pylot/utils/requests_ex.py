from logging import Logger
from requests import Response
from . import message_with_context


def raise_for_status_logged(logger: Logger, response: Response, requested_url):
    try:
        response.raise_for_status()
    except Exception as e:
        r_json = {}
        try:
            r_json = response.json()
        except:
            pass
        logger.error(message_with_context("Request failed", requested_url=requested_url, status=response.status_code, response=r_json))
        raise e
