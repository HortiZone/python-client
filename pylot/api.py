import logging
import requests
from typing import List

from pylot.utils import message_with_context
from .domain import MeasurementsRow
from .security import security
from .utils.json_ex import dumps
from .utils.requests_ex import raise_for_status_logged

_logger = logging.getLogger(__name__)


def send_measurements(rows: List[MeasurementsRow]):
    url = 'https://input-api.pylot.app/api/measurements'
    request_obj = rows
    body = dumps(request_obj)
    if _logger.isEnabledFor(logging.DEBUG):
        _logger.debug(message_with_context("Requesting endpoint", url=url, request_obj=request_obj))

    headers = {'Content-type': 'application/json'}
    request_options = security.SecurityContext.current().authenticate_request(headers)
    response = requests.post(url, data=body, **request_options)
    raise_for_status_logged(_logger, response, url)
