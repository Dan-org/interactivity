"""
Django Laboratory setup.
"""

from setuptools import setup, find_packages

setup( name='django-interactivity',
       version='0.1',
       description='Django app flash activities that can save and load work.',
       author='Matt Easterday',
       author_email='easterday@northwestern.edu',
       packages = find_packages(),
       include_package_data = True,
       zip_safe = False,
       install_requires = ['django-ttag', 'pyamf']
      )