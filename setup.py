from setuptools import setup, find_packages
setup(
    name="csSociety",
    version="0.1",
    packages=find_packages(),

    # Check that a package for install is available from PyPI
    install_requires=[
        'Flask>=0.12.2',
        'Flask-Bootstrap >= 3.3.7.1',
        'Flask-Login >= 0.4.1',
        'Flask-Migrate >= 2.1.1',
        'Flask-Misaka >= 0.4.1',
        'Flask-Session >= 0.3.1',
        'Flask-SQLAlchemy >= 2.3.2',
        'Flask-WTF >= 0.14.2',
    ],  # PyPI package

    package_data={
        # If any package contains *.txt or *.pdf files, include them:
        '': ['*.txt', '*.pdf'],
        # And everything in the test, doc, static and jinja folders:
        'css': [
            'docs/*.py',
            'docs/gantt_chart/*',
            'docs/overview_and_requirements/*',
            'docs/uml/*',
            'tests/*',
            'app/static/*',
            'app/templates/*'
        ],
    },

    # metadata for upload to PyPI
    author="Daniel Power, Kent Barter, Adrien Lagamelle, Stephen Walsh, Xuemeng Li",
    author_email="djp468@mun.ca",
    description="Reddit/StackOverflow like forum software for CS2005",
    keywords="flask forum",
    tests_require=['pytest'],
)
