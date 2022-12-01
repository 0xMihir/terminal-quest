#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.PlayerLocation import generate_real_path
from linux_story.common import get_username
from linux_story.helper_functions import has_write_permissions
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.terminals.terminal_rm import TerminalRm


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm
    dark_theme = True


class StepPeopleInCage(StepTemplateRm):
    commands_done = {
        "cat bell": False,
        "cat Rabbit": False
    }

    def check_command(self, line):
        if line in self.commands:
            return StepTemplateRm.check_command(self, line)
        elif line == "cat Rabbit":
            self.send_hint("Rabbit: {{Bb:...}}\nThe rabbit looks frustrated.")
        elif line == "cat bell":
            self.send_hint("The bell glows menacingly.")
        elif line.startswith("cat cage/"):
            self.send_hint(self.cat_people())
        else:
            return StepTemplateRm.check_command(self, line)

    def cat_people(self):
        people = {
            "Mum": ("Mum: {{Bb:\"" + get_username() + ", I'm so glad to see you, but it's not safe here!\"}}"),

            "Dad": ("Dad: {{Bb:\"" + get_username() + ", strangest thing happened. I was kidnapped by a rabbit! "
                     "Although, it seems to be acting even stranger now.\"}}"),

            "grumpy-man": ("grumpy-man: {{Bb:\"My legs are fixed. I hope my wife knows I'm safe.\"}}"),
            "Mayor": ("Mayor: {{Bb:\"When I get out of here, I'm going to make a law to hunt all rabbits.\"}}"),
            "little-boy": ("little-boy: {{Bb:\"I miss my mummy!\"}}"),
            "young-girl": ("young-girl: {{Bb:\"I don't like being in here.\"}}"),
            "Edith": ("Edith: {{Bb:\"You, " + get_username() + "! Get us out of here!\"}}"),
            "Edward": ("Edward: {{Bb:\"Edith dear, calm down...\"}}"),
            "dog": ("dog: {{Bb:\"Woof woof!\"}}"),
            "Bernard": ("Bernard: {{Bb:\"After you left, I heard this sound\"}}"),
            "head-librarian": ("head-librarian: {{Bb:\"Who are you?\"}}")
        }
        for person in people:
            if self._last_user_input == "cat cage/" + person:
                return people[person]

        return ""


class Step1(StepPeopleInCage):
    story = [
        ("You are in the rabbithole. {{lb:Look around.}}")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "ls",
        "ls ./",
        "ls ."
    ]
    hints = [
        ("{{rb:Look around with}} {{yb:ls}}")
    ]

    def __next__(self):
        return 45, 2


class Step2(StepPeopleInCage):
    story = [
        ("You see the Rabbit, but it seems to be distracted."),
        ("There is also a cage and a mysteriously glowing bell. You sneak over to the cage."),
        ("Swordmaster: {{Bb:\"Psst! We're inside the cage!\"}}"),
        "",
        ("{{lb:Look inside the cage.}}")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        ("{{rb:Use}} {{yb:ls cage}} {{rb:to look inside the cage.}}")
    ]
    commands = [
        "ls cage",
        "ls cage/"
    ]

    def __next__(self):
        return 45, 3


class Step3(StepPeopleInCage):
    story = [
        ("You see all the people who disappeared, looking miserable, inside the cage. Including your Mum and Dad!"),
        ("Swordmaster: {{Bb:\"Hey, listen. I have something to say.\"}}"),
        "",
        ("Speak to your Mum and Dad. You can also listen to the other people trapped. "
          "And when you're ready listen to what the Swordmaster has to say.")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        ("{{rb:Use}} {{yb:cat cage/Swordmaster}} {{rb:to listen to the swordmaster.}}")
    ]
    commands = [
        "cat cage/Swordmaster"
    ]

    def __next__(self):
        return 45, 4


class Step4(StepPeopleInCage):
    story = [
        ("Swordmaster: {{Bb:\"Listen, we don't have much time. But I think it's the bell, "
          "it's controlling the Rabbit. It has mysterious powers.\"}}"),
        "",
        ("{{lb:Examine}} the bell.")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        ("{{rb:Use}} {{yb:cat bell}} {{rb:to examine the bell.}}")
    ]
    commands = [
        "cat bell"
    ]

    def __next__(self):
        return 45, 5


class Step5(StepPeopleInCage):
    story = [
        ("The bell glows menacingly."),
        "",
        ("Swordmaster: {{Bb:\"The Rabbit hasn't figured out how to use the power it stole. But it will soon.\"}}"),
        ("\"{{Bb:Before it does you must let us out of this cage, quietly.\"}}"),
        "",
        ("{{lb:You need to unlock the cage.}}")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        ("Swordmaster: {{Bb:\"We're all trapped in here because the}} {{lb:write}} {{Bb:permissions are removed.\"}}"),
        ("Swordmaster: {{Bb:\"To re-add the write permissions, use}} {{yb:chmod +w cage}}{{Bb:\"}}")
    ]

    def check_command(self, line):
        if has_write_permissions(generate_real_path("~/woods/thicket/rabbithole/cage")):
            return True
        self.send_stored_hint()

    def __next__(self):
        return 45, 6


class Step6(StepPeopleInCage):
    story = [
        ("Swordmaster: {{Bb:\"Now move us to the}} {{bb:~/town}}{{Bb:\"}}"),
        ("{{Bb:\"To move a large group of people use the *. Like this:}} {{yb:mv cage/* ~/town}}{{Bb:\"}}")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        ("{{rb:Use}} {{yb:mv cage/* ~/town}} {{rb:to move all the villagers into the town.}}")
    ]
    commands = [
        "mv cage/* ~/town",
        "mv cage/* ~/town/"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def __next__(self):
        return 45, 7


class Step7(StepTemplateRm):
    story = [
        ("{{lb:Look in ~/town}} to check that you moved all the people safely.")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "ls ~/town",
        "ls ~/town/"
    ]
    hints = [
        ("{{rb:Use}} {{yb:ls ~/town}} {{rb:to check you moved everyone.}}")
    ]

    def __next__(self):
        return 46, 1
