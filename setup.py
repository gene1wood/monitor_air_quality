# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='monitor_air_quality',  # Required
    version='1.0.0',  # Required
    description='Read data from sds011 sensor and POST to API',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/gene1wood/monitor_air_quality',  # Optional
    author='Gene Wood',  # Optional
    author_email='gene_wood@cementhorizon.com',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    python_requires='>=3',
    entry_points = {
        'console_scripts': ['monitor_air_quality=monitor_air_quality.monitor_air_quality:query_mode'],
    },
    install_requires=['PyYAML', 'requests', 'py-sds011', 'python-aqi'],
    include_package_data=True,
)
