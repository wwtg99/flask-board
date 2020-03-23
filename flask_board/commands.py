from platform import python_version
import click
from flask import __version__ as flask_version
from flask_board import __version__ as board_version
from flask_board.generator import guess_generator


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Python {}'.format(python_version()))
    click.echo('Flask {}'.format(flask_version))
    click.echo('Flask Board {}'.format(board_version))
    ctx.exit()


@click.command(short_help='Generate flask app by templates')
@click.argument('name')
@click.option('-d', '--directory', help='Project directory, default current directory')
@click.option('-t', '--template', help='Template name', default='default')
@click.option('-a', '--additional', help='Additional parameters send to generator', multiple=True)
@click.option('-s', '--skip', help='Skip prompts and use default', is_flag=True)
@click.option('--excludes', help='Exclude file patterns in template directory, comma separated')
@click.option('--excludes-dir', help='Exclude directory patterns in template directory, comma separated')
@click.option('--version', help='Show version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli(name, directory, template, **kwargs):
    """
    Create Flask project by template.

    name: project name
    """
    generator = guess_generator(name=name, directory=directory, template=template)
    try:
        generator.run(**kwargs)
    except (FileNotFoundError, FileExistsError) as e:
        click.echo(e)
