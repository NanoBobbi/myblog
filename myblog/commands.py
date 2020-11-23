import click
from myblog import app, db
from myblog.models import Article
from myblog.fakes import fake_article, fake_categories


def register_commands():
    @app.cli.command("initdb")
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        if drop:
            db.drop_all()
            click.echo("Dropped database.")
        db.create_all()
        click.echo("Initialized database.")

    @app.cli.command()
    def forge():
        db.create_all()
        fake_categories(5)
        fake_article(20)
        click.echo('Done.')
