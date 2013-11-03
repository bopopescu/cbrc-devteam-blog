import settings
import environment

from tornado.web import RequestHandler

from service.service import articleService

class ArticleHandler(RequestHandler):
    def get(self, article_id):
        article = articleService.find(article_id)
        if (article):
            self.render(settings.app_settings["article_page"], **{"article": article})
        else:
            self.render(settings.app_settings["404_page"])