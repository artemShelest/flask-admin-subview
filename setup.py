import os

from setuptools import setup


def file_path(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(file_path(fname)).read()


def desc():
    info = read('README.rst')
    try:
        return info + '\n\n' + read('changelog.rst')
    except IOError:
        return info


setup(
    name='Flask-Admin-Subview',
    version='0.1.1',
    packages=['flask_admin_subview'],
    package_dir={'': 'src'},
    package_data={
        'flask_admin_subview': [
            'LICENSE',
            'README.rst'
        ]
    },
    include_package_data=True,
    url='https://github.com/artemShelest/flask-admin-subview',
    license='MIT',
    author='Artem Shelest',
    author_email='artem.e.shelest@gmail.com',
    description='Embedded Flask-Admin list views.',
    long_description=desc(),
    keywords=['flask-admin', 'list', 'view', 'embedded', 'nested', 'subview', 'one-to-many', 'relation',
              'view relations'],
    install_requires=[
        'flask',
        'wtforms',
        'flask-admin',
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
