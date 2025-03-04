#!/usr/bin/env python

from shutil import which as find_executable
from setuptools import setup, Extension, find_packages
import pkg_resources
from setuptools.command.build_py import build_py
# import pip parse_requirements

import sys
import os
import errno
import pathlib
from kSpider_version import get_version

if sys.version_info[:2] < (3, 8):
    raise RuntimeError("Python version >=3.8")

if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')


try:
    readme = pathlib.Path('README.md').read_text()
except IOError:
    readme = ''

if os.path.islink("kSpider_BUILD_DIR"):
    os.unlink("kSpider_BUILD_DIR")

if os.path.exists("build/libkSpider.a"):
    os.symlink("build", "kSpider_BUILD_DIR")


def check_exist(dirs):
    all_exists = True
    not_found_files = []
    for directory in dirs:
        if not (os.path.isdir(directory)):
            print(f"[ERROR] | DIR: {directory} does not exist.", file=sys.stderr)
            all_exists = False
            not_found_files.append(directory)

    if not all_exists:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ",".join(not_found_files))


SOURCES = [
    'src/swig_interfaces/kSpider_internal.i',
    'lib/kProcessor/src/kDataFrames/kDataFrame.cpp',
    'lib/kProcessor/src/algorithms.cpp',
]

if not find_executable('swig'):
    sys.exit("Error:  Building this module requires 'swig' to be installed")

INCLUDES = [
    'include',
    'lib/argh',
    'lib/kProcessor/include/kProcessor',
    'lib/kProcessor/ThirdParty/MQF/include',
    'lib/kProcessor/ThirdParty/kmerDecoder/include',
    'lib/kProcessor/ThirdParty/kmerDecoder/lib/kseq/include',
    'lib/kProcessor/ThirdParty/sdsl-lite/include',
    'lib/kProcessor/ThirdParty/ntCard/include',
    'lib/kProcessor/ThirdParty/kmerDecoder/lib/parallel-hashmap',
    'lib/json_parser/lib/include',
    'lib/zstr/src',
]

check_exist(INCLUDES)

LINK_ARGS = [
    "-fopenmp",
    "-lgomp",
    "-lbz2",
    "-lz",
    "-ldl",
]

kSpider_BUILD_DIR_dir = "kSpider_BUILD_DIR"

LIBRARIES_DIRS = [
    f"{kSpider_BUILD_DIR_dir}/lib/kProcessor",
    f"{kSpider_BUILD_DIR_dir}",
    f"{kSpider_BUILD_DIR_dir}/lib/kProcessor/ThirdParty/MQF/src",
    "lib/kProcessor/ThirdParty/ntCard",
    f"{kSpider_BUILD_DIR_dir}/lib/kProcessor/ThirdParty/sdsl-lite/lib",
    f"{kSpider_BUILD_DIR_dir}/lib/kProcessor/ThirdParty/kmerDecoder",
    f"{kSpider_BUILD_DIR_dir}/lib/kProcessor/ThirdParty/MQF/ThirdParty/stxxl/lib",
]

check_exist(LIBRARIES_DIRS)

LIBRARIES = [
    'kProcessor',
    'kSpider',
    'sdsl',
    'MQF',
    'ntcard',
    'kmerDecoder',
    'stxxl_debug',
]

SWIG_OPTS = [
    '-c++',
    # '-py3',
    # '-keyword',
    '-outdir',
    './pykSpider/'
]


class CustomBuild(build_py):
    def run(self):
        self.run_command('build_ext')
        self.run_command('build_clib')
        super().run()


kSpider_module = Extension('_kSpider_internal',
                           library_dirs=LIBRARIES_DIRS,
                           libraries=LIBRARIES,
                           sources=SOURCES,
                           include_dirs=INCLUDES,
                           extra_link_args=LINK_ARGS,
                           extra_compile_args=["-O3", "-Ofast", "-std=c++17", "-fPIC"],
                           swig_opts=SWIG_OPTS,
                           )

classifiers = [
    "License :: OSI Approved :: Apache Software License",
    'Development Status :: 3 - Alpha',
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

from setuptools.command.build_py import build_py
class BuildPy(build_py):
    def run(self):
        self.run_command('build_ext')
        super(build_py, self).run()


with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(name='DBRetina',
      version=get_version(),
      description="""DBRetina Python Package""",
      ext_modules=[kSpider_module],
      py_modules=['kSpider_internal'],
      packages=find_packages('pykSpider'),
      package_dir={'': 'pykSpider'},
      python_requires='>=3.8',
      cmdclass={'build_py': BuildPy},
      license='BSD 3-Clause',
      long_description_content_type='text/markdown',
      long_description=readme,
      classifiers=classifiers,
      install_requires=install_requires,
      include_package_data=True,
      entry_points='''
        [console_scripts]
        DBRetina=kSpider2:cli
    ''',
      project_urls={
          'Bug Reports': 'https://github.com/DBRetina/DBRetina/issues',
          'Source': 'https://github.com/DBRetina/DBRetina/issues',
      },
      )

if os.path.exists("build/libkSpider.a") and os.path.islink("kSpider_BUILD_DIR"):
    os.unlink("kSpider_BUILD_DIR")
