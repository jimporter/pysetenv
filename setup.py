import os
import re
import subprocess
from setuptools import setup, find_packages, Command

from pysetenv.version import version

root_dir = os.path.abspath(os.path.dirname(__file__))


class Coverage(Command):
    description = 'run tests with code coverage'
    user_options = [
        ('test-suite=', 's',
         "test suite to run (e.g. 'some_module.test_suite')"),
    ]

    def initialize_options(self):
        self.test_suite = None

    def finalize_options(self):
        pass

    def run(self):
        env = dict(os.environ)
        pythonpath = os.path.join(root_dir, 'test', 'scripts')
        if env.get('PYTHONPATH'):
            pythonpath += os.pathsep + env['PYTHONPATH']
        env.update({
            'PYTHONPATH': pythonpath,
            'COVERAGE_FILE': os.path.join(root_dir, '.coverage'),
            'COVERAGE_PROCESS_START': os.path.join(root_dir, 'setup.cfg'),
        })

        subprocess.run(['coverage', 'erase'], check=True)
        subprocess.run(
            ['coverage', 'run', '-m', 'unittest', 'discover'] +
            (['-v'] if self.verbose != 0 else []) +
            ([self.test_suite] if self.test_suite else []),
            env=env, check=True
        )
        subprocess.run(['coverage', 'combine'], check=True,
                       stdout=subprocess.DEVNULL)


custom_cmds = {
    'coverage': Coverage,
}

with open(os.path.join(root_dir, 'README.md'), 'r') as f:
    # Read from the file and strip out the badges.
    long_desc = re.sub(r'(^# pysetenv)\n\n(.+\n)*', r'\1', f.read())

setup(
    name='pysetenv',
    version=version,

    description=('A simple tool to set environment variables before running ' +
                 'a command'),
    long_description=long_desc,
    long_description_content_type='text/markdown',
    keywords='set environment variables',
    url='https://github.com/jimporter/pysetenv',

    author='Jim Porter',
    author_email='itsjimporter@gmail.com',
    license='BSD-3-Clause',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],

    packages=find_packages(exclude=['test', 'test.*']),

    extras_require={
        'test': ['coverage', 'flake8 >= 3.0', 'flake8-quotes'],
    },

    entry_points={
        'console_scripts': [
            'pysetenv=pysetenv:main',
        ],
    },

    test_suite='test',
    cmdclass=custom_cmds,
)
