import click
from flask.cli import with_appcontext
from seeders import seed_all

@click.command(name='create')
@with_appcontext
def seed_command():
    seed_all()
    click.echo("Database seeded successfully!")
