# challenge_11.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
from linux_story.StepTemplate import StepTemplate
from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.step_helper_functions import unblock_commands
from linux_story.common import tq_file_system, get_story_file
from linux_story.helper_functions import wrap_in_box


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


# The next few steps should be like the disappearing of people in the town
class Step1(StepTemplateCd):
    story = [
        ("You see a group of scared looking people and a {{bb:dog}}.\n"),
        ("{{lb:Listen}} to what they have to say with {{yb:cat}}.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"

    # Use functions here
    all_commands = {
        "cat Edith": ("{{wb:Edith:}} {{Bb:\"You found us! Edward, I told you to keep your voice down.\"}}"),
        "cat Eleanor": ("{{wb:Eleanor:}} {{Bb:\"My mummy is scared the bell will find us if we go outside.\"}}"),
        "cat Edward": ("{{wb:Edward:}} {{Bb:\"I'm sorry Edith...but I don't think they mean any harm. "
                        "Maybe they could help us?\"}}"),
        "cat dog": ("{{wb:Dog:}} {{Bb:\"Woof woof!\"}}")
    }

    def check_command(self, line):

        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = ("{{gb:You look around.}}")
            self.send_hint(hint)
            return False

        end_dir_validated = self.get_fake_path() == self.end_dir

        # if the validation is included
        if line in list(self.all_commands.keys()) and end_dir_validated:
            # Print hint from person
            hint = self.all_commands[self._last_user_input]
            self.all_commands.pop(self._last_user_input, None)

            if len(self.all_commands) > 0:
                hint += ("\n{{gb:Well done! Check on %d more.}}") % len(self.all_commands)
            else:
                hint += ("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")

            self.send_hint(hint)

        else:
            self.send_hint(("{{rb:Use}} {{yb:%s}} {{rb:to progress.}}") % list(self.all_commands.keys())[0])

        # Don't pass unless the user has emptied self.all_commands
        return False

    def __next__(self):
        return 11, 2


class Step2(StepTemplateMv):
    story = [
        ("Edward looks like he has something he wants to say to you.\n"),
        ("{{wb:Edward:}} {{Bb:\"Hey! Can you help me?\"}}"),

        ("{{Bb:\"I've been trying to move this}} {{bb:apple}} {{Bb:into the}} {{bb:basket}}{{Bb:.\"}}"),

        ("{{Bb:\"I was told the command}} {{yb:mv apple basket/}} {{Bb:would make it happen, but I can't seem to make "
          "it work. Do you have the power to make it happen?\"}}\n"),
    ]

    story += wrap_in_box([
        ("{{gb:New Power}}: to {{lb:move}} objects, type {{yb:mv}}"),
        ("and the object name."),
    ])

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "mv apple basket",
        "mv apple basket/"
    ]
    highlighted_commands = ['mv']
    hints = [
        ("{{rb:Use the command}} {{yb:mv apple basket/}} {{rb:to move the apple into the basket.}}")
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def __next__(self):
        return 11, 3


class Step3(StepTemplateMv):
    story = [
        ("Check you've managed to move the {{bb:apple}}. {{lb:Look around}} in this directory.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        ("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]
    file_list = [
        {
            "path": "~/town/.hidden-shelter/basket/apple",
            "contents": get_story_file("apple"),
            "type": "file"
        }
    ]

    def __next__(self):
        return 11, 4


class Step4(StepTemplateMv):
    story = [
        ("{{gb:Nice work! The apple isn't in this directory anymore.}}\n"),
        ("{{wn:Now check the apple is in the}} {{bb:basket}} {{wn:using}} {{yb:ls}}{{wn:.}}\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls basket",
        "ls basket/",
        "ls -a basket",
        "ls -a basket/"
    ]
    hints = [
        ("{{rb:Use the command}} {{yb:ls basket/}} {{rb:to look in the basket.}}")
    ]

    def __next__(self):
        return 11, 5


class Step5(StepTemplateMv):
    story = [
        ("{{gb:Excellent, you moved the apple into the basket!}}"),
        ("\n{{wb:Edward:}} {{Bb:\"Wow, you did it!\"}}"),
        ("{{Bb:\"Can you also move the}} {{bb:apple}} {{Bb:from the}} {{bb:basket}} "
          "{{Bb:back to here?\"}}\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "mv basket/apple .",
        "mv basket/apple ./"
    ]
    hints = [
        ("{{rb:Use the command}} {{yb:mv basket/apple ./}} {{rb:to move the apple from the basket to your current "
          "position}} {{bb:./}}")
    ]

    def block_command(self, line):
        if line == "mv basket/apple":
            hint = ("{{gb:Nearly! The full command is}} {{yb:mv basket/apple ./}} {{gb:- don't forget the dot!}}")
            self.send_hint(hint)
            return True
        else:
            return unblock_commands(line, self.commands)

    def __next__(self):
        return 11, 6


class Step6(StepTemplateMv):
    story = [
        ("{{wb:Edith:}} {{Bb:\"You should stop playing with that, that's the last of our food.\"}}"),
        ("{{Bb:\"Ah! The dog ran outside!\"}}"),
        ("{{wb:Eleanor:}} {{Bb:\"Doggy!\"}}"),
        ("{{wb:Edith:}} {{Bb:\"No, honey! Don't go outside!\"}}"),
        ("\n{{bb:Eleanor}} follows her {{bb:dog}} and leaves the {{bb:.hidden-shelter}}."),
        ("{{lb:Look around}} to check this.\n")
    ]
    file_list = [
        {"path": "~/town/Eleanor"},
        {"path": "~/town/dog"}
    ]
    deleted_items = [
        '~/town/.hidden-shelter/Eleanor',
        '~/town/.hidden-shelter/dog'
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls", "ls -a"
    ]
    hints = [
        ("{{rb:Look around using}} {{yb:ls}} {{rb:to check if Eleanor is here.}}")
    ]

    def __next__(self):
        return 11, 7


class Step7(StepTemplateMv):
    story = [
        ("{{wb:Edith:}} {{Bb:\"No! Honey, come back!!!\"}}"),
        ("{{Bb:\"You, please, save my little girl!\"}}\n"),

        ("First, {{lb:look outside}} for {{bb:Eleanor}} with {{yb:ls ../}}"),
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = ""
    commands = [
        "ls ..",
        "ls ../",
        "ls ~/town",
        "ls ~/town/"
    ]
    hints = [
        ("{{rb:Look in the town directory by using either}} {{yb:ls ../}} {{rb:or}} {{yb:ls ~/town/}}")
    ]

    def __next__(self):
        return 11, 8


class Step8(StepTemplateMv):
    story = [
        ("Now {{lb:move}} {{bb:Eleanor}} from the {{bb:town}} outside {{bb:..}} to your current position {{bb:.}}\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "mv ../Eleanor .",
        "mv ../Eleanor ./",
        "mv ~/town/Eleanor ~/town/.hidden-shelter",
        "mv ~/town/Eleanor ~/town/.hidden-shelter/",
        "mv ~/town/Eleanor .",
        "mv ~/town/Eleanor ./",
        "mv ../Eleanor ~/town/.hidden-shelter",
        "mv ../Eleanor ~/town/.hidden-shelter/",
    ]
    hints = [
        ("{{rb:Quick! Use}} {{yb:mv ../Eleanor ./}} {{rb:to move the little girl back to safety.}}")
    ]
    girl_file = os.path.join(tq_file_system, '~/town/.hidden-shelter/Eleanor')

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def check_command(self, line):

        if os.path.exists(self.girl_file):
            return True

        else:
            self.send_stored_hint()
            return False

    def __next__(self):
        return 12, 1
