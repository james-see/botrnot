from setuptools import setup, find_packages
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('botrnot/botrnot.py').read(),
    re.M
).group(1)

setup(
    name='botrnot',
    author='James Campbell',
    author_email='james@jamescampbell.us',
    version=version,
    license='GPLv3',
    description='Evaluate if a twitter account is a bot or not',
    packages=['botrnot'],
    py_modules=['botrnot'],
    keywords=['bots', 'data-analysis', 'twitter', 'osint-research', 'osint'],
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    install_requires=[
        'argparse',
        'pandas',
        'pprint',
        'requests',
        'twitter_scraper'
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
