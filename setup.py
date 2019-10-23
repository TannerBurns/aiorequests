import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name= 'aiorequests',
    version= '0.2.1',
    packages= find_packages(),
    include_package_data= True,
    description= 'Async requests library built with asyncio and requests. Ability to bulk async request.',
    long_description= README,
    url= 'https://www.github.com/tannerburns/aiorequests',
    author= 'Tanner Burns',
    author_email= 'tjburns102@gmail.com',
    install_requires=[
        "requests"
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
