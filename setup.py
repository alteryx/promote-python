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
        author_email="promotedev@alteryx.com",
        url="https://github.com/alteryx/promote-python",
        packages=find_packages(),
        description="Client for deploying Python models to Promote.",
        license="BSD",
        classifiers=(
        ),
        install_requires=[
            "requests",
            "schema"
        ],
        long_description=open("README.rst").read(),
        keywords=['alteryx', 'scikit-learn', 'numpy', 'pandas'],
    )
