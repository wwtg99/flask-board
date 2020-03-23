import os
import shutil
import random
import fnmatch
import string
import click


def generate_random_str(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def guess_generator(name, directory, template):
    if os.path.exists(template) and os.path.isdir(template):
        template_dir = os.path.dirname(template)
        return Jinja2Generator(name=name, directory=directory, template=template, template_dir=template_dir)
    else:
        return Jinja2Generator(name=name, directory=directory, template=template)


class AppGenerator:

    ignore_content = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.cache
nosetests.xml
coverage.xml

# Translations
*.mo
*.pot

# Django stuff:
*.log

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# IDEs
.idea/

# data
instance/
.DS_store
.env
    """

    def __init__(self, name, directory, template):
        self.name = name
        self.directory = directory or ''
        self.template = template
        self.skip_prompt = False

    @property
    def app_dir(self):
        if self.directory:
            path = os.path.join(self.directory, self.name)
        else:
            path = self.name
        return path

    @property
    def default_additional(self):
        return {}

    def create_app_dir(self, exist_ok=False):
        """
        Create app directory.

        :param bool exist_ok:
        """
        path = self.app_dir
        if not exist_ok and os.path.exists(path):
            raise FileExistsError('App path {} already exists!'.format(path))
        os.makedirs(path, exist_ok=exist_ok)

    def create_ignore(self):
        path = os.path.join(self.app_dir, '.gitignore')
        if not os.path.exists(path):
            with open(path, 'w') as fh:
                fh.write(self.ignore_content)

    def run(self, **kwargs):
        """
        Run generator.
        """
        kwargs = self.pre_process(**kwargs)
        self.generate(**kwargs)
        self.post_process(**kwargs)

    def pre_process(self, **kwargs):
        """
        Pre process before generation.
        """
        if 'skip' in kwargs and kwargs['skip'] is True:
            self.skip_prompt = True
        # create app directory
        self.create_app_dir()
        # generate additional params
        additional = kwargs.get('additional')
        params = self.default_additional
        if additional:
            for a in additional:
                idx = a.find('=')
                if idx > 0:
                    params[a[0:idx]] = a[idx + 1:]
        kwargs['additional_params'] = params
        return kwargs

    def generate(self, **kwargs):
        """
        Generate project from template.
        """
        yield NotImplementedError

    def post_process(self, **kwargs):
        """
        Post process after generation
        """
        self.create_ignore()
        click.echo('Create project {} successfully. Enjoy yourself!'.format(self.app_dir))


class FileGenerator(AppGenerator):

    category = 'file'

    def __init__(self, name, directory, template, template_dir=None):
        super().__init__(name, directory, template)
        self.template_dir = template_dir

    @classmethod
    def get_internal_template_dir(cls):
        return os.path.realpath(os.path.join(os.path.dirname(__file__), 'templates', cls.category))

    @classmethod
    def find_template(cls, template, template_dir=None):
        if not template_dir:
            template_dir = cls.get_internal_template_dir()
        path = os.path.join(template_dir, template)
        if os.path.exists(path):
            return path
        raise FileNotFoundError('Template path {} not found!'.format(path))

    @staticmethod
    def get_rel_path(base_path, path):
        if base_path == path:
            return ''
        elif len(base_path) < len(path):
            return path[len(base_path) + 1:]
        else:
            raise ValueError('Path {} must larger than base path {}!'.format(path, base_path))

    def pre_process(self, **kwargs):
        kwargs = super().pre_process(**kwargs)
        path = self.find_template(template=self.template, template_dir=self.template_dir)
        kwargs['template_path'] = path
        return kwargs

    def generate(self, **kwargs):
        path = kwargs.get('template_path')
        for name, dirs, files in os.walk(path):
            rel_path = self.get_rel_path(path, name)
            # create sub directories
            for d in dirs:
                os.makedirs(os.path.join(self.app_dir, rel_path, d), exist_ok=True)
            # get templates
            if rel_path:
                tmpls = [os.path.join(rel_path, t) for t in files]
            else:
                tmpls = files
            for tmpl in tmpls:
                shutil.copyfile(os.path.join(path, tmpl), os.path.join(self.app_dir, tmpl))


class Jinja2Generator(FileGenerator):

    category = 'jinja2'
    index_list = [
        'https://pypi.org/simple',
        'https://pypi.tuna.tsinghua.edu.cn/simple/',
        'https://mirrors.aliyun.com/pypi/simple',
        'https://pypi.doubanio.com/simple/',
    ]

    @property
    def default_additional(self):
        return {'secret': generate_random_str()}

    @staticmethod
    def get_ignore_filter(ignore_file_pattern, ignore_dir_pattern):
        if not ignore_file_pattern:
            ignore_file_pattern = ['*.pyc', '*.pyo', '*.pyd', '*.egg', '*.log', '*.so', '*.zip', '*.tar', '*.tar.gz']
        if isinstance(ignore_file_pattern, str):
            ignore_file_pattern = ignore_file_pattern.split(',')
        if not ignore_dir_pattern:
            ignore_dir_pattern = ['.git', '__pycache__', '*.egg-info', 'build', 'dist', '.idea']
        if isinstance(ignore_dir_pattern, str):
            ignore_dir_pattern = ignore_dir_pattern.split(',')

        def ignore_file_filter(path):
            for exc in ignore_file_pattern:
                if fnmatch.fnmatch(path, exc):
                    return False
            return True

        def ignore_dir_filter(path):
            paths = path.strip(os.path.sep).split(os.path.sep)
            for exc in ignore_dir_pattern:
                for p in paths:
                    if fnmatch.fnmatch(p, exc):
                        return False
            return True

        return ignore_file_filter, ignore_dir_filter

    def get_context(self, **kwargs):
        context = {
            'name': self.name,
            'directory': self.directory,
            'template': self.template
        }
        context.update(kwargs)
        return context

    def pre_process(self, **kwargs):
        kwargs = super().pre_process(**kwargs)
        # select package index
        if 'pip_index' not in kwargs['additional_params']:
            pip_index = 1
            if not self.skip_prompt:
                pip_index = 0
                msg = ['Select which Python Package Index to use: ', '']
                msg += ['[{}] {}'.format(i + 1, self.index_list[i]) for i in range(len(self.index_list))]
                msg += ['', 'Please input the front number: ']
                while pip_index <= 0 or pip_index > len(self.index_list):
                    pip_index = click.prompt('\n'.join(msg), type=int, default=1)
            kwargs['additional_params']['pip_index'] = self.index_list[pip_index - 1]
        return kwargs

    def generate(self, **kwargs):
        path = kwargs.get('template_path')
        params = kwargs.get('additional_params') or {}
        excludes = kwargs.get('excludes')
        excludes_dir = kwargs.get('excludes_dir')
        excludes_file_filter, excludes_dir_filter = self.get_ignore_filter(excludes, excludes_dir)
        context = self.get_context(template_path=path)
        # load templates
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(path))
        for name, dirs, files in os.walk(path):
            rel_path = self.get_rel_path(path, name)
            # filter ignores
            if not excludes_dir_filter(rel_path):
                continue
            files = filter(excludes_file_filter, files)
            # create directory
            os.makedirs(os.path.join(self.app_dir, rel_path), exist_ok=True)
            # get templates
            if rel_path:
                tmpls = [os.path.join(rel_path, t) for t in files]
            else:
                tmpls = files
            for tmpl in tmpls:
                template = env.get_template(tmpl, globals={'context': context})
                target = os.path.join(self.app_dir, tmpl)
                with open(target, 'w') as fh:
                    fh.write(template.render(**params))
