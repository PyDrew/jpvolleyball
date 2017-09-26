from setuptools import setup

setup(name='flaskjpv',
      version='1.0',
      description='JPVolleyball Webiste',
      author='Drew Marchand',
      author_email='drew.marchand@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.10.1', 'MarkupSafe', 'Flask-SQLAlchemy', 'MySQL-Python'],
      )
