# challenge_29.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os

from linux_story.story.challenges.CompanionMisc import StepTemplateNano
from linux_story.helper_functions import record_user_interaction


story_replies = {
    "echo 1": [
        {
            "user": ("\"Why is the private section in the library locked?\""),
            "clara": \
                ("Clara: {{Bb:\"It contains some dangerous information.\"" +\
                "\n\"...I'm sorry, I shouldn't say more. The head librarian " +\
                "was quite concerned that no one should go in. He was the " +\
                "only one who could lock and unlock it.\"}}")
        },
        {
            "user": ("\"How did he lock it?\""),
            "clara": \
                ("Clara: {{Bb:\"I don't know, it's a very special lock. But, I think he learnt the secrets of the "
                  "lock from a masked swordmaster living outside of town.\"}}")
        },
        {
            "user": ("\"Where would I find this masked swordmaster?\""),
            "clara": \
                ("Clara: {{Bb:\"He said the}} " +\
                "{{bb:masked swordmaster}} {{Bb:lived in the woods.\"}}" +\
                "\n{{Bb:\"I presume he meant the woods just off the}} " +\
                "{{lb:Windy Road}}{{Bb:? The one " +\
                "near the farm and that funny lonely house outside town.\"}}")
        }
    ],

    "echo 2": [
        {
            "user": ("\"Why are you hiding down here?\""),
            "clara": \
                ("Clara: {{Bb:\"I heard a bell ring, and saw the " +\
                "lead librarian disappear in front of me. I was " +\
                "so scared I ran away, and found this}} {{bb:.cellar}}" +\
                "{{Bb:.\"}}")
        },
        {
            "user": ("\"Do you have any relatives in town?\""),
            "clara": \
                ("Clara: {{Bb:\"I have a couple of children, a}} " +\
                "{{bb:little-boy}} {{Bb:and a}} " +\
                "{{bb:young-girl}}{{Bb:. I hope they are alright.\"}}")
        },
        {
            "user": ("\"Why is the library so empty?\""),
            "clara": \
                ("Clara: {{Bb:\"We should have introduced late fees a long " +\
                "time ago...\"}}")
        }
    ],

    "echo 3": [
        {
            "user": ("\"Do you know any other people in town?\""),
            "clara": \
                ("Clara: {{Bb:\"There's a man I don't trust that runs the}} " +\
                "{{bb:shed-shop}}{{Bb:. I think his name is}} {{bb:Bernard}}{{Bb:.\"}}")
        },
        {
            "user": ("\"Why don't you like Bernard?\""),
            "clara": \
                ("Clara: {{Bb:\"He makes very simple tools and charges a fortune " +\
                "for them.}}" +\
                "\n{{Bb:His father was a very clever man and spent all " +\
                "his time in the library reading up commands. He became a " +\
                "successful business man as a result.\"}}")
        },
        {
            "user": ("\"What happened to Bernard's father?\""),
            "clara": \
                ("Clara: {{Bb:\"People aren't sure, he disappeared one day. " +\
                "It was " +\
                "assumed he had died. I saw him leave the library the day " +\
                "he went missing, " +\
                "he left in a hurry. He looked absolutely terrified.\"}}")
        }
    ]
}


# Generate the story from the step number
def create_story(step):
    print_text = ""

    if step > 1:
        print_text = ("{{yb:%s}}") % story_replies["echo 1"][step - 2]["user"]

    story = [
        story_replies["echo 1"][step - 2]["clara"],
        ("\n{{yb:1: %s}}") % story_replies["echo 1"][step - 1]["user"],
        ("{{yb:2: %s}}") % story_replies["echo 2"][0]["user"],
        ("{{yb:3: %s}}") % story_replies["echo 3"][0]["user"]
    ]

    return print_text, story


# Want to eliminate the story that the user has already seen
def pop_story(user_input):
    # if the user_input is echo 1, echo 2 or echo 3
    if user_input in story_replies:
        reply = story_replies[user_input][0]
        story_replies[user_input].remove(reply)
        return reply


