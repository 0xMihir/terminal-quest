# challenge_31.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_nano import TerminalNano


class StepTemplateNano(StepTemplate):
    TerminalClass = TerminalNano


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateNano):
    story = [
        ("You've arrived in the {{bb:shed-shop}}. {{lb:Look around.}}")
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        ("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    def __next__(self):
        return 31, 2


class Step2(StepTemplateNano):
    story = [
        ("Huh, you can't see {{bb:Bernard}} anywhere."),

        ("I wonder where he went.\n"),

        ("Maybe he's in his {{bb:basement}}? Let's {{lb:go}} down there.")
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop/basement"
    hints = [
        ("{{rb:Go into the basement with}} {{yb:cd basement}}")
    ]

    def check_command(self, line):
        if line == "cat Bernards-hat":
            self.send_hint(("\nIs that Bernard\'s hat? Strange he left it behind..."))
        else:
            return StepTemplateNano.check_command(self, line)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def __next__(self):
        return 31, 3


class Step3(StepTemplateNano):
    story = [
        ("You walked into {{bb:Bernard}}'s basement. {{lb:Look around.}}")
    ]
    start_dir = "~/town/east/shed-shop/basement"
    end_dir = "~/town/east/shed-shop/basement"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        ("{{rb:Look around with}} {{yb:ls}}{{rb:.}}")
    ]

    def __next__(self):
        return 31, 4


class Step4(StepTemplateNano):
    story = [
        ("You see what looks like another script and a couple of diaries."),
        "",
        ("Shall we {{lb:examine}} them?")
    ]
    start_dir = "~/town/east/shed-shop/basement"
    end_dir = "~/town/east/shed-shop/basement"
    commands = [
        "cat bernards-diary-1",
        "cat bernards-diary-2",
        "cat photocopier.sh"
    ]
    hints = [
        ("{{rb:Use}} {{yb:cat}} {{rb:to examine the objects around you.}}")
    ]

    def check_command(self, line):
        if line in self.commands:
            self.commands.remove(line)

            if not self.commands:
                text = ("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")
                self.send_hint(text)
            else:
                text = ("\n{{gb:Well done! Look at the other objects.}}")
                self.send_hint(text)

        elif not line and not self.commands:
            return True

        else:
            return StepTemplateNano.check_command(self, line)

    def __next__(self):
        return 32, 1
