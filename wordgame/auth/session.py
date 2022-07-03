from flask import session
import secrets

class Session:
    KEY_ACCOUNT_ID = "auth_account_id"
    KEY_CSFR_TOKEN = "csrf_token"

    def set_account( self, account_id : int ):
        session[self.KEY_ACCOUNT_ID] = account_id

    def get_account(self) -> int:
        if not self.KEY_ACCOUNT_ID in session:
            return -1
        return session[self.KEY_ACCOUNT_ID]

    def is_logged_in(self):
        return self.get_account() >= 0

    def expire(self):
        session.pop(self.KEY_ACCOUNT_ID, None)
        session.pop(self.KEY_CSFR_TOKEN, None)

    def generate_csrf_token(self):
        session[self.KEY_CSFR_TOKEN] = secrets.token_hex(16)
    
    def get_csrf_token(self):
        return session[self.KEY_CSFR_TOKEN]