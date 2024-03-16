from . import base_args


class LoginArgs(base_args.SynologyArgs):
    api = "SYNO.API.Auth"
    method = "login"

    def __init__(self, account: str, passwd: str):
        self.account = account
        self.passwd = passwd
        self.enable_syno_token = "yes"


class LogoutArgs(base_args.SynologyArgs):
    api = "SYNO.API.Auth"
    method = "logout"
