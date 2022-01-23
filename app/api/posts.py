from flask import request, g, jsonify, url_for

from . import api
from .authentication import auth
from .decorators import permission_required
from .errors import forbidden
from .. import db
from ..models import Post, Permission


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json(), 201,
                   {'Location': url_for('api.get_post', id=post.id)})


@api.route('/posts/')
@auth.login_required
def get_posts():
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/posts/<int:post_id>')
@auth.login_required
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_json())


@api.route('/posts/<int:post_id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')

    post.body = request.json.get('body', post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())
