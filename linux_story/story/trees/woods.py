
from cave import cave
from clearing import clearing
from linux_story.common import get_story_file


thicket = {
    "name": "thicket",
    "challenges": [
        {
            "challenge": 1,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 40,
            "step": 1
        }
    ],
    "children": [
        {
            "name": "Rabbit",
            "contents": get_story_file("Rabbit"),
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 40,
                    "step": 1
                },
                {
                    "challenge": 43,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "rabbithole",
            "type": "directory",
            "challenges": [
                {
                    "challenge": 40,
                    "step": 1,
                },
                {
                    "challenge": 41,
                    "step": 1,
                    "permissions": 0000
                }
            ]
        },
        {
            "name": "note",
            "contents": get_story_file("note_rabbithole"),
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 41,
                    "step": 1
                },
                {
                    "challenge": 43,
                    "step": 1,
                    "exists": False
                }
            ]
        }
    ]
}


woods = {
    "name": "woods",
    "challenges": [
        {
            "challenge": 1,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 32,
            "step": 1
        }
    ],
    "children": [
        clearing,
        cave,
        thicket,
        {
            "contents": get_story_file("note_woods"),
            "name": "note",
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 41,
                    "step": 2
                }
            ]
        },
    ]
}