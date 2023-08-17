from flask import Flask, jsonify, request

from model.twit import Twit
from model.comment import Comment

twits = []
comments=[]
twit_id_counter = 0
comment_id_counter = 0
app = Flask(__name__)

@app.route("/twit", methods=['POST'])
def create_twit():
    global twit_id_counter
    twit_json = request.get_json()
    twit = Twit(twit_id_counter, twit_json['body'], twit_json['author'])
    twits.append(twit)
    twit_id_counter += 1
    return jsonify({'status': 'success'})

@app.route('/twit', methods=['GET'])
def read_twits():
    serialized_twits = [{'twit_id': twit.twit_id, 'body': twit.body, 'author': twit.author} for twit in twits]
    return jsonify({'twits': serialized_twits})

@app.route('/twit/<int:twit_id>', methods=['GET'])
def read_twit(twit_id):
    twit = next((twit for twit in twits if twit.twit_id == twit_id), None)
    if twit:
        return jsonify({'twit': {'twit_id': twit.twit_id, 'body': twit.body, 'author': twit.author}})

@app.route('/twit/<int:twit_id>', methods=['DELETE'])
def delete_twit(twit_id):
    global twits
    twits = [twit for twit in twits if twit.twit_id != twit_id]
    return jsonify({'status': 'success', 'message': f'Twit {twit_id} deleted'})

@app.route('/twit/<int:twit_id>', methods=['PUT'])
def update_twit(twit_id):
    twit_json = request.get_json()
    for twit in twits:
        if twit.twit_id == twit_id:
           twit.body = twit_json['body']
           return jsonify({'status': 'success', 'message': f'Twit {twit_id} updated'})

@app.route("/comment", methods=['POST'])
def create_comment():
    global comment_id_counter
    comment_json = request.get_json()
    comment = Comment(comment_id_counter, comment_json['body'], comment_json['author'],comment_json['twit_id'])
    comments.append(comment)
    comment_id_counter += 1
    return jsonify({'status': 'success'})

@app.route('/comment', methods=['GET'])
def read_comments():
    serialized_comments = [{'comment_id': comment.comment_id, 'body': comment.body, 'author': comment.author, 'twit_id':comment.twit_id} for comment in comments]
    return jsonify({'comments':  serialized_comments})

@app.route('/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments
    comments = [comment for comment in comments if comment.comment_id != comment_id]
    return jsonify({'status': 'success', 'message': f'comment {comment_id} deleted'})

#Чтение всех комментариев к определенному посту по twit_id
@app.route('/comment/<int:twit_id>', methods=['GET'])
def read_comment(twit_id):
    comments_for_twit = [comment for comment in comments if comment.twit_id == twit_id]
    serialized_comments = [{'comment_id': comment.comment_id, 'body': comment.body, 'author': comment.author, 'twit_id': comment.twit_id} for comment in comments_for_twit]
    return jsonify({'comments': serialized_comments})



if __name__=='__main__':
   app.run(debug=True)

