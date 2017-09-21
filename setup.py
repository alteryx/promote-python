import os
from distutils.core import setup
from setuptools import find_packages

# Get version from defined python file
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'promote', 'version.py')) as fh:
    version = fh.read().strip()
    exec(version)

    setup(
        name="promote",
        version=__version__,
        author="Alteryx",
        author_email="dev@yhathq.com",
        url="https://github.com/alteryx/promote-python-client",
        packages=find_packages(),
        description="Client for deploying Python models to Promote.",
        license="BSD",
        classifiers=(
        ),
        install_requires=[
            "progressbar2==3.10.1",
            "requests==2.11.1",
            "requests-toolbelt==0.7.0",
            "schema==0.6.5"
        ],
        long_description=open("README.rst").read(),
        keywords=['alteryx', 'scikit-learn', 'numpy', 'pandas'],
    )
