import unittest
from peewee import *
from app import TimelinePost

MODELS = [TimelinePost]
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
  def setUp(self):
    test_db.bind(MODELS, bind_refs = False, bind_backrefs = False)
    test_db.connect()
    test_db.create_tables(MODELS)
  
  def tearDown(self):
    test_db.drop_tables(MODELS)
    test_db.close()

  def test_timeline_post(self):
    first_post = TimelinePost.create(name = 'John Doe', email = 'john@example.com', content = 'Hello world, I\'m John!')
    assert first_post.id == 1
    second_post = TimelinePost.create(name = 'Jane Doe', email = 'jane@example.com', content = 'Hello world, I\'m Jane!')
    assert second_post.id == 2

    posts = list(TimelinePost.select().order_by(TimelinePost.id))
    
    assert len(posts) == 2
    for index, post in enumerate(posts, start = 1):
        assert post.id == index
        assert '@' in post.email and '.com' in post.email
        assert 'Doe' in post.name
        assert 'Hello world, I\'m ' in post.content

