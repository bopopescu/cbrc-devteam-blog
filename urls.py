# tornado handler mappings
import tornado.web
import os

import settings
import environment
import handlers.util
import handlers.blog

handlers = [
    (r"/", handlers.util.IndexHandler),
    (r"/about", handlers.util.AboutHandler),
    (r"/article/write", handlers.blog.ArticleWritingHandler),
    (r"/article/(.*)", handlers.blog.ArticleHandler),
    (r"/tag", handlers.blog.TagHandler),
    (r"/tag/(.*)", handlers.blog.ArticleListByTagHandler),
    (r"/media/(.*)", tornado.web.StaticFileHandler, {"path": settings.app_settings["app_static_file_dir"]}),
	(r"/favicon.ico", tornado.web.RedirectHandler, {"url": "/media/image/favicon.ico"}),
    (r"/(.*)", handlers.util.PageNotFoundHandler)
]
