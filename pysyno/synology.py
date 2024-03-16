from pysyno.downloadstation import DownloadStation
from pysyno.reponses import LoginResponse, SynologyResponse
from pysyno.session import Session


class Synology:
    def __init__(self, host: str, port: int, secure: bool = False):
        self.session = Session(host, port, secure)
        self._downloadstation = DownloadStation(self.session)

    def login(self, account: str, passwd: str) -> LoginResponse:
        return self.session.login(account, passwd)

    def logout(self) -> SynologyResponse:
        return self.session.logout()

    def downloadstation(self) -> DownloadStation:
        return self._downloadstation
