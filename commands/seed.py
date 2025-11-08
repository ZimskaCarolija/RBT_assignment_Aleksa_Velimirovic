import click
from flask.cli import with_appcontext
from app import db
from seeders import seed_all

@click.command("seed")
@click.option("--fresh", is_flag=True, help="Clear all tables before seeding")
@with_appcontext
def seed_command(fresh):
    """Seed the database. Use --fresh to clear all tables first."""
    if fresh:
        click.confirm("Are you sure you want to delete all data from the database?", abort=True)
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        click.echo("Database cleared successfully!")
    
    seed_all()
    click.echo("Database seeded successfully!")
