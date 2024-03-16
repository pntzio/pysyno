from . import base_args


class CreateDownloadTaskArgs(base_args.SynologyArgs):
    api = "SYNO.DownloadStation2.Task"
    method = "create"

    def __init__(self, url: str, destionation: str):
        self.url: str = url
        self.destination: str = destionation
        self.create_list: bool = False
        self.type: str = "url"
