#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands


GO_TO_THE_LIBRARY = [
    ("The Rabbit wants to know where the Super User command is kept?"),
    "....",
    ("Let's head to the {{bb:~/town/east/library}}."),
    ("It looks as if the Rabbit will follow.")
]

RABBITS_ARE_QUIET = [
    ("Rabbit: {{Bb:...}}"),
    "",
    ("It seems the Rabbit doesn't say very much."),
    ("That's quite normal for rabbits.")
]

RABBIT_BLOCKING_RABBITHOLE = ("The rabbit is in front of the rabbithole and won't let you pass.")


class TerminalRabbit(TerminalChmod):
    def _autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        completions = TerminalChmod._autocomplete_files(self, text, line, begidx, endidx, only_dirs, only_exe)
        if "cage/" in completions or "Mum" in completions:
            print(("\n" + RABBIT_BLOCKING_RABBITHOLE))
            return []
        else:
            return completions


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod

    def block_command(self, line):
        if "rabbithole" in line and ("ls" in line or "cat" in line):
            print(RABBIT_BLOCKING_RABBITHOLE)
            return True
        else:
            return StepTemplate.block_command(self, line)


# Same as the towns people, and the last challenge?
class Step1(StepTemplateChmod):
    story = [
        ("You see a Rabbit, a piece of paper and a rabbithole."),
        ("This Rabbit looks somewhat familiar..."),
        ("{{lb:Listen}} to the Rabbit.")
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    hints = [
        ("{{rb:Use}} {{yb:cat Rabbit}} {{rb:to listen to the Rabbit.}}")
    ]

    read_note = False
    commands = [
        "cat Rabbit"
    ]

    def check_command(self, line):
        if line == "cat note":
            self.read_note = True

        return StepTemplateChmod.check_command(self, line)

    def __next__(self):
        if self.read_note:
            return 41, 4
        else:
            return 41, 2


class Step2(StepTemplateChmod):
    story = RABBITS_ARE_QUIET + ["", ("{{lb:Examine}} the note.")]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    commands = [
        "cat note"
    ]
    hints = [
        ("{{rb:Use}} {{yb:cat note}} {{rb:to examine the note.}}")
    ]

    def __next__(self):
        return 41, 3


class Step3(StepTemplateChmod):
    story = GO_TO_THE_LIBRARY
    start_dir = "~/woods/thicket"
    end_dir = "~/town/east/library"
    hints = [
        ("{{rb:Use}} {{yb:cd ~/town/east/library}} {{rb:to go to the library}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def __next__(self):
        return 42, 1


class Step4(StepTemplateChmod):
    story = RABBITS_ARE_QUIET + [""] + GO_TO_THE_LIBRARY
    start_dir = "~/woods/thicket"
    end_dir = "~/town/east/library"
    hints = [
        ("{{rb:Is this the same place the swordmaster referred to?}}"),
        ("{{rb:Use}} {{yb:cd ~/town/east/library}} {{rb:to go to the library}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def __next__(self):
        return 42, 1
