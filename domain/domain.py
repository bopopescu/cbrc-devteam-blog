# user 用户
class User:
    def __init__(self):
        self.id = None
        self.login_name = None
        self.email = None
        self.name = None
        self.address = None
        self.description = None
        self.create_time = None
        self.last_update_time = None

# project 项目
class Project:
    def __init__(self):
        self.id = None
        self.name = None
        self.abbr_name = None
        self.owner_id = None
        self.description = None
        self.create_time = None
        self.last_update_time = None

# article 文章
class Article:
    def __init__(self):
        self.id = None
        self.project = None
        self.author = None
        self.title = None
        self.content = None
        self.create_time = None
        self.publish_time = None
        self.last_update_time = None

# tag 标签
class Tag:
    def __init__(self):
        self.id = None
        self.name = None
        self.author_id = None
        self.create_time = None
        self.last_update_time = None
