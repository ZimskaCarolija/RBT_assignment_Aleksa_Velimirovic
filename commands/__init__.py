from flask import Flask

def register_commands(app: Flask):
    """
    Automatically register all Flask CLI commands from this folder.
    """
    from .seed import seed_all_command

    app.cli.add_command(seed_all_command)
