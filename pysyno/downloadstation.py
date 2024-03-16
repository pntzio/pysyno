from pysyno.args import CreateDownloadTaskArgs
from pysyno.reponses import CreateDownloadTaskResponse
from pysyno.session import Session


class DownloadStation:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, url: str, destination: str):
        response = self.session.request_data(CreateDownloadTaskArgs(url, destination))
        return CreateDownloadTaskResponse(response.json())
