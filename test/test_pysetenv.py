import os.path
import subprocess
import sys
import unittest


class SubprocessError(unittest.TestCase.failureException):
    def __init__(self, message):
        unittest.TestCase.failureException.__init__(
            self, '\n{line}\n{msg}\n{line}'.format(line='-' * 60, msg=message)
        )


class TestSetEnv(unittest.TestCase):
    def assertPopen(self, command, env=None, env_update=True, returncode=0):
        if env is not None and env_update:
            overrides = env
            env = dict(os.environ)
            env.update(overrides)

        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env=env, universal_newlines=True
        )
        output = proc.communicate()[0]
        if proc.returncode != returncode:
            raise SubprocessError(output)
        return output

    def assertOutput(self, command, output, *args, **kwargs):
        self.assertEqual(self.assertPopen(command, *args, **kwargs), output)

    def test_no_args(self):
        self.assertOutput(
            ['pysetenv'],
            output='pysetenv: COMMAND is required\n',
            returncode=1
        )

    def test_no_command(self):
        self.assertOutput(
            ['pysetenv', 'FOO=bar'],
            output='pysetenv: COMMAND is required\n',
            returncode=1
        )

    def test_command(self):
        self.assertOutput(
            ['pysetenv', '--', sys.executable, '-c', 'print("hi")'],
            output='hi\n'
        )

    def test_command_and_args(self):
        self.assertOutput(
            ['pysetenv', '--', 'FOO=bar', sys.executable, '-c',
             'import os; print(os.environ["FOO"])'],
            output='bar\n'
        )
