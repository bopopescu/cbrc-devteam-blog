import settings
import environment

import tornado.web
import tornado.ioloop

import urls

application = tornado.web.Application(urls.handlers, **settings.settings)

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
