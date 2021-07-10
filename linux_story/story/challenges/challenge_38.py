#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

# Redo chapter 5 with the swordmaster.

import os

from linux_story.StepTemplate import StepTemplate
from linux_story.PlayerLocation import generate_real_path
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        ("{{gb:You've found the answer to the Swordmaster's riddle!}}"),
        "",
        ("{{lb:Go back to the Swordmaster's clearing.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/clearing"
    hints = [
        ("Head back to the {{bb:~/woods/clearing}} where the Swordmaster lives."),
        ("{{rb:Use}} {{yb:cd ~/woods/clearing}} {{rb:to go back to the Swordmaster's clearing.}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def __next__(self):
        return 38, 2


class Step2(StepTemplateChmod):
    story = [
        ("Knock on the Swordmaster's door.")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo knock knock"
    ]
    hints = [
        ("{{rb:Use}} {{yb:echo knock knock}} {{rb:to knock on the Swordmaster's door.}}")
    ]

    def __next__(self):
        return 38, 3


class Step3(StepTemplateChmod):
    story = [
        ("Swordmaster:"),
        ("{{Bb:\"If you have me, you want to share me."),
        ("If you share me, you haven't got me."),
        ("What am I?\"}}"),
        "",
        ("{{yb:1. A secret}}"),
        ("{{yb:2. I don't know}}"),
        "",
        ("Use {{lb:echo}} to reply.")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo 1",
        "echo secret",
        "echo a secret",
        "echo A secret",
        "echo \"secret\"",
        "echo \"a secret\"",
        "echo \"A secret\""
    ]

    def check_command(self, line):
        if line.startswith("echo ") and line not in self.commands:
            self.send_hint("Swordmaster: {{Bb:\"Incorrect. Did you finish the challenges in the cave? "
                           "The answer was in there.\"}}")
        return StepTemplateChmod.check_command(self, line)

    def __next__(self):
        path = generate_real_path("~/woods/clearing/house")
        os.chmod(path, 0o755)
        return 38, 4


class Step4(StepTemplateChmod):
    story = [
        ("{{wb:Clunck.}} {{gb:It sounds like the door unlocked.}}"),
        "",
        ("{{lb:Go in the house.}}")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing/house"
    hints = [
        ("{{rb:Use}} {{yb:cd house}} {{rb:to go inside.}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def __next__(self):
        return 38, 5


class Step5(StepTemplateChmod):
    story = [
        ("{{lb:Look around.}}")
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        ("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]
    commands = [
        "ls"
    ]

    def __next__(self):
        return 39, 1
