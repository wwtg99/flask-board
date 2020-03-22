from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.0'

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='Flask-Board',
    version=VERSION,
    description='Build base flask app depends on template.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/wwtg99/flask-board',
    author='Wu Wentao',
    author_email='wwtg99@gmail.com',
    license='MIT',
    install_requires=[
        "Werkzeug>=0.15",
        "Jinja2>=2.10.1",
        "flask>=1.0",
        "click>=5.1",
        "python-dotenv>=0.12",
    ],
    include_package_data=True,
    keywords='flask template',
    entry_points={
        'flask.commands': [
            'board=flask_board.commands:cli'
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    packages=find_packages(),
    zip_safe=False,
    platforms='any'
)
