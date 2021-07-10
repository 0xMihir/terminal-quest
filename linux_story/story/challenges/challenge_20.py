# challenge_20.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.step_helper_functions import unblock_commands_with_mkdir_hint, unblock_cd_commands
from linux_story.helper_functions import wrap_in_box


class StepTemplateEcho(StepTemplate):
    TerminalClass = TerminalEcho


class StepTemplateMkdir(StepTemplate):
    TerminalClass = TerminalMkdir


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateEcho):
    print_text = [
        ("{{yb:\"Some people survived by going into hiding.\"}}")
    ]
    story = [
        ("Ruth: {{Bb:\"Oh! That reminds me, my husband used " +
        "to build special shelters to store crops in over winter. " +
        "I think he used a specific tool. " +
        "We should take a look in his toolshed to see if we can find it.\"}}"),
        ("\nUse the {{lb:cd}} command to go into the {{bb:toolshed}}.\n")
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/toolshed"
    hints = [
        ("{{rb:Go to the toolshed in one step using}} {{yb:cd ../toolshed}}")
    ]

    path_hints = {
        "~/farm/barn": {
            "blocked": ("\n{{rb:Use}} {{yb:cd ..}} {{rb:to go back.}}")
        },
        "~/farm": {
            "not_blocked": ("\n{{gb:You walk outside. Now go into the}} {{bb:toolshed}}{{gb:.}}"),
            "blocked": ("\n{{rb:Use}} {{yb:cd toolshed}} {{rb:to go in the toolshed.}}")
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
        return 20, 2


class Step2(StepTemplateEcho):
    story = [
        ("{{bb:Ruth}} follows you into the {{bb:toolshed}}. It's a very large " +\
        "space with tools lining the walls.\n"),
        ("Ruth: {{Bb:\"Let's}} {{lb:look around}} {{Bb:for " +\
        "anything that could be useful.\"}}\n")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    hints = [
        ("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./",
        "ls -a .",
        "ls -a ./"
    ]
    # Move Ruth into toolshed
    file_list = [
        {
            "path": "~/farm/toolshed/Ruth",
            "contents": get_story_file("Ruth"),
            "type": "file"
        }
    ]
    deleted_items = ["~/farm/barn/Ruth"]

    def __next__(self):
        return 20, 3


class Step3(StepTemplateEcho):
    story = [
        ("Ruth: {{Bb:\"Ah, look! There are some instructions with the word}} {{bb:MKDIR}} {{Bb:on it.\"}}"),
        ("{{Bb:\"What does it say?\"}}"),
        "",
        ("{{lb:Examine}} the {{bb:MKDIR}} instructions.")
    ]
    hints = [
        ("Ruth: {{Bb:\"...you are able to read, yes? You use}} {{yb:cat}} {{Bb:to read things.\"}}"),
        ("Ruth: {{Bb:\"What do you kids learn in schools nowadays...\"}}"),
        ("{{Bb:\"Just use}} {{yb:cat MKDIR}} {{Bb:to read the paper.\"}}"),
        ("{{rb:Use}} {{yb:cat MKDIR}} {{rb:to read it.}}")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = [
        "cat MKDIR"
    ]

    def __next__(self):
        return 20, 4


class Step4(StepTemplateMkdir):
    story = [
        ("Ruth: {{Bb:\"This says you can make something using the word}} {{yb:mkdir}}{{Bb:?\"}}"),
        ("\nTry making an igloo using {{yb:mkdir igloo}}\n "),
    ]

    story += wrap_in_box([
        ("{{gb:New Power}}: {{yb:mkdir}} followed by a word"),
        ("lets you {{lb:create}} a shelter"),
    ])

    hints = [
        ("{{rb:Create an igloo structure by using}} {{yb:mkdir igloo}}\n")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = [
        "mkdir igloo"
    ]
    highlighted_commands = ['mkdir']

    def block_command(self, line):
        return unblock_commands_with_mkdir_hint(line, self.commands)

    def check_command(self, line):
        if line == "cat MKDIR":
            self.send_hint(("\n{{gb:Well done for checking the page again!}}"))
            return False

        return StepTemplateMkdir.check_command(self, line)

    def __next__(self):
        return 20, 5


class Step5(StepTemplateMkdir):
    story = [
        ("Now have a {{lb:look around}} and see what's changed.")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./"
    ]
    hints = [
        ("{{rb:Look around using}} {{yb:ls}}{{rb:.}}")
    ]

    def __next__(self):
        return 21, 1
