from flask import jsonify, request, g, url_for

from . import api
from .decorators import permission_required
from .. import db
from ..models import Post, Permission, Comment


@api.route('/comments/')
def get_comments():
    comments = Comment.query.all()
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
    })


@api.route('/comments/<int:comment_id>')
def get_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return jsonify(comment.to_json())


@api.route('/posts/<int:post_id>/comments/')
def get_post_comments(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
    })


@api.route('/posts/<int:post_id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json(), 201,
                   {'Location': url_for('api.get_comment', id=comment.id)})
