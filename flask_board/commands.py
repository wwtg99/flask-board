import click
from werkzeug.utils import import_string


def get_generator(name):
    if '.' not in name:
        name = 'flask_board.generator.{}Generator'.format(name.capitalize())
    try:
        cls = import_string(name)
        return cls
    except ImportError:
        click.echo('No generator {} found!'.format(name))


@click.command(short_help='Generate flask app by templates')
@click.argument('name')
@click.option('-d', '--directory', help='Project directory, default current directory')
@click.option('-g', '--generator', help='Generator type', type=str, default='jinja2', show_default=True)
@click.option('-t', '--template', help='Template name', default='default')
@click.option('-p', '--template-dir', help='Use custom template directory')
@click.option('-a', '--additional', help='Additional parameters send to generator', multiple=True)
@click.option('-s', '--skip', help='Skip prompts and use default', is_flag=True)
def cli(name, directory, generator, template, **kwargs):
    generator = get_generator(generator)(name=name, directory=directory, template=template)
    try:
        generator.run(**kwargs)
    except (FileNotFoundError, FileExistsError) as e:
        click.echo(e)
