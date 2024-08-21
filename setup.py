# Copyright 2024, Guillermo Adrián Molina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from setuptools import setup, find_packages

################################################################################
# HELPER FUNCTIONS #############################################################
################################################################################


def get_lookup():
    '''get version by way of the version file
    '''
    lookup = dict()
    version_file = os.path.join('ttkedit', 'version.py')
    with open(version_file, encoding='utf-8') as filey:
        exec(filey.read(), lookup)
    return lookup


def get_install_requirements():
    with open('requirements.txt', encoding='utf-8') as file:
        requirements = file.read().splitlines()
        return requirements


# Make sure everything is relative to setup.py
install_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(install_path)

# Get version information from the lookup
lookup = get_lookup()
VERSION = lookup['__version__']
NAME = lookup['NAME']
AUTHOR = lookup['AUTHOR']
AUTHOR_EMAIL = lookup['AUTHOR_EMAIL']
PACKAGE_URL = lookup['PACKAGE_URL']
KEYWORDS = lookup['KEYWORDS']
DESCRIPTION = lookup['DESCRIPTION']
LICENSE = lookup['LICENSE']
with open('README.md', encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

################################################################################
# MAIN #########################################################################
################################################################################

if __name__ == "__main__":

    INSTALL_REQUIRES = get_install_requirements()
    #DEV_REQUIRES = get_dev_requirements()
    #TESTS_REQUIRES = get_test_requirements()

    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        url=PACKAGE_URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        keywords=KEYWORDS,
        test_suite="tests",
        # tests_require=TESTS_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        entry_points={
            'console_scripts': [
                 'ttkedit = ttkedit:main',
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            'License :: OSI Approved :: Apache Software License',
            "Operating System :: OS Independent",
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "Topic :: Terminals",
            "Topic :: Software Development :: User Interfaces"
        ],
    )