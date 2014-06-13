from setuptools import setup
import sys

prefix = getattr(sys, "prefix")
if prefix == '/usr':
    prefix = ''

setup(
    name='cryptocoinnotify',
    version='0.2.0',
    packages=['cryptocoinnotify', 'cryptocoinnotify.backends'],
    url='https://www.odesk.com/users/%7E01286f3481df6273cb',
    license='',
    author='derfenix',
    author_email='derfenix@gmail.com',
    description='',
    scripts=['cryptocoinnotify/scripts/cryptocoinnotify'],
    data_files=[
        (prefix + '/etc/', ['cryptocoinnotify/cryptocoinnotify.cfg'])
    ],
    install_requires=open('./requirements.txt', 'r').readlines()
)