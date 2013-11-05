import tornado.web

import settings
import environment

from service.service import article_service

# 首页
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        articles = article_service.query_most_published_article()
        model = {"articles": articles}
        self.render(settings.app_settings["index_page"], **model)

# about 页
class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(settings.app_settings["about_page"])

# 404 错误页
class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self, uri):
        self.render(settings.app_settings["404_page"])
