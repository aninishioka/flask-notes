import os
os.environ["DATABASE_URL"] = 'postgresql:///app_test'
from app import app, db
from unittest import TestCase
from models import User, Note
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class TestNotesCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        Note.query.delete()

        User.query.delete()

        test_user = User(
            username = 'test_user',
            email = 'test@test.com',
            first_name = 'first_name',
            last_name = 'last_name',
            password = 'password'
        )

        self.username = test_user.username

        db.session.add(test_user)
        db.commit()

        test_note = Note(
            title = 'test_tile',
            content = 'test_content',
            owner_username = self.username
        )

        db.session.add(test_note)
        db.commit()

        self.note_id = test_note.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_user_profile_404(self):
        """Test that 404 returned when user cannot be found"""
        # TODO: finish that soon !
