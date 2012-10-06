from setuptools import setup
import subprocess
import os.path

long_description = (open('README.md').read())

setup(
    name='django-formfield-cache',
    version='0.3',
    description='django-formfield-cache provide a simple and non-intrusive way (using decorators) to cache the queries from foreign key fields of any inlineAdmin subclasses.',
    long_description=long_description,
    author='Tom Tang',
    author_email='tly1980@gmail.com',
    url='https://github.com/tly1980/django-formfield-cache',
    classifiers=[
        'Development Status ::  - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    packages=['django-formfield-cache'],
    package_dir={'django-formfield-cache': 'src/formfield_cache'}
)