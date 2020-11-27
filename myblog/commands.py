import click
from myblog import app, db
from myblog.models import Article, User
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

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login')
    def admin(username, password):
        """
        Create user.
        """
        db.create_all()
        user = User.query.first()
        if user is not None:
            click.echo('Updating user ...')
            user.username = username
            user.password = password
        else:
            click.echo('Creating user ...')
            user = User(userName=username, password=password)
            db.session.add(user)
        db.session.commit()
        click.echo('Done.')
