import tornado.web

import settings
import environment

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(settings.app_settings["index_page"])
