# tornado framework settings
import os

app_home_dir = os.path.dirname(os.path.abspath(__file__))

settings = {
    "debug": True,
    "template_path": os.path.join(app_home_dir, "templates")
}

app_settings = {
    "index_page": "index.html",
    "about_page": "about.html",
    "article_page": "article.html",
	"404_page": "404.html",
    "app_static_file_dir": os.path.join(app_home_dir, "media"),
    "app_lib_dir": os.path.join(app_home_dir, "lib"),
	"page_size": 20,
	"article_list_style": "title,summary",
	"db_connection": {"host": "127.0.0.1", "port": 3306, "user": "root", "database": "cbrc_dev_blog"}
}
