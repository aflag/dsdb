from setuptools import setup

setup(name='dsdb',
    version='0.1',
    description='A simple database for simple needs',
    long_description="""This is a filesystem backed schemaless database. It is very simple, but handles concurrent access.""",
    author='Rafael Cunha de Almeida',
    author_email='rafael@kontesti.me',
    package_dir = {'': 'src'},
    py_modules=['dsdb'],
    license='MIT',
    url='http://github.com/aflag/dsdb',
) 
