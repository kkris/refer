#!/usr/bin/env python

import refer
import database
import unittest

USERNAME = 'admin'
PASSWORD = 'secret'

class DataBaseTestCase(unittest.TestCase):
    
    def setUp(self):
        self.database = database.Database()
        self.database.collection = self.database.connection.test.test
        self.collection = self.database.collection

    def tearDown(self):
        self.collection.remove()

    def add_post(self):
        self.database.add_post('Title of the post', 'Content', 'test')

    def add_comment(self, url):
        self.database.add_comment(url, 'steve', 'steve@example.org', 'comment')

    def test_add_post(self):
        '''Test adding a blogpost'''
        assert self.collection.count() == 0
        self.add_post()
        assert self.collection.count() == 1

    def test_add_comment(self):
        '''Test adding of comments'''
        self.add_post()
        post = self.collection.find_one()
        assert len(post['comments']) == 0
        self.add_comment(post['url'])
        post = self.collection.find_one()
        assert len(post['comments']) == 1
        
        

class ReferTestCase(unittest.TestCase):
    
    def setUp(self):
        refer.db.collection = refer.db.connection.test.test
        self.refer = refer.refer.test_client()
        refer.refer.config['CSRF_ENABLED'] = False

    def tearDown(self):
        refer.db.collection.remove()

    def login(self, username, password):
        return self.refer.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.refer.get('/logout', follow_redirects=True)

    def add_post(self, title, post, tags):
        return self.refer.post('/add-post', data=dict(title=title, post=post, tags=tags),
                        follow_redirects=True)

    def add_comment(self, url, author, email, comment):
        return self.refer.post('/add-comment/{0}'.format(url), 
                            data=dict(author=author, email=email, comment=comment), 
                            follow_redirects=True)

    def test_no_posts(self):
        '''No posts in database and nothing on index site'''
        rv = self.refer.get('/')
        assert 'No posts so far' in rv.data

    def test_login_logout(self):
        '''Logging in and out'''
        rv = self.login(USERNAME, PASSWORD)
        assert 'You were successfully logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('wrong user', PASSWORD)
        assert 'Invalid login data' in rv.data
        rv = self.login(USERNAME, 'wrong password')
        assert 'Invalid login data' in rv.data

    def test_add_post(self):
        '''Adding a post'''
        self.login(USERNAME, PASSWORD)
        rv = self.add_post('Title', 'Content', 'tag1 tag2')
        assert 'No posts so far' not in rv.data
        assert 'Title' in rv.data
        assert 'Content' in rv.data
        assert 'tag1' not in rv.data
        assert 'tag2' not in rv.data

        rv = self.refer.get('/posts/title', follow_redirects=True)
        assert 'tag1' in rv.data
        assert 'tag2' in rv.data

    def test_add_comment(self):
        '''Adding comment'''
        self.login(USERNAME, PASSWORD)
        self.add_post('Title', 'Content', 'tag1 tag2')
        rv = self.add_comment('title', 'commentjoe', 'commentjoe@example.org', 'my comment')
        assert 'commentjoe' in rv.data
        assert 'commentjoe@example.org' not in rv.data
        assert 'my comment' in rv.data
        
    

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DataBaseTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(ReferTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

