from setuptools import setup, find_packages
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('botrnot/botrnot.py').read(),
    re.M
).group(1)

with open("README.md", "r") as f:
    long_descr = f.read()

setup(
    name='botrnot',
    author='James Campbell',
    author_email='james@jamescampbell.us',
    version=version,
    license='GPLv3',
    description='Evaluate if a twitter account is a bot or not',
    long_description=long_descr,
    packages=['botrnot'],
    py_modules=['botrnot'],
    keywords=['bots', 'data-analysis', 'twitter', 'osint-research', 'osint'],
    classifiers=["Programming Language :: Python :: 3 :: Only","Operating System :: OS Independent"],
    install_requires=[
        'argparse',
        'beautifultable',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'botrnot = botrnot.botrnot:main',
        ],
    },
    url='https://github.com/jamesacampbell/botrnot',
    download_url='https://github.com/jamesacampbell/botrnot/archive/{}.tar.gz'.format(
        version)
)
