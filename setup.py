"""
YANK is a testbed for experimenting with algorithms for the efficient computation of small molecule binding free energies to biomolecular targets using alchemical methods.
YANK is built on OpenMM, the API for molecular simulation, and uses its GPU-accelerated library implementation for hardware acceleration.
"""
from __future__ import print_function
import os
import sys
from os.path import relpath, join
from setuptools import setup, find_packages
import subprocess
DOCLINES = __doc__.split("\n")

########################
VERSION = "0.9.0"
ISRELEASED = False
__version__ = VERSION
########################
CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: Lesser GNU Public License (LGPL)
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering :: Bio-Informatics
Topic :: Scientific/Engineering :: Chemistry
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""


def find_package_data():
    files = []
    for root, dirnames, filenames in os.walk('yank'):
        for fn in filenames:
            files.append(relpath(join(root, fn), 'yank'))
    return files


def check_dependencies():
    from distutils.version import StrictVersion
    found_openmm = True
    found_openmm_52_or_later = True
    found_numpy = True

    try:
        from simtk import openmm
        openmm_version = StrictVersion(openmm.Platform.getOpenMMVersion())
        if openmm_version < StrictVersion('5.2'):
            found_openmm_52_or_later = False
    except ImportError as err:
        found_openmm = False

    try:
        import numpy
    except:
        found_numpy = False

    msg = None
    bar = ('-' * 70) + "\n" + ('-' * 70)
    if found_openmm:
        if not found_openmm_52_or_later:
            msg = [bar, '[Unmet Dependency] YANK requires OpenMM version 5.2 or later. You have version %s.' % openmm_version, bar]
    else:
        msg = [bar, '[Unmet Dependency] YANK requires the OpenMM python package. Refer to <http://openmm.org> for details and installation instructions.', bar]

    if not found_numpy:
        msg = [bar, '[Unmet Dependency] YANK requires the numpy python package. Refer to <http://www.scipy.org/scipylib/download.html> for numpy installation instructions.', bar]

    if msg is not None:
        import textwrap
        print()
        print(os.linesep.join([line for e in msg for line in textwrap.wrap(e)]), file=sys.stderr)
        #print('\n'.join(list(textwrap.wrap(e) for e in msg)))




################################################################################
# Writing version control information to the module
################################################################################

def git_version():
    # Return the git revision as a string
    # copied from numpy setup.py
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION


def write_version_py(filename='yank/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM yank setup.
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()


write_version_py()



setup(
    name='yank',
    author='John Chodera',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    version=__version__,
    license='LGPL',
    url='https://github.com/choderalab/yank',
    platforms=['Linux', 'Mac OS-X', 'Unix', 'Windows'],
    classifiers=CLASSIFIERS.splitlines(),
    packages=find_packages(),
    package_data={'yank': find_package_data()},
    zip_safe=False,
    install_requires=[],
    entry_points={'console_scripts': ['yank = yank.yank:main', 'yank-analyze = yank.analyze:main']})

check_dependencies()
