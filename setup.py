# -*- coding: utf-8 -*-
#
# Copyright 2020 AllanKT.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from setuptools import (
    setup,
    find_packages,
)

here = os.path.dirname(__file__)
requires = [
    'boto3 >= 1.10.37',
]


with open(os.path.join(here, './README.rst'), 'r') as fh:
    long_description = fh.read()

setup(
    name='dynamodb',
    version='1.0.0',

    description='DynamoDB SDK.',
    long_description=long_description,
    url='https://github.com/AllanKT/python-dynamo',

    author='Allan Kleitson Teotonio',
    author_email='allankltsn@gmail.com',

    keywords=['DynamoDB', 'AWS', 'boto3'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires=requires,
    python_requires='>=3.5',
)