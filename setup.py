
import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'networkx'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='network-games',
    version='0.0.1',
    description='Various combinatrial games on graphs',
    long_description=readme + '\n\n' + history,
    author='Peter Nicks',
    author_email='pfwnicks@gmail.com',
    url='https://github.com/pfwnicks/network-games',
    packages=[
        'core',
    ],
    # entry_points={'console_scripts': ['deepwalk = deepwalk.__main__:main']},
    # package_dir={'deepwalk':
    #              'deepwalk'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    # zip_safe=False,
    # keywords='deepwalk',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    # test_suite='tests',
    # tests_require=test_requirements
)