#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.file_creation.FileTree import modify_permissions
from linux_story.helper_functions import wrap_in_box
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.terminals.terminal_rm import TerminalRm


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


REPLY_PRINT_TEXT = ("{{yb:A rabbit came and stole the command in front of me.}}")


class Step1(StepTemplateChmod):
    story = [
        ("You stand alone in the library. The Rabbit has stolen the command."),
        ("There is a growing sense of impending doom. Then, the Swordmaster runs into the room."),
        "",
        ("Swordmaster: {{Bb:\"What have you done?\"}}"),
        "",
        "{{yb:1:}} " + REPLY_PRINT_TEXT,
        ("{{yb:2: Nothing.}}")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    file_list = [
        {
            "path": "~/town/east/library/private-section/Swordmaster",
            "contents": get_story_file("swordmaster"),
            "permissions": 0o644,
            "type": "file"
        }
    ]
    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        ("Swordmaster: {{Bb:\"Speak with}} {{lb:echo}} {{Bb:and tell me!\"}}")
    ]
    dark_theme = True

    def _run_at_start(self):
        modify_permissions("~/woods/thicket/rabbithole", 0000)

    def __next__(self):
        if self._last_user_input == "echo 2":
            return 43, 100
        else:
            return 43, 2


class Step100(StepTemplateChmod):
    story = [
        ("Swordmaster: {{rb:\"ENOUGH!\"}}"),
        ("{{Bb:\"Tell me}} {{rb:the truth.\"}}"),
        ("{{Bb:\"You need my help to fix this....\"}}"),
        "",
        ("{{yb:1:}} " + REPLY_PRINT_TEXT),
        ("{{yb:2: Nothing.}}")
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    hints = [
        ("{{rb:Tell the Swordmaster the truth, using}} {{yb:echo 1}}")
    ]
    dark_theme = True

    def check_command(self, last_user_input):
        if last_user_input == "echo 2":
            self.send_hint(
                ("Swordmaster: {{Bb:\"We both know that's not true....\"}}")
            )
            return
        return StepTemplateChmod.check_command(self, last_user_input)

    def __next__(self):
        return 43, 2


class Step2(StepTemplateChmod):
    print_text = [REPLY_PRINT_TEXT]
    story = [
        ("Swordmaster: {{Bb:\"A Rabbit? Truth be told, I often see a white rabbit in a thicket near my house.\"}}"),
        ("{{Bb:\"But it always seemed so innocent, I would never have guessed it could do something like this.\"}}"),
        ("{{Bb:\"I wonder what has changed? Perhaps...hmm...the bell...\"}}"),
        ("{{Bb:\"We must remove the source of the problem. I will teach you how.\"}}"),
        "",
        ("{{pb:Ding. Dong.}}"),
        "",
        ("You heard the a bell. {{lb:Look around.}}")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]
    hints = [
        ("{{rb:Look around with}} {{yb:ls}}")
    ]
    file_list = [
        {
            "path": "~/town/east/library/private-section/sword",
            "contents": get_story_file("RM-sword"),
            "type": "file",
            "permissions": 0o644
        }
    ]
    dark_theme = True

    deleted_items = ["~/town/east/library/private-section/Swordmaster"]

    def __next__(self):
        return 43, 3


class Step3(StepTemplateChmod):
    story = [
        ("The Swordmaster has gone."),
        "",
        ("He left something behind. It looks like the {{lb:sword}} he carries around with him."),
        ("{{lb:Examine}} it.")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "cat sword"
    ]
    dark_theme = True

    hints = [
        ("{{rb:Use}} {{yb:cat sword}} {{rb:to examine it.}}")
    ]

    def __next__(self):
        return 43, 4


class Step4(StepTemplateRm):
    story = [
        ("It has a command inscribed on it."),
        "....{{lb:rm}}...?\n"
    ]

    story += wrap_in_box([
        ("{{gb:New Power:}} Use {{yb:rm}} to"),
        (" {{lb:remove an item}}.")
    ])

    story += [
        ("Use {{yb:rm note}}, to test the command out on the note."),
        ("Be careful though....it looks dangerous.")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "rm note"
    ]
    highlighted_commands = ["rm"]

    hints = [
        "",
        ("{{rb:Use the command}} {{yb:rm note}}")
    ]
    dark_theme = True

    def __next__(self):
        return 43, 5


class Step5(StepTemplateRm):
    story = [
        ("{{lb:Look around.}}")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls"
    ]

    hints = [
        ("{{rb:Use the command}} {{yb:ls}}")
    ]
    dark_theme = True

    def __next__(self):
        return 44, 1
