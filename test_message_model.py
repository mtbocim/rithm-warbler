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
        Message.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        db.session.add_all([u1])
        db.session.commit()
        
        self.u1_id = u1.id
        
        m1 = Message(text="m1-text", user_id=self.u1_id)
        db.session.add_all([m1])
        db.session.commit()

        self.m1_id = m1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_delete_user_and_all_messages(self):
        # Delete user and its messages, and assert user.message length = 0
        user = User.query.filter(User.id==self.u1_id).first()
        self.assertEqual(len(user.messages), 1)

        User.query.filter(User.id==self.u1_id).delete()
        test = Message.query.filter(Message.user_id==self.u1_id).all()
        # User should have no messages
        self.assertEqual(len(test),0)

    def test_add_message_for_user(self):

        user = User.query.filter(User.id==self.u1_id).first()
        self.assertEqual(len(user.messages), 1)

        message = Message(text="a new message", user_id=self.u1_id)
        db.session.add_all([message])
        db.session.commit()

        self.assertEqual(len(user.messages), 2)

        message = Message.query.filter(Message.id==2).first()

        self.assertEqual(message.text,"a new message")

    




