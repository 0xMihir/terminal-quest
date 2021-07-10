# introduction.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
from linux_story.KanoCmd import KanoCmd
from linux_story.StepTemplate import StepTemplate


class StepTemplateLs(StepTemplate):
    TerminalClass = KanoCmd


class Step1(StepTemplateLs):
    story = [
        ("Hello {}.").format("{{yb:" + os.environ['LOGNAME'] + "}}"),
        ("Welcome to the Terminal."),
        ("A wild and wondrous world where words wield power. These words are called commands."),
        ("Want new powers? Press {{gb:Enter}} to begin.")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    def __next__(self):
        return 1, 1
