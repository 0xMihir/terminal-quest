#
# badges.py
#
# Copyright (C) 2014 - 2018 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from __future__ import division

import os
import json
import itertools
from copy import deepcopy

from kano.logging import logger
from kano.utils import read_json, run_bg
from .paths import xp_file, levels_file, rules_dir, bin_dir, \
    app_profiles_file, online_badges_dir, online_badges_file
from .apps import load_app_state, get_app_list, save_app_state
# from .quests import Quests

is_gui = False

def save_app_state_with_dialog(app_name, data):
    logger.debug("save_app_state_with_dialog {}".format(app_name))


    save_app_state(app_name, data)



def save_app_state_variable_with_dialog(app_name, variable, value):
    logger.debug(
        'save_app_state_variable_with_dialog {} {} {}'
        .format(app_name, variable, value)
    )

    data = load_app_state(app_name)
    data[variable] = value

    save_app_state_with_dialog(app_name, data)
