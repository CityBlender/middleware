# middleware

## Setting up

This project uses ``pipenv`` to keep the local Python environment consistent accross different machines and development environments.

Please refer to [the installation guide](https://docs.pipenv.org/install/) to install it on your device and get an idea how it works. You can also check out [the instruction here](https://robots.thoughtbot.com/how-to-manage-your-python-projects-with-pipenv).


*If you get the ``Warning: the environment variable LANG is not set!`` error when trying to set up ``pipenv`` check out [this issue for a fix](https://github.com/pypa/pipenv/issues/538).*


### Set up development environment

To install the neccessary dependencies run ``pipenv install``

To use the project's virtualenv run ``pipenv shell``

### Installing new dependencies

To install a new library run ``pipenv install *LIBRARY NAME*``

This will install the library into the project's virtualenv and update ``Pipfile`` and ``Pipfile.lock``.

Make sure you to keep an eye on ``Pipfile`` changes and update your dependencies when it changes.







## Contributors

- Ilja Panic
- Alfie Long
- Soma Suzuki
