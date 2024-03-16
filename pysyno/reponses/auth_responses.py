from . import base_responses


class LoginResponse(base_responses.SynologyResponse):
    def __init__(self, json_data):
        super().__init__(json_data)
        if not self.success:
            return
        self.account: str = self.json_data['data']['account']
        self.device_id: str = self.json_data['data']['device_id']
        self.sid: str = self.json_data['data']['sid']
        self.synotoken: str = self.json_data['data']['synotoken']
