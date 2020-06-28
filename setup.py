from setuptools import setup, find_packages
from botrnot.__version__ import __version__


with open("README.md", "r") as f:
    long_descr = f.read()

setup(
    name='botrnot',
    author='James Campbell',
    author_email='james@jamescampbell.us',
    version=__version__,
    license='GPLv3',
    description='Evaluate if a twitter account is a bot or not',
    long_description=long_descr,
    long_description_content_type="text/markdown",
    packages=['botrnot'],
    py_modules=['botrnot'],
    keywords=['bots', 'data-analysis', 'twitter', 'osint-research', 'osint'],
    classifiers=["Programming Language :: Python :: 3 :: Only","Operating System :: OS Independent"],
    install_requires=[
        'argparse',
        'beautifultable',
        'requests',
        'twitter_scraper',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'botrnot = botrnot.botrnot:main',
        ],
    },
    url='https://github.com/jamesacampbell/botrnot',
    download_url='https://github.com/jamesacampbell/botrnot/archive/{}.tar.gz'.format(
        __version__)
)