class StepNanoStory(StepTemplateNano):
    commands = [
        "echo 1"
    ]

    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/restaurant/.cellar"
    hints = [
        ("{{rb:Talk to Clara using}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} {{yb:echo 3}}{{rb:.}}")
    ]
    step_number = None


    def story_check_command(self, line, echo_hit):
        # If self.last_user_input equal to "echo 1" or "echo 3"
        if line in story_replies:

            if line == "echo 1":
                return True

            else:
                if echo_hit[line]:
                    echo_hit[line] = False
                    reply = pop_story(line)["clara"]
                    self.send_hint("\n\n" + reply)

                    # Record that the user got optional info
                    # Replace spaces with underscores
                    user_input = "_".join(line.split(" "))
                    state_name = "clara_%s" % user_input
                    record_user_interaction(self, state_name)
                else:
                    self.send_hint(
                        ("\n{{rb:You've already asked Clara that. Ask her something else.}}")
                    )

        else:
            return StepTemplateNano.check_command(self, line)


# ----------------------------------------------------------------------------------------


class Step1(StepNanoStory):
    story = [
        ("Clara: {{Bb:\"What? Who are you?\"}}"),

        ("\nEleanor: {{Bb:\"Hello! I'm Eleanor, and this is}} {{gb:%s}}{{Bb:.}}" +\
        " {{Bb:I recognise you! You used to work in the library!\"}}")\
        % os.environ["LOGNAME"],

        ("\nClara: {{Bb:\"...ah, Eleanor! Yes, I remember you, you used to " +\
        "come in almost everyday.\"}}"),

        # Options
        ("\n{{yb:1: \"Why is the private section in the library locked?\"}}"),
        ("{{yb:2: \"Why are you hiding down here?\"}}"),
        ("{{yb:3: \"Do you know about any other people in town?\"}}"),

        ("\nUse {{yb:echo}} to ask {{bb:Clara}} a question.")
    ]

    companion_speech = ("Eleanor: {{Bb:\"I'm not scared anymore, I like Clara.\"}}")

    def _run_at_start(self):
        self.echo_hit = {
            "echo 2": True,
            "echo 3": True
        }

    def check_command(self, last_user_input):
        return self.story_check_command(last_user_input, self.echo_hit)

    def __next__(self):
        return 29, 2


class Step2(StepNanoStory):
    companion_speech = ("Eleanor: {{Bb:\"What is so dangerous in the private-section?\"}}")

    def _run_at_start(self):
        self.echo_hit = {
            "echo 2": True,
            "echo 3": True
        }

        self.print_text = [create_story(2)[0]]
        self.story = create_story(2)[1]

    def check_command(self, last_user_input):
        return self.story_check_command(last_user_input, self.echo_hit)

    def __next__(self):
        return 29, 3


class Step3(StepNanoStory):
    companion_speech = ("Eleanor: {{Bb:\"Do we want to unlock something so dangerous?\"}}")

    def _run_at_start(self):
        self.echo_hit = {
            "echo 2": True,
            "echo 3": True
        }

        self.print_text = [create_story(3)[0]]
        self.story = create_story(3)[1]

    def check_command(self, last_user_input):
        return self.story_check_command(last_user_input, self.echo_hit)

    def __next__(self):
        return 29, 4


class Step4(StepNanoStory):
    last_step = True

    print_text = ("{{yb:\"Where would I find this masked swordmaster?\"}}"),
    story = [
        ("Clara: {{Bb:\"He said the}} " +\
        "{{bb:masked swordmaster}} {{Bb:lived in the woods.\"}}"),

        ("{{Bb:\"I presume he meant the woods just off the}} " +\
        "{{bb:Windy Road}}{{Bb:? The one " +\
        "near the farm and that funny lonely house outside town.\"}}"),

        ("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")
    ]

    companion_speech = ("Eleanor: {{Bb:\"A masked swordmaster??\"}}")

    commands = []

    def __next__(self):
        return 30, 1
