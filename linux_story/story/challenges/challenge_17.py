# challenge_17.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from kano_profile.apps import save_app_state_variable, load_app_state_variable

from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.helper_functions import wrap_in_box


# This is for the challenges that only need ls
class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# This is for that challenges that need echo
class StepTemplateEcho(StepTemplate):
    TerminalClass = TerminalEcho


# ----------------------------------------------------------------------------------------

class Step1(StepTemplateMv):
    story = [
        ("You're in your room, standing in front of the {{bb:.chest}} containing all the commands "
          "you've learned so far.\n"),
        ("Maybe something else is hidden in the house?\n"),
        ("{{lb:Look}} in the hallway {{lb:behind you}}. Remember, behind you is {{bb:..}}")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    file_list = [
        {"path": "~/farm/barn/Cobweb"},
        {"path": "~/farm/barn/Daisy"},
        {"path": "~/farm/barn/Ruth"},
        {"path": "~/farm/barn/Trotter"},
        {"path": "~/farm/toolshed/MKDIR"},
        {"path": "~/farm/toolshed/spanner"},
        {"path": "~/farm/toolshed/hammer"},
        {"path": "~/farm/toolshed/saw"},
        {"path": "~/farm/toolshed/tape-measure"},
        {
            "path": "~/farm/farmhouse/bed",
            "contents": get_story_file("bed_farmhouse")
        },
        {"path": "~/farm/toolshed/MKDIR"},
        {"path": "~/my-house/parents-room/.safe/ECHO"},
        {"path": "~/my-house/parents-room/.safe/mums-diary"},
        {"path": "~/my-house/parents-room/.safe/map"}
    ]
    hints = [
        ("{{rb:Look behind you with}} {{yb:ls ../}}")
    ]
    commands = [
        "ls ..",
        "ls ../"
    ]

    def __next__(self):
        return 17, 2


class Step2(StepTemplateMv):
    story = [
        ("You see doors to your {{bb:garden}}, {{bb:kitchen}}, {{bb:my-room}} and {{bb:parents-room}}."),
        ("We haven't checked out your parents' room properly yet.\n"),
        ("{{lb:Go into your}} {{bb:parents-room}}.")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/parents-room"

    path_hints = {
        "~/my-house/my-room": {
            "blocked": ("\n{{rb:Use}} {{yb:cd ..}} {{rb:to go back.}}")
        },
        "~/my-house": {
            "not_blocked": ("\n{{gb:Now go into your}} {{lb:parents-room}}{{gb:.}}"),
            "blocked": ("\n{{rb:Use}} {{yb:cd parents-room}} {{rb:to go in.}}")
        }
    }

    def check_command(self, line):
        if self._location.get_fake_path() == self.end_dir:
            return True
        elif "cd" in self.get_last_user_input() and not self.get_command_blocked():
            hint = self.path_hints[self._location.get_fake_path()]["not_blocked"]
        else:
            hint = self.path_hints[self._location.get_fake_path()]["blocked"]

        self.send_hint(hint)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def __next__(self):
        Step3()

    def __next__(self):
        return 17, 3


class Step3(StepTemplateMv):
    story = [
        ("Look around {{lb:closely}}.")
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"

    hints = [
        ("{{rb:Use the command}} {{yb:ls -a}} {{rb:to look around closely.}}")
    ]
    commands = [
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def __next__(self):
        return 17, 4


class Step4(StepTemplateMv):
    story = [
        ("There's a {{bb:.safe}}!\n"),
        ("Maybe there's something useful in here. {{lb:Look inside}} the {{bb:.safe}}.")
    ]

    commands = [
        "ls .safe",
        "ls .safe/",
        "ls -a .safe",
        "ls -a .safe/"
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    hints = [
        ("{{rb:Look in the}} {{bb:.safe}} {{rb:using}} {{lb:ls}}{{rb:.}}"),
        ("{{rb:Use}} {{yb:ls .safe}} {{rb:to look into the .safe.}}")
    ]

    def __next__(self):
        return 17, 5


class Step5(StepTemplateMv):
    story = [
        ("So you found your {{bb:Mum's diary}}?"),
        ("You probably shouldn't read it...\n"),
        ("What else is here? Let's {{lb:examine}} that {{bb:map}}.")
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    hints = [
        ("{{rb:Use}} {{yb:cat}} {{rb:to read the}} {{bb:map}}{{rb:.}}"),
        ("{{rb:Use}} {{yb:cat .safe/map}} {{rb:to read the map.}}")
    ]

    commands = "cat .safe/map"

    def check_command(self, line):
        checked_diary = load_app_state_variable("linux-story", "checked_mums_diary")
        if line == 'cat .safe/mums-diary' and not checked_diary:
            self.send_hint(("\n{{rb:You read your Mum\'s diary!}} {{ob:Your nosiness has been recorded.}}"))
            save_app_state_variable("linux-story", "checked_mums_diary", True)
            return False

        return StepTemplateMv.check_command(self, line)

    def __next__(self):
        return 17, 6


class Step6(StepTemplateMv):
    story = [
        ("So there's a farm around here?"),
        ("Apparently it's not far from our house, just off the windy road...\n"),
        ("What is this {{bb:ECHO}} note? {{lb:Examine}} the {{bb:ECHO}} note.")
    ]

    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    commands = "cat .safe/ECHO"
    hints = [
        ("{{rb:Use the}} {{yb:cat}} {{rb:command to read the}} {{bb:ECHO}} {{rb:note.}}"),
        ("{{rb:Use}} {{yb:cat .safe/ECHO}} {{rb:to read the note.}}")
    ]

    def __next__(self):
        return 17, 7


class Step7(StepTemplateEcho):
    story = [
        ("So the note says {{Bb:\"echo hello - will make you say hello\"}}"),
        ("Let's test this out. \n"),
    ]
    story += wrap_in_box([
        ("{{gb:New Power}}: {{yb:echo}} followed by words"),
        ("lets you {{lb:speak}}"),
    ])

    hints = [
        ("{{rb:Use the command}} {{yb:echo hello}}")
    ]
    commands = [
        "echo hello",
        "echo HELLO",
        "echo Hello"
    ]
    highlighted_commands = ['echo']
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"

    def __next__(self):
        return 18, 1
