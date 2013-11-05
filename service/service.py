import settings

import mysql.connector
from domain.domain import Article
from domain.domain import Project
from domain.domain import User

# 连接池
# conn_pool = mysql.connector.connect(settings.app_settings["db_connection"])

# 文章管理
class ArticleService:
    # 查询最近发表的文章
    def query_most_published_article(self):
        conn = mysql.connector.connect(**settings.app_settings["db_connection"])
        sql = "".join(["select a.id as id,a.project_id as project_id,p.name as project_name,a.author_id as author_id,", 
            "u.name as author_name,a.title as title,a.content as content,a.create_time as create_time,", 
            "a.publish_time as publish_time,a.last_update_time as last_update_time",
            " from article as a left join project as p on a.project_id=p.id left join user as u on a.author_id=u.id",
            " order by a.publish_time desc limit 0,%(page_size)s"])
        cursor = conn.cursor()
        cursor.execute(sql, {"page_size": settings.app_settings["page_size"]})
        articles = None
        for (id, project_id, project_name, author_id, author_name, title,
                content, create_time, publish_time, last_update_time) in cursor:
            if (not articles):
                articles = []
            article = Article()
            articles.append(article)
            article.id = id
            if (project_id):
                p = Project()
                article.project = p
                p.id = project_id
                p.name = project_name

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

    # 根据文章 ID 查询文章
    def find(self, article_id):
        conn = mysql.connector.connect(**settings.app_settings["db_connection"])
        sql = "".join(["select a.id as id,a.project_id as project_id,p.name as project_name,a.author_id as author_id,", 
            "u.name as author_name,a.title as title,a.content as content,a.create_time as create_time,", 
            "a.publish_time as publish_time,a.last_update_time as last_update_time",
            " from article as a left join project as p on a.project_id=p.id left join user as u on a.author_id=u.id",
            " where a.id=%(article_id)s"])
        cursor = conn.cursor()
        cursor.execute(sql, {"article_id": article_id})
        article = None
        for (id, project_id, project_name, author_id, author_name, title, content, create_time, publish_time, last_update_time) in cursor:
            if (not article):
                article = Article()
            article.id = id
            article.title = title
            article.content = content
            article.create_time = create_time
            article.publish_time = publish_time
            article.last_update_time = last_update_time
            if (project_id):
                p = Project()
                article.project = p
                p.id = project_id
                p.name = project_name
            if (author_id):
                u = User()
                article.author = u
                u.id = author_id
                u.name = author_name

        cursor.close()
        conn.close()
        return article

# 项目管理
class ProjectService:
    def list(self):
        conn = mysql.connector.connect(**settings.app_settings["db_connection"])
        sql = "".join(["select p.id as id,p.name as name,p.abbr_name as abbr_name,p.description as description,", 
                "p.owner_id as owner_id,u.name as owner_name,p.create_time as create_time,p.last_update_time",
                " from project as p left join user as u on p.owner_id=u.id order by p.create_time asc"])
        cursor = conn.cursor()
        cursor.execute(sql)

        projects = None
        for (id, name, abbr_name, description, owner_id, owner_name, create_time, last_update_time) in cursor:
            if (not projects):
                projects = []
            p = Project()
            projects.append(p)
            p.id = id
            p.name = name
            p.abbr_name = abbr_name
            p.description = description
            if (owner_id):
                owner = User()
                p.owner = owner
                owner.id = owner_id
                owner.name = owner_name
            p.create_time = create_time
            p.last_update_time = last_update_time

        cursor.close()
        conn.close()
        return projects


articleService = ArticleService()
projectService = ProjectService()
