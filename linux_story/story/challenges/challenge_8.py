# challenge_8.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.story.terminals.terminal_cd import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):

    story = [
        ("{{pb:Ding. Dong.}}\n"),
        ("It sounds like the bell you heard before.\n"),
        ("Use {{yb:ls}} to {{lb:look around}} again.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = [("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")]
    deleted_items = ["~/town/grumpy-man"]

    def __next__(self):
        return 8, 2


class Step2(StepTemplateCd):

    story = [
        ("{{wb:Little-boy:}} {{Bb:\"Oh no! That grumpy-man with the funny legs has gone!}} {{Bb:Did you hear the bell just before he vanished??\"}}"),
        ("{{wb:Young-girl:}} {{Bb:\"I'm scared...\"}}"),
        ("\n{{pb:Ding. Dong.}}\n"),
        ("{{wb:Young-girl:}} {{Bb:\"Oh! I heard it go again!\"}}"),
        ("\nTake a {{lb:look around}} you to check.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = [("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")]
    deleted_items = ["~/town/little-boy"]

    def __next__(self):
        return 8, 3


class Step3(StepTemplateCd):

    story = [
        ("{{wb:Young-girl:}} {{Bb:\"Wait, there was a}} {{bb:little-boy}} {{Bb:here...right?\""),
        ("Every time that bell goes, someone disappears!}}"),
        ("{{wb:Mayor:}} {{Bb:\"Maybe they just decided to go home...?\"}}"),
        ("\n{{pb:Ding. Dong.}}\n"),
        ("{{lb:Look around.}}")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = [("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")]
    deleted_items = ["~/town/young-girl"]

    def __next__(self):
        return 8, 4


class Step4(StepTemplateCd):

    story = [
        ("You are alone with the {{bb:Mayor}}.\n"),
        ("{{lb:Listen}} to what the {{bb:Mayor}} has to say.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat Mayor"
    hints = [("{{rb:Use}} {{yb:cat Mayor}} {{rb:to talk to the Mayor.}}")]

    def __next__(self):
        return 8, 5


class Step5(StepTemplateCd):

    story = [
        ("{{wb:Mayor:}} {{Bb:\"Everyone...has disappeared??\"\n"),
        ("\"....I should head home now...\"}}"),
        ("\n{{pb:Ding. Dong.}}\n")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = [("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")]
    deleted_items = ["~/town/Mayor"]
    file_list = [
        {
            "path": "~/town/note",
            "contents": get_story_file("note_town"),
            "type": "file"
        }
    ]

    def __next__(self):
        return 8, 6


class Step6(StepTemplateCd):
    story = [
        ("Everyone has gone."),
        ("Wait - there's a {{bb:note}} on the floor.\n"),
        ("Use {{yb:cat}} to read the {{bb:note}}.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat note"
    hints = [("{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}")]

    def __next__(self):
        return 9, 1
