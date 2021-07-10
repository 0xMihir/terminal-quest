# challenge_18.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os

from linux_story.StepTemplate import StepTemplate
from linux_story.story.terminals.terminal_echo import TerminalEcho


class StepTemplateEcho(StepTemplate):
    TerminalClass = TerminalEcho


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateEcho):
    username = os.environ['LOGNAME']
    story = [
        ("Ruth: {{Bb:\"You startled me!\""),
        ("\"Do I know you? You look familiar...\""),
        ("\"Wait, you're}} {{bb:Mum}}{{Bb:'s kid, aren't you!\""),
        ("\"...Yes? Do you have a tongue?\""),
        ("\"Is your name not}} {{yb:%s}}{{Bb:?\"}}") % username,
        ("\n{{gb:Reply with}} {{yb:echo yes}} {{gb:or}} {{yb:echo no}}{{gb:.}}")
    ]

    # Story has been moved to
    hints = [
        ("{{rb:Use}} {{yb:echo}} {{rb:to reply to her question.}}"),
        ("{{rb:Reply with yes by using}} {{yb:echo yes}}{{rb:.}}")
    ]

    commands = [
        "echo yes",
        "echo Yes",
        "echo YES"
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    def check_command(self, line):

        if line == "echo no" or line == "echo No" or line == "echo NO":
            hint = (
                ("Ruth: {{Bb:\"Oh don't be ridiculous, you look just like her.\"}}")
            )
            self.send_hint(hint)

        return StepTemplateEcho.check_command(self, line)

    def __next__(self):
        return 19, 2


class Step2(StepTemplateEcho):
    print_text = [("{{yb:\"Yes\"}}")]

    story = [
        ("Ruth: {{Bb:\"Ah, I knew it!\"}}"),
        ("{{Bb:\"So you live in that little house outside town?\"}}"),
        # TODO: see if this can appear as a block
        # TODO: change the colour of this.
        ("{{yb:1: \"Yes\"}}"),
        ("{{yb:2: \"No\"}}"),
        ("{{yb:3: \"I don't know\"}}"),
        ("\n{{gb:Use}} {{yb:echo 1}}{{gb:,}} {{yb:echo 2}} {{gb:or}} {{yb:echo 3}} {{gb:to reply with either option 1, 2 or 3.}}\n")
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = ["echo 1", "echo 2", "echo 3"]
    hints = [
        ("{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} {{yb:echo 3}} {{rb:to reply to Ruth.}}")
    ]

    def check_command(self, line):
        replies = {
            "echo yes": "1",
            "echo no": "2",
            "echo \"i don't know\"": "3",
            "echo i don't know": "3"
        }

        if line.lower() in replies:
            hint = [
                ("\n{{rb:If you want to reply with \"%s\", use}} {{yb:echo %s}}") % (line, replies[line.lower()])
            ]
            self.send_hint(hint)
        else:
            return StepTemplateEcho.check_command(self, line)

    def __next__(self):
        Step3.prev_command = self._last_user_input
        return 19, 3


class Step3(StepTemplateEcho):
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        ("Ruth: {{Bb:\"Excuse me? What did you say? You know to use the}} {{lb:echo}} {{Bb:command, yes?\"}}"),
        ("{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} {{yb:echo 3}} {{rb:to reply.}}")
    ]

    def _run_at_start(self):
        if self.prev_command == "echo 1":  # yes
            self.print_text = [("{{yb:\"Yes\"}}")]
            self.story = [("Ruth: {{Bb:\"I thought so!\"}}")]
        elif self.prev_command == "echo 2":  # no
            self.print_text = [("{{yb:\"No\"}}")]
            self.story = [("Ruth: {{Bb:\"Stop lying, I know you do.\"}}")]
        elif self.prev_command == "echo 3":  # I don't know
            self.print_text = [("{{yb:\"I don't know\"}}")]
            self.story = [("Ruth: {{Bb:\"You don't know? That's worrying...\"}}")]

        self.story = self.story + [
            ("\n{{Bb:\"Did you walk all the way from town? Did you see my husband there?"),
            ("He's a pretty}} {{bb:grumpy-man}}{{Bb:, he was travelling to town because of that big meeting with the"
              " Mayor.\"}}"),
            ("\n{{yb:1: \"I'm sorry, he disappeared in front of me.\"}}"),
            ("{{yb:2: \"I didn't see your husband, but people have been disappearing in town.\"}}"),
            ("{{yb:3: \"I don't know anything.\"}}"),
            ("\nRespond with one of the following options using the {{yb:echo}} command and option number.\n")
        ]

    def check_command(self, line):
        if line == "echo 1":
            return True
        elif line == "echo 2":
            hint = (("Ruth: {{Bb:\"I feel like you're hiding something from me...\"}}"))
            self.send_hint(hint)
            return False
        elif line == "echo 3":
            hint = (("Ruth: {{Bb:\"Really? Are you sure you didn't see a}} {{lb:grumpy-man}}{{Bb: in town?\"}}"))
            self.send_hint(hint)
            return False

        else:
            self.send_stored_hint()
            return False

    def __next__(self):
        return 19, 4


class Step4(StepTemplateEcho):
    print_text = [
        ("{{yb:\"I'm sorry, he disappeared in front of me.\"}}")
    ]
    story = [
        ("Ruth: {{Bb:\"He disappeared in front of you?? Oh no! They've been saying on the radio that people have "
          "been going missing...what should I do?\"}}"),
        ("\n{{yb:1: \"Some people survived by going into hiding.\"}}"),
        ("{{yb:2: \"I think you should go and look for your husband\"}}\n")
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    commands = [
        "echo 1",
        "echo 2"
    ]

    hints = [
        ("Ruth: {{Bb:What did you say? I didn't catch that.}}"),
        ("{{rb:Use}} {{yb:echo 1}} {{rb:or}} {{yb:echo 2}} {{rb:to reply.}}")
    ]

    def check_command(self, line):
        if line == "echo 1":
            return True
        elif line== "echo 2":
            response = (
                ("Ruth: {{Bb:\"I would, but I'm scared of going missing myself.\"\n\"He might come back, so I should "
                  "stay here in case he does. Can you think of anything else?\"}}")
            )
            self.send_hint(response)
        else:
            self.send_stored_hint()

    def __next__(self):
        return 20, 1
