from setuptools import setup, find_packages
import subprocess
import os.path

path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'README.md')
long_description = "description"

try:
    with open(path) as f:
        long_description = f.read()
except:
    pass

setup(
    name='django-formfield-cache',
    version='0.3',
    description='django-formfield-cache provide a simple and non-intrusive way (using decorators) to cache the queries from foreign key fields of any inlineAdmin subclasses.',
    long_description=long_description,
    author='Tom Tang',
    author_email='tly1980@gmail.com',
    url='https://github.com/tly1980/django-formfield-cache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    packages=['formfield_cache'],
    package_dir= {'formfield_cache':'src/formfield_cache'},
)