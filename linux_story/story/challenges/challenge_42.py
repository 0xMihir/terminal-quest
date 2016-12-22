#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import time
from threading import Thread

from linux_story.common import get_story_file
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.challenges.challenge_43 import Step10 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 42


# Make the rabbit follow whether the user goes.
# If the user does cat rabbit, the rabbit should reply with his emotions
# depending on how far he is from the locked room
class Step1(StepTemplateChmod):
    story = [
        "Now, which is the locked room? {{lb:Look around}} to remind yourself."
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    file_list = [
        {
            "path": "~/town/east/library/Rabbit",
            "contents": get_story_file("Rabbit"),
            "permissions": 0644,
            "type": "file"
        }
    ]
    deleted_items = [
        "~/woods/thicket/Rabbit",
        "~/woods/thicket/note"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Ah, it's the {{lb:private-section}}.",
        "The Rabbit looks very excited. His eyes are sparkling.",
        "How do you unlock the {{lb:private-section}}? It was the command "
        "that the swordmaster talked about..."
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"
    commands = [
        "chmod +rwx private-section",
        "chmod +rwx private-section/",
        "chmod +wxr private-section",
        "chmod +wxr private-section/",
        "chmod +xrw private-section",
        "chmod +xrw private-section/",
        "chmod +rxw private-section",
        "chmod +rxw private-section/",
        "chmod +xwr private-section",
        "chmod +xwr private-section/",
        "chmod +wxr private-section",
        "chmod +wxr private-section/"
    ]

    hints = [
        "{{rb:The command was}} {{lb:chmod}}{{rb:, and you need to enable "
        "all the permissions.}}",
        "{{rb:The command is}} {{yb:chmod +rwx private-section}} {{rb:to "
        "enable all the permissions.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Awesome, you unlocked it! Let's go inside."
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library/private-section"
    hints = [
        "{{rb:Use}} {{yb:cd private-section/}} {{rb:to go inside the}} "
        "{{rb:private-section.}}"
    ]
    file_list = [
        {
            "path": "~/town/east/library/private-section/chest/scroll",
            "contents": get_story_file("SUDO"),
            "permissions": 0644,
            "type": "file"
        },
        {
            "path": "~/town/east/library/private-section/torn-note",
            "contents": get_story_file("torn-note"),
            "permissions": 0644,
            "type": "file"
        }
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "Have a look around."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls",
        "ls -a",
        "cat chest/scroll"
    ]
    file_list = [
        {
            "path": "~/town/east/library/private-section/Rabbit",
            "contents": get_story_file("Rabbit"),
            "permissions": 0644,
            "type": "file"
        }
    ]
    deleted_items = ["~/town/east/library/Rabbit"]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateChmod):
    story = [
        "You see a chest.",
        "This looks like the treasure we were looking for.",
        "The Rabbit looks more excited than you've ever seen him before.",
        "He snatches the chest and runs off!",
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    deleted_items = [
        "~/town/east/library/private-section/Rabbit",
        "~/town/east/library/private-section/chest"
    ]

    def next(self):
        script_path = os.path.expanduser("~/weekend-work-2/terminal-Quest/bin/rabbit")
        os.system(script_path)
        t = Thread(target=self.timeout_dark_theme)
        t.start()
        Step8()

    def timeout_dark_theme(self):
        time.sleep(3)
        self.send_dark_theme()


class Step8(StepTemplateChmod):
    story = [
        "The place shivers...and then everything goes black.",
        "{{gb:Press ENTER to continue.}}"
    ]

    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    def next(self):
        NextStep(self.xp)
