import os
import shutil
import random
import string
import click


def generate_random_str(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class AppGenerator:

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

    def create_app_dir(self, exist_ok=False):
        """
        Create app directory.

        :param bool exist_ok:
        """
        path = self.app_dir
        if not exist_ok and os.path.exists(path):
            raise FileExistsError('App path {} already exists!'.format(path))
        os.makedirs(path, exist_ok=exist_ok)

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
        self.create_app_dir()
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
        pass


class FileGenerator(AppGenerator):

    category = 'file'

    @classmethod
    def get_internal_template_dir(cls):
        return os.path.realpath(os.path.join(os.path.dirname(__file__), 'templates', cls.category))

    @staticmethod
    def get_rel_path(base_path, path):
        if base_path == path:
            return ''
        elif len(base_path) < len(path):
            return path[len(base_path) + 1:]
        else:
            raise ValueError('Path {} must larger than base path {}!'.format(path, base_path))

    def find_template(self, template_dir=None):
        if not template_dir:
            template_dir = self.get_internal_template_dir()
        path = os.path.join(template_dir, self.template)
        if os.path.exists(path):
            return path
        raise FileNotFoundError('Template path {} not found!'.format(path))

    def pre_process(self, **kwargs):
        kwargs = super().pre_process(**kwargs)
        template_dir = kwargs.get('template_dir')
        path = self.find_template(template_dir=template_dir)
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
        # generate render params
        additional = kwargs.get('additional')
        params = {'secret': generate_random_str()}
        if additional:
            for a in additional:
                idx = a.find('=')
                if idx > 0:
                    params[a[0:idx]] = a[idx + 1:]
        # select package index
        if 'pip_index' not in params:
            pip_index = 1
            if not self.skip_prompt:
                pip_index = 0
                msg = ['Select which Python Package Index to use: ', '']
                msg += ['[{}] {}'.format(i + 1, self.index_list[i]) for i in range(len(self.index_list))]
                msg += ['', 'Please input the front number: ']
                while pip_index <= 0 or pip_index > len(self.index_list):
                    pip_index = click.prompt('\n'.join(msg), type=int, default=1)
            params['pip_index'] = self.index_list[pip_index - 1]
        # set render_params
        kwargs['render_params'] = params
        return kwargs

    def generate(self, **kwargs):
        path = kwargs.get('template_path')
        params = kwargs.get('render_params') or {}
        context = self.get_context(template_path=path)
        # load templates
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(path))
        for name, dirs, files in os.walk(path):
            rel_path = self.get_rel_path(path, name)
            # create sub directories
            for d in dirs:
                os.makedirs(os.path.join(self.app_dir, rel_path, d), exist_ok=True)
            # get templates
            if rel_path:
                tmpls = [os.path.join(rel_path, t) for t in files if not t.endswith('.pyc')]
            else:
                tmpls = files
            for tmpl in tmpls:
                print('-----', tmpl)
                template = env.get_template(tmpl, globals={'context': context})
                target = os.path.join(self.app_dir, tmpl)
                with open(target, 'w') as fh:
                    fh.write(template.render(**params))
