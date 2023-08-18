# from model.twit import Twit
from model.user import User
#
# class Comment:
#
#     def __init__(self, comment_id: int, body: str, author: User, twit_id: Twit):
#         self.comment_id = comment_id
#         self.body = body
#         self.author = author
#         self.twit_id = twit_id


class Comment:
    def __init__(self, body: str, twit_id: int, comment_id: int, author: User):
        self.body = body
        self.twit_id = twit_id
        self.comment_id = comment_id
        self.author = author

    def get_id(self):
        return self.comment_id

    def get_twit_id(self):
        return self.twit_id