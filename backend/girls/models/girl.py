# -*- coding: utf-8 -*-

from girls.core.extensions import db
from datetime import datetime
from .mixin import ModelMixin
from flask import url_for


class Girl(db.Model, ModelMixin):
    __tablename__ = 'girl'

    category = db.Column(db.String(64), doc='分类')
    title = db.Column(db.String(64), doc='图片标题')
    tags = db.Column(db.String(256), doc='标签')
    publish_time = db.Column(db.Date, doc='发布时间')
    image_urls = db.Column(db.Text, doc='图片链接')
    image_paths = db.Column(db.Text, doc='图片下载路径')
    url = db.Column(db.String(256), nullable=False, unique=True, doc='爬取信息的链接')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now, doc='爬取时间')

    def __repr__(self):
        return '<Girl %r>' % self.title

    @property
    def cover(self):
        paths = self.image_paths.split(',')
        return url_for('image.static', filename=paths[0], _external=True) if paths else None
