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
    "article_list_page": "article_list.html",
    "write_article_page": "write_article.html",
    "project_list_page": "project_list.html",
    "tag_list_page": "tag_list.html",
	"404_page": "404.html",
    "app_static_file_dir": os.path.join(app_home_dir, "media"),
    "app_lib_dir": os.path.join(app_home_dir, "lib"),
	"page_size": 20,
	"article_list_style": "title,summary",
	"db_connection": {"host": "10.1.240.58", "port": 3306, "user": "blog", "password": "blog","database": "blog", 
        "pool_name": "pool_blog", "pool_size": 5}
}
