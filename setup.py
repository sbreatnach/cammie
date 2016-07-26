#!/usr/bin/env python
"""
PyPi installation script for the project
"""
# HACK: for issue https://bugs.python.org/issue8876 which is fixed but may not
# have filtered down for your particular distro
import os
del os.link

from cammie import __version__
from setuptools import setup, find_packages

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


def read_requirements(path):
    """
    Parses and returns the requirements from the given file path

    :param path:
    :return: list of requirements parsed from file
    """
    requirements = []
    with open(path, 'rb') as handle:
        for line in handle:
            requirements.append(line.strip())
    return requirements


setup(
    name='cammie',
    version=__version__,
    author='Shane Breatnach',
    author_email='shane.breatnach@gmail.com',
    description='',
    license='MIT',
    keywords='webcam raspberrypi',
    url='https://github.com/sbreatnach/cammie',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(
        os.path.join(ROOT_PATH, 'requirements.txt')
    ),
    long_description='',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'cammie = cammie.main:main'
        ]
    }
)
