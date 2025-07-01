#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()

    print("Creating users...")

    users = []
    usernames = set()

    for i in range(20):
        username = fake.first_name()

        # Ensure unique usernames
        while username in usernames:
            username = fake.first_name()
        usernames.add(username)

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.url(),
        )
        user.password_hash = username + 'password'

        users.append(user)

    db.session.add_all(users)
    db.session.commit()  # commit users so they have IDs

    print("Creating recipes...")
    recipes = []
    for i in range(100):
        instructions = fake.paragraph(nb_sentences=8)

        # Ensure instructions are at least 50 characters
        while len(instructions.strip()) < 50:
            instructions = fake.paragraph(nb_sentences=10)

        user = rc(users)

        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15, 90),
            user_id=user.id  # ✅ set foreign key directly
        )

        recipes.append(recipe)

    db.session.add_all(recipes)
    db.session.commit()

    print("✅ Seeding complete.")
