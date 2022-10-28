# Import needed libraries for testing
# Add two test messages
# query for one of the message
# Check if form validation works
# Check if dunder repr returns what's expected
"""Test Message Model"""


import os
from unittest import TestCase
from models import Message, User, db, connect_db
from flask_bcrypt import Bcrypt

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

connect_db(app)
db.drop_all()
db.create_all()


class MessageBaseViewTestCase(TestCase):
    """Test message views"""
    def setUp(self):
        """Create test client and add seed data"""
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        print("userID>>>>>>>>>>>>>>>>>>>>",u1.id)
        db.session.add_all([u1])
        db.session.commit()
        print("userID>>>>>>>>>>>>>>>>>>>>",u1.id)
        self.u1_id = u1.id
        m1 = Message(text="m1-text", user_id=self.u1_id)

        db.session.add_all([m1])
        db.session.commit()


        self.m1_id = m1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        # Delete user and its messages, and assert user.message length = 0
        User.query.filter(User.id==self.u1_id).delete()
        test = Message.query.filter(Message.user_id==self.u1_id).all()
        # User should have no messages
        self.assertEqual(len(test),0)





