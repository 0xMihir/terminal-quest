#!/usr/bin/env python

# setup.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from distutils.core import setup
import os
from pathlib import Path


def recursively_get_dirs(package_name, start_dir):

    start_path = os.path.join(package_name, start_dir)
    paths = []

    for root, dir, files in os.walk(start_path):
        for f in files:
            file_path = os.path.join(root, f)

            # If this is package data for linux_story
            if package_name:
                file_path = file_path.replace(package_name + "/", "")

            paths.append(file_path)

    return paths



def get_locales():
    locale_dir = 'locale'
    locales = []

    for dirpath, dirnames, filenames in os.walk(locale_dir):
        for filename in filenames:
            locales.append(
                (str(Path.home().joinpath('.terminal-quest/', dirpath)),
                [str(Path(dirpath).joinpath(filename))])
                )

    return locales


story = recursively_get_dirs("linux_story", "story")
file_creation = recursively_get_dirs("linux_story", "file_creation")
rules = recursively_get_dirs("", "rules")
ascii_assets = recursively_get_dirs("linux_story", "ascii_assets")


setup(name='Linux Story',
      version='1.2',
      description='Story to teach people basic Linux commands',
      author='Team Kano',
      author_email='dev@kano.me',
      url='https://github.com/KanoComputing/linux-tutorial',
      packages=['linux_story',"kano_profile","kano"],
      package_dir={'linux_story': 'linux_story'},
      scripts=['bin/terminal-quest'],
      package_data={
          'linux_story': story + ascii_assets + file_creation
      },
      data_files=[
          (str(Path.home().joinpath('.terminal-quest/kano-profile/rules')), rules),
      ] + get_locales()
      )
