from flask import Flask

def register_commands(app: Flask):
    """
    Automatically register all Flask CLI commands from this folder.
    """
    from .seed import seed_command

    app.cli.add_command(seed_command)
