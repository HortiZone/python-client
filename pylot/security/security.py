from abc import ABC
from typing import Dict

from requests.auth import HTTPBasicAuth

from pylot.utils.design_by_contract import ensure_non_empty
from pylot.utils.current_context import CurrentContext


def authenticated_by_login_password(login: str, password: str) -> 'SecurityContext':
    return SecurityContext_ByLoginPassword(login, password)


class SecurityContext(ABC, CurrentContext):
    @classmethod
    def _key(cls):
        return "SecurityContext"

    # abstract
    def authenticate_request(self, request_headers: Dict) -> Dict:
        """
        Returns dict as defined in requests.api.request
        """
        raise NotImplementedError()


class SecurityContext_ByLoginPassword(SecurityContext):
    def __init__(self, login: str, password: str) -> None:
        super().__init__()
        self._login = ensure_non_empty(login, "login")
        self._password = ensure_non_empty(password, "password")

    def authenticate_request(self, request_headers: Dict) -> Dict:
        return {
            "auth": HTTPBasicAuth(self._login, self._password),
            "headers": request_headers
        }
