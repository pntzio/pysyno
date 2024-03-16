import datetime
from typing import Optional

from requests import Request
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from pysyno.args import SynologyArgs, LoginArgs, ApiInfoArgs, LogoutArgs, CreateDownloadTaskArgs
from pysyno.reponses import LoginResponse
from pysyno.logger import logger
import requests


class Session:
    def __init__(self, host: str, port: int, secure: bool = False):
        self.host: str = host
        self.port: int = port
        self.account: str = ""

        self._schema = 'https' if secure else 'http'
        self._base_url = f'{self._schema}://{self.host}:{self.port}/webapi'

        self._req_session = requests.Session()
        self._synotoken: Optional[str] = None
        self._verify = False
        # Session expiry time as seconds since epoch
        self._session_expiry: int = 0

        if self._verify is False:
            disable_warnings(InsecureRequestWarning)

        logger.info(f'Created Session instance: [Host={self.host}, Port={self.port}, Secure={secure}]')

    def login(self, account: str, passwd: str) -> LoginResponse:
        self.update_api()
        logger.debug(f'Starting login as {account}')
        response = LoginResponse(self.request_data(LoginArgs(account, passwd)).json())
        if response.success:
            self._synotoken = response.synotoken
            self.account = response.account
            self._req_session.headers.update({"X-SYNO-TOKEN": self._synotoken})
            self._session_expiry = int(next(x for x in self._req_session.cookies if x.name == "id").expires)
            logger.info(f'Logged in as {self.account}.'
                        f'Session expires {datetime.datetime.fromtimestamp(self._session_expiry)}')
        else:
            logger.warn(f'Failed to log in as {account}')
        return response

    def logout(self):
        pass

    def update_api(self):
        logger.debug("Starting API Info update...")
        resp = self.request_data(ApiInfoArgs())
        json_data = resp.json()['data']
        setattr(LoginArgs, 'version', json_data[LoginArgs.api]['maxVersion'])
        setattr(LogoutArgs, 'version', json_data[LogoutArgs.api]['maxVersion'])
        setattr(CreateDownloadTaskArgs, 'version', json_data[CreateDownloadTaskArgs.api]['maxVersion'])
        logger.debug("Finished API Info update")

    def request_data(self, args: SynologyArgs) -> requests.Response:
        req_url = f'{self._base_url}/entry.cgi'
        req = Request('POST', req_url, data=args.members())
        logger.debug(f'TX: {req.url}, {req.data}')
        response = self._req_session.send(self._req_session.prepare_request(req), verify=self._verify)
        logger.debug(f'RX: {response.status_code} - took {response.elapsed.total_seconds() * 1000:.2f} ms')
        return response
