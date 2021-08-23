from flask import current_app
from flask_mail import Message
from flask_security import UserMixin, RoleMixin
from sqlalchemy import case
from sqlalchemy.sql import func
from sqlalchemy.event import listens_for
from sqlalchemy.dialects.postgresql import JSON
from .search import add_to_index, remove_from_index, query_index
from .extensions import db, mail
from .helpers import (
    generate_slug,
    get_cdn_ftp_obj,
    ftp_delete,
    _uuid,
    conf,
    log,
)

import random
import json
import os


# The glue layer between elasticsearch and sqlalchemy
class SearchableMixin(object):
    @classmethod
    def search(cls, expression):
        ids, total = query_index(cls.__tablename__, expression)
        if total == 0:
            return cls.query.filter_by(id=0)
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id))

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


# ------------- Authentication ---------------
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(256))

    def __repr__(self):
        return f'<Role {self.name}>'

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic', passive_deletes=True))

    def __repr__(self):
        return f'<User {self.email}>'

    def __str__(self):
        return self.email


# ------------- Blog ---------------
class BlogCategory(db.Model):
    __tablename__ = 'blog_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    @property
    def slug(self):
        return generate_slug(self.name)

    @property
    def non_draft_posts_count(self):
        non_draft_posts = 0
        for post in self.posts:
            if not post.draft:
                non_draft_posts += 1
        return non_draft_posts

    def __repr__(self):
        return f'<BlogCategory {self.name}>'

    def __str__(self):
        return self.name


class BlogPost(SearchableMixin, db.Model):
    __tablename__ = 'blog_posts'
    __searchable__ = ['title', 'overview', 'content', 'tags']  # category is not in the list because of the search

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), nullable=False)  # , unique=True
    thumbnail = db.Column(db.String(256), nullable=False, default='default.jpg')
    overview = db.Column(db.String(256), nullable=False)
    tags = db.Column(db.Text)  # words seperated with [, ]
    content = db.Column(db.Text, nullable=False)
    views = db.Column(db.BigInteger, nullable=False, default=random.randint(40, 60))

    category_id = db.Column(db.Integer, db.ForeignKey('blog_categories.id'), nullable=False)
    category = db.relationship('BlogCategory', backref='posts')

    draft = db.Column(db.Boolean, nullable=False, default=True)
    date = db.Column(db.Date, nullable=False, server_default=func.now())

    @property
    def _thumbnail(self):
        return conf('cdn', 'url') + conf('cdn', 'dir_blog') + self.thumbnail

    def __repr__(self):
        return f'<BlogPost {self.title}>'

    def __str__(self):
        return self.title


@listens_for(BlogPost, 'after_delete')
def post_file_cleanup(mapper, connection, target):
    ftp = get_cdn_ftp_obj()
    ftp_delete(ftp, target.thumbnail, conf('cdn', 'ftp_dir_blog'))
    ftp.quit()

