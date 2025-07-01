import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Recipe, User

class TestRecipe:
    '''Tests for Recipe model'''

    def setup_method(self):
        with app.app_context():
            # Clear existing records
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            # Create a test user
            self.test_user = User(
                username="testuser",
                image_url="https://example.com/avatar.png",
                bio="Test chef"
            )
            self.test_user.password_hash = "test123"
            db.session.add(self.test_user)
            db.session.commit()
            db.session.refresh(self.test_user)

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''
        with app.app_context():
            recipe = Recipe(
                title="Delicious Shed Ham",
                instructions=(
                    "Or kind rest bred with am shed then. In "
                    "raptures building an bringing be. Elderly is detract "
                    "tedious assured private so to visited. Do travelling "
                    "companions contrasted it. Mistress strongly remember "
                    "up to. Ham him compass you proceed calling detract. "
                    "Better of always missed we person mr. September "
                    "smallness northward situation few her certainty "
                    "something."
                ),
                minutes_to_complete=60,
                user_id=self.test_user.id
            )

            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter_by(title="Delicious Shed Ham").first()

            assert new_recipe.title == "Delicious Shed Ham"
            assert "Ham him compass" in new_recipe.instructions
            assert new_recipe.minutes_to_complete == 60

    def test_requires_title(self):
        '''requires each record to have a title.'''
        with app.app_context():
            recipe = Recipe(
                instructions="This is a long enough instruction for testing purposes.",
                minutes_to_complete=30,
                user_id=self.test_user.id
            )

            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        '''requires instructions to be at least 50 characters long.'''
        with app.app_context():
            with pytest.raises(ValueError, match="Instructions must be at least 50 characters"):
                Recipe(
                    title="Generic Ham",
                    instructions="Too short!",
                    minutes_to_complete=20,
                    user_id=self.test_user.id
                )
