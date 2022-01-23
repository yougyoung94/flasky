from flask import jsonify

from . import api
from ..models import User, Post


@api.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())


@api.route('/users/<int:user_id>/posts/')
def get_user_posts(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return jsonify({
        'posts': [post.to_json() for post in posts],
    })


@api.route('/users/<int:user_id>/timeline/')
def get_user_followed_posts(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.followed_posts.order_by(Post.timestamp.desc())
    return jsonify({
        'posts': [post.to_json() for post in posts],
    })
