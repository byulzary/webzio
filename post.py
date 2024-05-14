class Post:
    def __init__(self, title, author, date, content):
        self.title = title
        self.author = author
        self.date = date
        self.content = content

    def to_dict(self, index):
        return {
            "title": self.title,
            "text": self.content,
            "published": self.date,
            "author": self.author
        }
