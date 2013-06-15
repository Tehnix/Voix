from setuptools import setup
from version import get_git_version

setup(name='Voix',
      version=get_git_version(),
      description='A voice communication client.',
      author='Christian Laustsen, Martin Madsen',
      author_mail='christianlaustsen@gmail.com, martin@martinjlowm.dk',
      url='http://codetalk.io/')
