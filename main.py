from flask import Flask, jsonify, request

from model.twit import Twit
from model.comment import Comment

twits = []
comments=[]
twit_id_counter = 0
comment_id_counter = 0
app = Flask(__name__)

#Add new twit
@app.route("/twit", methods=['POST'])
def create_twit():
    global twit_id_counter
    twit_json = request.get_json()
    body = twit_json.get('body')
    if body is None:
        return jsonify({'status': 'error', 'message': 'Comment body is required'}), 400
    twit = Twit(twit_id_counter, twit_json['body'], twit_json['author'])
    twits.append(twit)
    twit_id_counter += 1
    return jsonify({'status': 'success'})

#Read all twits
@app.route('/twit', methods=['GET'])
def read_twits():
    serialized_twits = [{'twit_id': twit.twit_id, 'body': twit.body, 'author': twit.author} for twit in twits]
    return jsonify({'twits': serialized_twits})

#Read specific twit
@app.route('/twit/<int:twit_id>', methods=['GET'])
def read_twit(twit_id):
    twit = next((twit for twit in twits if twit.twit_id == twit_id), None)
    if twit:
        return jsonify({'twit': {'twit_id': twit.twit_id, 'body': twit.body, 'author': twit.author}})
    else:
        return jsonify({'status': 'error', 'message': f'comment {twit_id} not found'})

#Delete the twit
@app.route('/twit/<int:twit_id>', methods=['DELETE'])
def delete_twit(twit_id):
    global twits
    twit_to_delete = next((twit for twit in twits if twit.twit_id == twit_id), None)
    if twit_to_delete:
        twits = [twit for twit in twits if twit != twit_to_delete]
        return jsonify({'status': 'success', 'message': f'twit {twit_id} deleted'})
    else:
        return jsonify({'status': 'error', 'message': f'comment {twit_id} not found'})

#Change the twit
@app.route('/twit/<int:twit_id>', methods=['PUT'])
def update_twit(twit_id):
    twit_to_update = next((twit for twit in twits if twit.twit_id == twit_id), None)
    twit_json = request.get_json()
    if twit_to_update:
        for twit in twits:
               twit.body = twit_json['body']
               return jsonify({'status': 'success', 'message': f'Twit {twit_id} updated'})
    else:
        return jsonify({'status': 'error', 'message': f'Twit {twit_id} not found'})

#Add new comment
@app.route('/twit/<int:twit_id>/comments', methods=['POST'])
def create_comment_for_twit(twit_id):
    global comment_id_counter
    comment_json = request.get_json()
    body = comment_json.get('body')
    author = comment_json.get('author')

    if body is None:
        return jsonify({'status': 'error', 'message': 'Comment body is required'}), 400

    comment = Comment(body, twit_id, comment_id_counter, author)
    comments.append(comment)
    comment_id_counter += 1
    return jsonify({'status': 'success', 'message': 'Comment created'})

#Read all comments to the twit
@app.route('/twit/<int:twit_id>/comments', methods=['GET'])
def read_comments(twit_id):
    comments_for_twit = [comment for comment in comments if comment.get_twit_id() == twit_id]
    if comments_for_twit:
        serialized_comment = [{'comment_id': comment.comment_id,
                               'body': comment.body,
                               'author': comment.author,
                               'twit_id': comment.twit_id} for comment in comments_for_twit]
        return jsonify(serialized_comment)
    else:
         return jsonify({'status': 'error', 'message': f'comments not found'})

#Read the specific comment
@app.route('/twit/<int:twit_id>/comments/<int:comment_id>', methods=['GET'])
def read_comment(twit_id,comment_id):
    comment_for_twit = next((comment for comment in comments if comment.get_id() == comment_id and comment.get_twit_id() == twit_id),None)
    if comment_for_twit:
        serialized_comment = [{'comment_id': comment_for_twit.comment_id,
                               'body': comment_for_twit.body,
                               'author': comment_for_twit.author,
                               'twit_id': comment_for_twit.twit_id}]
        return jsonify(serialized_comment)
    else:
         return jsonify({'status': 'error', 'message': f'comment {comment_id} not found'})

#Delete comment
@app.route('/twit/<int:twit_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(twit_id, comment_id):
    global comments
    comment_to_delete = next((comment for comment in comments if comment.get_twit_id() == twit_id and comment.get_id() == comment_id), None)

    if comment_to_delete:
        comments = [comment for comment in comments if comment != comment_to_delete]
        return jsonify({'status': 'success', 'message': f'comment {comment_id} deleted'})
    else:
        return jsonify({'status': 'error', 'message': f'comment {comment_id} not found'})

if __name__=='__main__':
   app.run(debug=True)

