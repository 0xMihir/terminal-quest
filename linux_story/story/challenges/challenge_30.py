# challenge_30.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os

from linux_story.common import get_story_file
from linux_story.story.challenges.CompanionMisc import StepTemplateEleanorBernard
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_nano import TerminalNano


# ----------------------------------------------------------------------------------------


class StepNano(StepTemplateEleanorBernard):
    TerminalClass = TerminalNano


class Step1(StepNano):
    story = [
        ("{{pb:Ding. Dong.}}\n"),
        ("\nEleanor: {{Bb:\"...what was that?\"}}\n"),
        ("{{lb:Look around.}}")
    ]
    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/restaurant/.cellar"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        ("{{rb:Use}} {{yb:ls}} {{rb:to check everyone is still present.}}")
    ]
    deleted_items = [
        "~/town/east/shed-shop/Bernard"
    ]
    file_list = [
        {
            "path": "~/town/east/shed-shop/Bernards-hat",
            "contents": get_story_file("bernards-hat")
        }
    ]
    companion_speech = ("Eleanor: {{Bb:......}}")

    def __next__(self):
        return 30, 2


class Step2(StepNano):
    story = [
        ("Everyone seems to be here. What was that bell?"),
        ("\n{{bb:Clara}} looks like she has something to say. {{lb:Listen to her.}}")
    ]
    commands = [
        "cat Clara"
    ]
    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/restaurant/.cellar"
    hints = [
        ("{{rb:Use}} {{yb:cat Clara}} {{rb:to see what Clara has to say.}}")
    ]
    companion_speech = \
        ("Eleanor: {{Bb:\"....I was so scared. I don't think I want to go " +\
        "outside now.\"}}")

    def __next__(self):
        return 30, 3


class Step3(StepNano):
    story = [
        ("Clara: {{Bb:\"Are you two going back out there?\"}}"),
        ("{{Bb:\"}}{{gb:%s}}" +\
        "{{Bb:, you look like you can take care of yourself, but " +\
        "I don't feel happy with Eleanor going outside.\"}}")\
        % os.environ['LOGNAME'],
        ("\n{{Bb:\"}}{{gb:%s}}{{Bb:, will you leave Eleanor with me? " +\
        "I'll look after her.\"}}") % os.environ['LOGNAME'],
        ("\n{{yb:1: \"That's a good idea, take good care of her.\"}}"),
        ("{{yb:2: \"No I don't trust you, she's safer with me.\"}}"),
        ("{{yb:3: \"(Ask Eleanor.) Are you happy to stay here?\"}}"),
        # ("{{yb:4: Do you have enough food here?}}"),
        ("\n{{lb:Reply to Clara.}}")
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/restaurant/.cellar"
    hints = [
        ("{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} " +\
        "{{yb:echo 3}} {{rb:to reply to Clara.}}")
    ]
    companion_speech = (
        ("Eleanor: {{Bb:\"I'm happy to stay here. I like Clara.\"}}")
    )

    def check_command(self, line):
        if line == "echo 2":
            text = (
                ("\nClara: {{Bb:\"Please let me look after her. " +\
                "I don't think it's safe for her to go outside.\"}}")
            )
            self.send_hint(text)
        elif line == "echo 3":
            text = ("\nEleanor: {{Bb:\"I'm happy to stay here. I like Clara.\"}}")
            self.send_hint(text)
        else:
            return StepNano.check_command(self, line)

    def __next__(self):
        return 30, 4


class Step4(StepNano):
    story = [
        ("Clara: {{Bb:\"Thank you!\"}}"),
        ("Eleanor: {{Bb:\"When you find my parents, can you tell them I'm " +\
        "here?\"}}"),
        ("Clara: {{Bb:\"Where are you going to go now?\"}}"),
        ("\nLet's head back to see {{bb:Bernard}} and see if he's heard of " +\
        "the {{bb:masked swordmaster}}.\n"),
        ("{{lb:Head to the}} {{bb:shed-shop.}}")
    ]
    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/shed-shop"

    path_hints = {
        "~/town/east/restaurant/.cellar": {
            "blocked": ("\n{{rb:Use}} {{yb:cd ../}} {{rb:to go back.}}")
        },
        "~/town/east/restaurant": {
            "not_blocked": ("\n{{gb:You head upstairs}}"),
            "blocked": ("\n{{rb:Use}} {{yb:cd ../}} {{rb:to go back.}}")
        },
        "~/town/east": {
            "not_blocked": ("\n{{gb:Now go into the}} {{bb:shed-shop}}{{gb:.}}"),
            "blocked": ("\n{{rb:Use}} {{yb:cd shed-shop/}}{{rb:.}}")
        }
    }

    def check_command(self, line):
        if self.get_fake_path() == self.end_dir:
            return True
        elif "cd" in line and not self.get_command_blocked():
            hint = self.path_hints[self.get_fake_path()]["not_blocked"]
        else:
            hint = self.path_hints[self.get_fake_path()]["blocked"]

        self.send_hint(hint)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def __next__(self):
        return 31, 1
