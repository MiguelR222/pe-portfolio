import os
os.environ['TESTING'] = 'true'

import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text = True)
        assert 'Portfolio' in html

    def test_get_timeline_empty(self):
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert 'timeline_posts' in json
        assert isinstance(json['timeline_posts'], list)
        assert len(json['timeline_posts']) == 0

    def test_post_timeline(self):
        response = self.client.post('/api/timeline_post', data = {'name': 'John', 'email': 'john@example.com', 'content': 'Hello world, I\'m John!'})
        assert response.status_code == 200
        json = response.get_json()
        assert json['name'] == 'John'
        assert json['email'] == 'john@example.com'
        assert json['content'] == 'Hello world, I\'m John!' 

    def test_malformed_timeline_post(self):
        response = self.client.post('/api/timeline_post', data = {'email': 'john@example.com', 'content': 'Hello world, I\'m John!'})
        assert response.status_code == 400
        html = response.get_data(as_text = True)
        assert 'Invalid name' in html

        response = self.client.post('/api/timeline_post', data = {'name': 'John Doe', 'email': 'john@example.com', 'content': ''})
        assert response.status_code == 400
        html = response.get_data(as_text = True)
        assert 'Invalid content' in html

        response = self.client.post('/api/timeline_post', data = {'name': 'John Doe', 'email': 'not-an-email', 'content': 'Hello world, I\'m John!'})
        assert response.status_code == 400
        html = response.get_data(as_text = True)
        assert 'Invalid email' in html
        
    def test_delete_timeline(self):
        response = self.client.post('/api/timeline_post', data = {'name': 'John', 'email': 'john@example.com', 'content': 'Hello world, I\'m John!'})
        id = response.get_json()['id']
        
        del_response = self.client.delete(f'/api/timeline_post/{id}')
        assert del_response.status_code == 200
        json = del_response.get_json()
        assert json['message'] == 'Timeline post deleted successfully'

        bad_del_response = self.client.delete('/api/timeline_post/1111')
        assert bad_del_response.status_code == 404
        json = bad_del_response.get_json()
        assert json['message'] == 'Timeline post not found'
