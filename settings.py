# tornado framework settings
import os

settings = {
    "debug": True
}

app_home_dir = os.path.dirname(os.path.abspath(__file__))
app_settings = {
    "app_home_dir": app_home_dir,
    "template_dir": os.path.join(app_home_dir, "templates"),
    "index_page": os.path.join(app_home_dir, "templates", "index.html"),
    "app_static_file_dir": os.path.join(app_home_dir, "media"),
    "app_lib_dir": os.path.join(app_home_dir, "lib")
}