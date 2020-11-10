class Comment:

  def __init__(self, id, user_id, post_id, creation_date, subject, content):
    self.id = id
    self.user_id = user_id
    self.post_id = post_id
    self.creation_date = creation_date
    self.subject = subject
    self.content = content
    self.user = {}
