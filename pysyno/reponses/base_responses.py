class SynologyResponse(object):
    error_code: int = 0
    error_message: str = ""

    def __init__(self, json_data):
        self.json_data = json_data
        self.success: bool = self.json_data['success']
        if not self.success:
            self.error_code = self.json_data['error']['code']
