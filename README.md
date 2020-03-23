Flask Board
===========

# Description

[Flask](https://flask.palletsprojects.com/en/1.1.x/) is a powerful and flexible web framework.
Since it is so flexible, we have to "copy" some codes to start a new production project.
Flask Board is aimed to start a flask project depends on some carefully prepared templates.

# Installation

```
pip install flask-board
```

After installation, we can see flask board installed as a flask command plugin.

```
flask board --help
```

# Usage

Create flask project depends on pre defined templates.

```
flask board your-project
```

Same as used the `default` template.

```
flask board your-project -t default
```

Change the project directory (default use the current directory).

```
flask board your-project -d <path-to-directory>
```

Use your own project template.

```
flask board your-project -t <path-to-your-tempalte-directory>
```

We use jinja2 engine to render all files in the template directory.

We can also exclude files in the template directory (default excludes file patterns *.pyc, *.pyo, *.pyd, *.egg, *.log, *.so, *.zip, *.tar, *.tar.gz).

And exclude directories and all files under it (default excludes directories .git, `__pycache__`, *.egg-info, build, dist, .idea).

```
flask board your-project -t <path-to-your-template-directory> --excludes="*.pyc,*.log" excludes_dir=".git,__pycache__"
```
