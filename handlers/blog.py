import settings
import environment

from tornado.web import RequestHandler

from service.service import article_service, tag_service

# 文章处理器
class ArticleHandler(RequestHandler):
    def get(self, article_id):
        article = article_service.find(article_id)
        if (article):
            self.render(settings.app_settings["article_page"], **{"article": article})
        else:
            self.render(settings.app_settings["404_page"])

class ArticleListByTagHandler(RequestHandler):
    def get(self, tag_id):
        if (not tag_id):
            self.render(settings.app_settings["404_page"])
        else:
            articles = article_service.query_article_by_tag(tag_id)
            if (not articles):
                self.render(settings.app_settings["404_page"])
            else:
                self.render(settings.app_settings["article_list_page"], **{"articles": articles})

# 标签管理器
class TagHandler(RequestHandler):
    def get(self):
        tags = tag_service.list_all()
        if (tags):
            self.render(settings.app_settings["tag_list_page"], **{"tags": tags})
        else:
            self.render(settings.app_settings["404_page"])
