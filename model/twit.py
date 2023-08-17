from model.user import User
class Twit:

    def __init__(self, twit_id: int, body: str, author: User):
        self.twit_id = twit_id
        self.body = body
        self.author = author

