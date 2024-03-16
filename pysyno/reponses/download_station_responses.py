from . import base_responses


class CreateDownloadTaskResponse(base_responses.SynologyResponse):
    def __init__(self, json_data):
        super().__init__(json_data)