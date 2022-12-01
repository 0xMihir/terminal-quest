#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.PlayerLocation import generate_real_path
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.helper_functions import has_write_permissions, has_read_permissions, has_execute_permissions
from linux_story.story.terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        ("You set off the firework!"),
        ("{{gb:You learnt all the chmod commands.}}"),
        "",
        ("{{lb:Thunk.}}"),
        "",
        ("Something new landed in front of you."),
        ("{{lb:Look around}} to see what it is.")
    ]
    file_list = [
        {
            "path": "~/woods/cave/chest",
            "permissions": 0000,
            "type": "directory"
        },
        {
            "path": "~/woods/cave/chest/answer",
            "type": "file",
            "permissions": 0o644,
            "contents": get_story_file("answer-cave")
        },
        {
            "path": "~/woods/cave/chest/riddle",
            "type": "file",
            "permissions": 0o644,
            "contents": get_story_file("riddle-cave")
        }
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        ("{{rb:Use}} {{yb:ls}} {{rb:to see what landed in front of you.}}")
    ]
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def __next__(self):
        return 37, 2


class Step2(StepTemplateChmod):
    story = [
        ("There is a {{bb:chest}} in front of you."),
        ("It is wrapped tightly by a big chain."),
        ("{{lb:Look inside the chest.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        ("{{rb:Use}} {{yb:ls chest}} {{rb:to see inside the chest.}}")
    ]
    commands = [
        "ls chest",
        "ls chest/"
    ]

    def __next__(self):
        return 37, 3


class Step3(StepTemplateChmod):
    story = [
        ("The chain won't budge. You cannot see inside, nor access its contents."),
        "",
        ("Break the chain."),
        ("{{lb:You'll need to combine all the chmod flags you've just learned: r, w, and x.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        "{{rb:Use}} {{yb:chmod +rwx chest}} {{rb:to unlock the chest.}}"
    ]

    def check_command(self, line):
        chest = generate_real_path("~/woods/cave/chest")
        if has_write_permissions(chest) and has_read_permissions(chest) and has_execute_permissions(chest):
            return True
        self.send_stored_hint()

    def __next__(self):
        return 37, 4


class Step4(StepTemplateChmod):
    story = [
        ("{{gb:You opened it!}}"),
        ("Now {{lb:look inside}} the chest.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"

    commands = [
        "ls chest",
        "ls chest/"
    ]

    hints = [
        ("{{rb:Use}} {{yb:ls chest/}} {{rb:to look inside the chest.}}")
    ]

    def __next__(self):
        return 37, 5


class Step5(StepTemplateChmod):
    story = [
        ("You see a riddle, and an answer. {{lb:Examine}} them.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat chest/answer"
    ]
    hints = [
        ("{{rb:Use}} {{yb:cat chest/answer}} {{rb:to examine the answer in the chest.}}")
    ]

    def check_command(self, last_user_input):
        if last_user_input == "cat chest/riddle":
            self.send_hint(
                ("{{gb:That looks like the riddle the swordmaster asked you.}}")
            )
            return
        return StepTemplateChmod.check_command(self, last_user_input)

    def __next__(self):
        return 38, 1
