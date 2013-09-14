from pybuilder.core import use_plugin, init, Author

use_plugin("python.install_dependencies")
#use_plugin("copy_resources")
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.distutils")

authors = [Author('Marco Hoyer', 'marco_hoyer@gmx.de')]
description = """icinga-status: a simple wsgi application parsing icingastats output, when queried by http get, responding yaml performance data for icinga.

for more documentation, visit https://github.com/marco-hoyer/icinga-status
"""

name = 'icinga-status'
license = 'GNU GPL v3'
summary = 'icinga-status - perfdata exposure via http/yaml'
url = 'https://github.com/marco-hoyer/icinga-status'
version = '1.0'

default_task = ['publish']


@init
def initialize(project):
    project.port_to_run_on = "9000"

    project.depends_on("yaml")
    project.depends_on("subprocess")

    project.install_file('/var/www', 'icinga-status/icinga-status.wsgi')
    project.install_file('/etc/httpd/conf.d/', 'icinga-status/icinga-status.conf')

    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Monitoring',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ])


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os

    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_dependencies', 'package']
    project.set_property('install_dependencies_use_mirrors', False)
    project.get_property('distutils_commands').append('bdist_rpm')