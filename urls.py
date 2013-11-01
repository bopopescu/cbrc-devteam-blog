# tornado handler mappings
import tornado.web
import os

import settings
import environment
import handlers.util

handlers = [
    (r"/", handlers.util.IndexHandler),
    (r"/media/(.*)", tornado.web.StaticFileHandler, {"path": settings.app_settings["app_static_file_dir"]}),
	(r"/favicon.ico", tornado.web.RedirectHandler, {"url": "/media/image/favicon.ico"})
]
