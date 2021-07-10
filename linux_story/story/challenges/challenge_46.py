#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.Animation import Animation
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file, get_username
from linux_story.helper_functions import wrap_in_box
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_sudo import TerminalSudo
from linux_story.story.terminals.terminal_rm import TerminalRm


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


class StepTemplateSudo(StepTemplate):
    TerminalClass = TerminalSudo


class Step1(StepTemplateRm):
    story = [
        ("{{gb:Brilliant! You saved all the villagers.}}"),
        ("You are alone with the Rabbit and the bell. The Rabbit turns angrily and starts running towards you."),
        "",
        ("Time to end this. {{lb:Remove the bell.}}")
    ]

    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "rm bell"
    ]
    hints = [
        ("{{rb:Use}} {{yb:rm bell}} {{rb:to remove the bell.}}")
    ]
    dark_theme = True

    def block_command(self, line):
        if line == "rm Rabbit":
            print((("The rabbit dodged the attack!")))
            return True
        return StepTemplateRm.block_command(self, line)

    def check_command(self, line):
        if self.get_last_user_input() == "rm Rabbit":
            self.send_hint(
                ("{{lb:The rabbit dodged the attack!}} {{rb:Remove the bell with}} {{yb:rm bell}}")
            )
            return

        return StepTemplateRm.check_command(self, line)

    def __next__(self):
        Animation("gong-being-removed").play_finite(1)
        self.send_normal_theme()
        Animation("rabbit-blinking").play_finite(1)
        return 46, 2


class Step2(StepTemplateRm):
    story = [
        ("The rabbit stops. The anger behind its eyes fades, replaced with confusion."),
        "",
        ("The Swordmaster runs into the {{bb:rabbithole}}."),
        "",
        ("Swordmaster: {{Bb:\"You did it! The rabbit is free from the cursed bell, and you saved everyone!\"}}"),
        "",
        ("{{Bb:\"Have you looked inside the}} {{bb:chest}} {{Bb:the rabbit stole? It's right here.\"}}")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "cat chest/scroll"
    ]
    hints = [
        ("{{rb:Use}} {{yb:cat chest/scroll}} {{rb:to examine the contents.}}")
    ]
    deleted_items = [
        "~/woods/thicket/rabbithole/Rabbit"
    ]

    file_list = [
        {
            "path": "~/woods/thicket/rabbithole/Swordmaster",
            "contents": get_story_file("swordmaster-without-sword")
        },
        {
            "path": "~/woods/thicket/rabbithole/Rabbit",
            "contents": get_story_file("Rabbit-cute")
        }
    ]

    def check_command(self, line):
        if line == "cat chest/torn-note":
            return False
        return StepTemplateRm.check_command(self, line)

    def __next__(self):
        return 46, 3


class Step3(StepTemplateSudo):
    story = wrap_in_box([
        ("{{gb:New Power:}} Use {{yb:sudo}} to"),
        (" {{lb:make yourself into a Super User.}}")
    ])
    story += [
        ("Try it out. Use {{yb:sudo ls}} to look around."),
        ("You will be asked for a password."),
        "",
        ("Swordmaster: {{Bb:The Rabbit couldn't guess the password.}}"),
        ("{{Bb:Can you figure it out?}}"),
        "",
        ("Tip: The password will be invisible to keep it secret. It will look like you've typed nothing, so you need to be careful.")
    ]
    commands = [
        "sudo ls",
        "sudo ls .",
        "sudo ls ./"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Try again! Use}} {{yb:sudo ls}}{{rb:. The default password is}} {{yb:kano}}"
        "{{rb:. If you've changed the password, try that here instead.}}"
    ]

    def __next__(self):
        return 46, 4


class Step4(StepTemplateSudo):
    story = [
        ("Swordmaster: {{Bb:\"Wow, you have some skills. You may not have noticed the change, but you became a "
          "Super User for an instant!}}"),
        ("{{Bb:Knowing this command gives you the power to do things when all else fails.\"}}"),
        "",
        ("{{gb:Well done, you've learnt the power of}} {{yb:sudo}}{{gb:!}}"),
        "",
        ("Swordmaster: {{Bb:\"You should turn into a Super User and}} {{lb:remove}} {{Bb:this chest so it cannot fall into enemy hands again.}}"),
        ("{{Bb:To delete the whole chest, use}} {{yb:sudo rm -r chest/}}{{Bb:. The -r flag is used for directories.\"}}")
    ]
    commands = [
        "sudo rm -r chest",
        "sudo rm -r chest/"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Use}} {{yb:sudo rm -r chest}} {{rb:to remove the chest and its contents.}}"
    ]

    def __next__(self):
        return 46, 5


