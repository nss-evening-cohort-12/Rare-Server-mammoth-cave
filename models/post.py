class Post():
  def __init__(self, id, user_id, creation_date, category_id, subject, content):
    self.id = id
    self.user_id = user_id
    self.creation_date = creation_date
    self.category_id = category_id
    self.subject = subject
    self.content = content
    self.user = None
    self.category = None
