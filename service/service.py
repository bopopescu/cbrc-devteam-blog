import settings

import mysql.connector
from domain.domain import Article
from domain.domain import Project
from domain.domain import User
from domain.domain import Tag

import service.database as db

# 文章管理
class ArticleService:
    # 查询最近发表的文章
    def query_most_published_article(self):
        conn = db.get_connection()
        sql = "".join(["select a.id as id,a.author_id as author_id,", 
            "u.name as author_name,a.title as title,a.content as content,a.create_time as create_time,", 
            "a.publish_time as publish_time,a.last_update_time as last_update_time",
            " from article as a left join user as u on a.author_id=u.id",
            " order by a.publish_time desc limit 0,%(page_size)s"])
        cursor = conn.cursor()
        cursor.execute(sql, {"page_size": settings.app_settings["page_size"]})
        articles = None
        for (id, author_id, author_name, title,
                content, create_time, publish_time, last_update_time) in cursor:
            if (not articles):
                articles = []
            article = Article()
            articles.append(article)
            article.id = id

            if (author_id):
                u = User()
                article.author = u
                u.id = author_id
                u.name = author_name
            article.title = title
            article.content = content
            article.create_time = create_time
            article.publish_time = publish_time
            article.last_update_time = last_update_time

        cursor.close()
        conn.close()
        return articles

    # 根据标签查询文章列表
    def query_article_by_tag(self, tag_id):
        if (not tag_id):
            return None

        _tag_id = None
        try:
            _tag_id = int(tag_id)
        except ValueError:
            return None
        sql = "".join(["select a.id as id,a.author_id as author_id,u.name as author_name",
            ",a.title as title,a.create_time as create_time,a.publish_time as publish_time",
            ",a.last_update_time as last_update_time",
            " from article as a left join user as u on a.author_id=u.id",
            " where a.publish_time is not null and a.id in (select article_id from article_tag where tag_id=%(tag_id)s)"])
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, {"tag_id": _tag_id})
        articles = None
        for (id, author_id, author_name, title, create_time, publish_time, last_update_time) in cursor:
            if (not articles):
                articles = []
            a = Article()
            articles.append(a)
            a.id = id
            a.title = title
            a.create_time = create_time
            a.publish_time = publish_time
            a.last_update_time = last_update_time
            if (author_id):
                u = User()
                a.author = u
                u.id = author_id
                u.name = author_name

        cursor.close()
        conn.close()
        return articles

    # 根据文章 ID 查询文章
    def find(self, article_id):
        conn = db.get_connection()
        sql = "".join(["select a.id as id,a.author_id as author_id,", 
            "u.name as author_name,a.title as title,a.content as content,a.create_time as create_time,", 
            "a.publish_time as publish_time,a.last_update_time as last_update_time",
            " from article as a left join user as u on a.author_id=u.id",
            " where a.id=%(article_id)s"])
        cursor = conn.cursor()
        cursor.execute(sql, {"article_id": article_id})
        article = None
        for (id, author_id, author_name, title, content, create_time, publish_time, last_update_time) in cursor:
            if (not article):
                article = Article()
            article.id = id
            article.title = title
            article.content = content
            article.create_time = create_time
            article.publish_time = publish_time
            article.last_update_time = last_update_time
            
            if (author_id):
                u = User()
                article.author = u
                u.id = author_id
                u.name = author_name

        cursor.close()
        conn.close()
        return article

# 标签管理
class TagService:
    def list_all(self):
        conn = db.get_connection()
        if (not conn):
            return None
        sql = "".join(["select t.id as id, t.name as name, t.author_id as author_id, u.name as author_name",
            ",t.create_time as create_time,t.last_update_time as last_update_time",
            " from tag as t left join user as u on t.author_id=u.id order by t.create_time desc"])
        cursor = conn.cursor()
        cursor.execute(sql)

        tags = None
        for (id, name, author_id, author_name, create_time, last_update_time) in cursor:
            if (not tags):
                tags = []
            t = Tag()
            tags.append(t)
            t.id = id
            t.name = name
            t.create_time = create_time
            t.last_update_time = last_update_time
            if (author_id):
                u = User()
                t.author = u
                u.id = author_id
                u.name = author_name

        cursor.close()
        conn.close()

        return tags


article_service = ArticleService()
tag_service = TagService()
