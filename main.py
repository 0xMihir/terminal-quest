#!/usr/bin/env python

# linux-story
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


import sys
import os
import signal



from kano_profile.apps import load_app_state_variable, save_app_state_variable

from linux_story.launch_functions import launch_project
from linux_story.common import get_max_challenge_number

# Reset the terminal. Not sure why this should be necessary,
# but it seems to be:
os.system('reset')

if __name__ == "__main__":
    # Arguments are pipe filename, and then optionally
    # the Challenge and Step numbers
    if len(sys.argv) == 3:
        if sys.argv[1].isdigit() and sys.argv[2].isdigit():
            launch_project(int(sys.argv[1]), int(sys.argv[2]))

    elif len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            launch_project(int(sys.argv[1]), 1)

    elif len(sys.argv) == 1:
        challenge = 0
        profile_level = load_app_state_variable("linux-story", "level")
        on_stable_version = load_app_state_variable(
            "linux-story", "stable-version"
        )

        # If the user has not launched the stable version of linux story
        # before.
        # This is for the people who completed Terminal Quest on when it was
        # in the experimental category.
        if not on_stable_version:
            # Reset progress
            save_app_state_variable("linux-story", "level", 0)
            # Tell profile the user is now on the stable version
            save_app_state_variable('linux-story', 'stable-version', 1)

        elif on_stable_version and profile_level:
            challenge = profile_level + 1

        # If the project was completed previously, just start over
        max_challenge = get_max_challenge_number()
        if challenge > max_challenge:
            challenge = 0

        launch_project(challenge, 1)
    else:
        sys.exit("Wrong number of arguments!")
