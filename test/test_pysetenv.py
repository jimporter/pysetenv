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
        output = self.assertPopen(['pysetenv'])
        self.assertTrue('PATH={}\n'.format(os.environ['PATH']) in output)

    def test_def_var(self):
        output = self.assertPopen(['pysetenv', 'FOO=bar'])
        self.assertTrue('FOO=bar\n' in output)

        output = self.assertPopen(['pysetenv', 'FOO=bar', '--'])
        self.assertTrue('FOO=bar\n' in output)

        output = self.assertPopen(['pysetenv', 'PATH=path'])
        self.assertTrue('PATH=path\n' in output)

    def test_undef_var(self):
        output = self.assertPopen(['pysetenv', '-uPATH'])
        self.assertFalse('PATH={}\n'.format('PATH', os.environ['PATH'])
                         in output)

        output = self.assertPopen(['pysetenv', '-uPATH', 'PATH=path'])
        self.assertTrue('PATH=path\n' in output)

        output = self.assertPopen(['pysetenv', '-uPATH', 'PATH=path', '--'])
        self.assertTrue('PATH=path\n' in output)

    def test_ignore_environment(self):
        self.assertOutput(['pysetenv', '-i'], '')

    def test_ignore_environment_def_var(self):
        self.assertOutput(['pysetenv', '-i', 'FOO=bar'], 'FOO=bar\n')
        self.assertOutput(['pysetenv', '-i', 'FOO=bar', '--'], 'FOO=bar\n')

    def test_command(self):
        self.assertOutput(
            ['pysetenv', sys.executable, '-c', 'print("hi")'],
            output='hi\n'
        )
        self.assertOutput(
            ['pysetenv', '--', sys.executable, '-c', 'print("hi")'],
            output='hi\n'
        )

    def test_def_var_command(self):
        self.assertOutput(
            ['pysetenv', 'FOO=bar', sys.executable, '-c',
             'import os; print(os.environ["FOO"])'],
            output='bar\n'
        )
        self.assertOutput(
            ['pysetenv', 'FOO=bar', '--', sys.executable, '-c',
             'import os; print(os.environ["FOO"])'],
            output='bar\n'
        )

    def test_undef_var_command(self):
        self.assertOutput(
            ['pysetenv', '-uPATH', sys.executable, '-c',
             'import os; print(os.environ.get("PATH"))'],
            output='None\n'
        )
        self.assertOutput(
            ['pysetenv', '-uPATH', '--', sys.executable, '-c',
             'import os; print(os.environ.get("PATH"))'],
            output='None\n'
        )

        self.assertOutput(
            ['pysetenv', '-uPATH', 'PATH=path', sys.executable, '-c',
             'import os; print(os.environ["PATH"])'],
            output='path\n'
        )
        self.assertOutput(
            ['pysetenv', '-uPATH', 'PATH=path', '--', sys.executable, '-c',
             'import os; print(os.environ["PATH"])'],
            output='path\n'
        )

    def test_ignore_environment_command(self):
        self.assertOutput(
            ['pysetenv', '-i', sys.executable, '-c',
             'import os; print(os.environ.get("PATH"))'],
            output='None\n'
        )
        self.assertOutput(
            ['pysetenv', '-i', '--', sys.executable, '-c',
             'import os; print(os.environ.get("PATH"))'],
            output='None\n'
        )

    def test_ignore_environment_def_varcommand(self):
        self.assertOutput(
            ['pysetenv', '-i', 'PATH=path', sys.executable, '-c',
             'import os; print(os.environ["PATH"])'],
            output='path\n'
        )
        self.assertOutput(
            ['pysetenv', '-i', 'PATH=path', '--', sys.executable, '-c',
             'import os; print(os.environ["PATH"])'],
            output='path\n'
        )
