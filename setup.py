# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='monitor_air_quality',  # Required
    version='2.0.2',  # Required
    description='Read data from sds011 sensor, gather purpleair and notion data and POST to an API',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/gene1wood/monitor_air_quality',  # Optional
    author='Gene Wood',  # Optional
    author_email='gene_wood@cementhorizon.com',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    python_requires='>=3',
    entry_points = {
        'console_scripts': ['monitor_air_quality=monitor_air_quality.monitor_air_quality:main'],
    },
    install_requires=['PyYAML', 'requests', 'py-sds011', 'python-aqi', 'xdg'],
    include_package_data=True,
)
