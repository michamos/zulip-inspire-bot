# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2018 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Zulip chatbot for Inspire"""

from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup


url = 'https://github.com/inspirehep/zulip-inspire-bot'

readme = open('README.rst').read()

setup_requires = [
    'autosemver~=0.0,>=0.5.3',
]

install_requires = [
    'subprocess32~=3.5,>=3.5.0rc1',
    'zulip~=0.0,>=0.4.6',
]

docs_require = []

tests_require = [
    'flake8-future-import~=0.0,>=0.4.4',
    'flake8~=3.0,>=3.5.0',
    'mock~=2.0,>=2.0.0',
    'pytest-cov~=2.0,>=2.5.1',
    'pytest~=3.0,>=3.5.0',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
    'tests:python_version=="2.7"': [
        'unicode-string-literal~=1.0,>=1.1',
    ],
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name not in ['all', 'tests:python_version=="2.7"']:
        extras_require['all'].extend(reqs)

packages = find_packages(exclude=['docs', 'tests'])

setup(
    name='zulip-inspire-bot',
    autosemver={
        'bugtracker_url': url + '/issues',
    },
    url=url,
    license='GPLv3',
    author='CERN',
    author_email='admin@inspirehep.net',
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    description=__doc__,
    long_description=readme,
    setup_requires=setup_requires,
    install_require=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)