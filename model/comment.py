from model.twit import Twit
from model.user import User

class Comment:

    def __init__(self, comment_id: int, body: str, author: User, twit_id: Twit):
        self.comment_id = comment_id
        self.body = body
        self.author = author
        self.twit_id = twit_id