class Step5(StepTemplateSudo):
    story = [
        ("Swordmaster: {{Bb:\"Well done!\"}}"),
        ("{{Bb:\"Let's go back to}} {{bb:~/town}}{{Bb:. Everyone will want to thank you!\"}}")
    ]

    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/town"
    file_list = [
        {
            "path": "~/town/Ruth",
            "contents": get_story_file("Ruth")
        },
        {
            "path": "~/town/Clara",
            "contents": get_story_file("Clara")
        },
        {
            "path": "~/town/Eleanor",
            "contents": get_story_file("Eleanor")
        }
    ]

    def block_command(self, last_user_input):
        return unblock_cd_commands(last_user_input)

    def __next__(self):
        return 46, 6


class Step6(StepTemplateSudo):
    story = [
        ("The towns people cheer as you walk into town."),
        ("{{lb:Look around.}}")
    ]
    commands = [
        "ls"
    ]
    start_dir = "~/town"
    end_dir = "~/town"

    hints = [
        ("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    file_list = [
        {
            "path": "~/town/Rabbit",
            "contents": get_story_file("Rabbit-cute")
        },
        {
            "path": "~/town/Swordmaster",
            "contents": get_story_file("swordmaster-without-sword")
        }
    ]

    deleted_items = [
        "~/woods/thicket/rabbithole/Rabbit",
        "~/woods/thicket/rabbithole/Swordmaster"
    ]

    def __next__(self):
        return 46, 7


class Step7(StepTemplateSudo):
    story = [
        ("You see your Mum, Dad and everyone else you met on your adventure. They stand around you in the street "
          "clapping and cheering."),
        ("{{lb:Talk to everyone.}}")
    ]
    start_dir = "~/town"
    end_dir = "~/town"

    hints = [
        ("")
    ]

    all_commands = {
        "cat Mum": ("Mum: {{Bb:\"You saved Folderton! You're a hero!\"}}"),
        "cat Dad": ("Dad: {{Bb:\"I'm so proud of you, " + get_username() + ".\"}}"),
        "cat Mayor": ("Mayor: {{Bb:\"Now that you're a Super User, you must always remember:\n"
                       " 1. Respect the privacy of others.\n"
                       " 2. Think before you type.\n"
                       " 3. With great power comes great responsibility.\"}}")
    }

    other_commands = {
        "cat grumpy-man": ("grumpy-man: {{Bb:\"Ruth told me about how you helped hide her and our animals. "
                            "Thank you!}}"),
        "cat Ruth": ("Ruth: {{Bb:\"If you ever come by the farm, you can have a glass of milk on us!\"}}"),
        "cat little-boy": ("little-boy: {{Bb:\"Mummy is safe!\"}}"),
        "cat young-girl": ("young-girl: {{Bb:\"We found Mummy. I'm really glad she's safe.\"}}"),
        "cat Edith": ("Edith: {{Bb:\"I'm so glad Eleanor is safe! Thank you for saving Edward and I.\"}}"),
        "cat Edward": ("Edward: {{Bb:\"Now all this is over, we can go back to our house and stop living in "
                        "hiding.\"}}"),
        "cat Eleanor": ("Eleanor: {{Bb:\"You found my parents! I knew they'd be alright.\"}}"),
        "cat dog": ("dog: {{Bb:\"Woof woof!\"}}"),
        "cat Bernard": ("Bernard: {{Bb:\"Who is that Masked Swordmaster? He looks oddly familiar.\"}}"),
        "cat Clara": (
            "Clara: {{Bb:\"Eleanor helped me feel brave, but I'm so happy you found my children}} {{bb:young-girl}} {{Bb:and}} "
            "{{bb:little-boy}}{{Bb:! Thank you " + get_username() + "!\"}}"
        ),
        "cat Swordmaster": ("Swordmaster: {{Bb:\"You've done well. You are indeed a force to be reckoned with. "
                             "Keep training and you'll become even more powerful.\"}}"),
        "cat Rabbit": ("Rabbit: {{Bb:....}}")
    }

    def check_command(self, line):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = ("\n{{gb:You look around.}}")
            self.send_hint(hint)
            return False
        elif line in self.other_commands:
            hint = "\n" + self.other_commands[line]
            self.send_hint(hint)
            return False

        # check through list of commands
        self.hints = [
            ("{{rb:Use}} {{yb:%s}} {{rb:to progress.}}") % list(self.all_commands.keys())[0]
        ]

        end_dir_validated = self.get_fake_path() == self.end_dir

        if (line in list(self.all_commands.keys())) and end_dir_validated:
            hint = "\n" + self.all_commands[line]
            self.all_commands.pop(line, None)

            if len(self.all_commands) == 0:
                hint += ("\n\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")

            self.send_hint(hint)
        else:
            self.send_stored_hint()

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def __next__(self):
        from kano_profile.badges import save_app_state_variable_with_dialog
        save_app_state_variable_with_dialog('linux-story', 'finished', 'challenge_46')
        self._is_finished = True
        self.exit()
        return -1, -1
