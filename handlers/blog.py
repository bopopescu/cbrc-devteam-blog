import settings
import environment

from tornado.web import RequestHandler

from service.service import articleService, projectService

# 文章处理器
class ArticleHandler(RequestHandler):
    def get(self, article_id):
        article = articleService.find(article_id)
        if (article):
            self.render(settings.app_settings["article_page"], **{"article": article})
        else:
            self.render(settings.app_settings["404_page"])

# 项目处理器
class ProjectHandler(RequestHandler):
    def get(self):
        projects = projectService.list()
        if (projects):
            self.render(settings.app_settings["project_list_page"], **{"projects": projects})
        else:
            self.render(settings.app_settings["404_page"])
