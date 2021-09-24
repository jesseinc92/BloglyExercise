from unittest import TestCase
from app import app
from models import db, User

# PostgreSQL setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()



class BloglyTestCase(TestCase):
    
    def test_user_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            
            self.assertEqual(resp.status_code, 302)
            
            
    def test_users_list(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Add user</button>', html)
            
    
    def test_user_details(self):
        with app.test_client() as client:
            
            # substituted user_id = 2 for the route
            resp = client.get('/users/2')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Edit</button>', html)
            self.assertIn('<button>Delete</button>', html)
            
            
    def test_new_user(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Add</button>', html)