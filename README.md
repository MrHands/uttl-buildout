# uttl-buildout
Buildout utilities as developed for Up There They Love

# Building from source

Check that you're running at least Python 3.9:

    D:\Projects\uttl-buildout>python --version
    Python 3.9.5

Build and install egg:

    python setup.py install

Create egg and install locally:

    python setup.py bdist_egg
    python -m easy_install -a dist\uttl_buildout-1.0.0-py3.9.egg
