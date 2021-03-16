# Bot Commands
COMMANDS = {
    "APOD": {"command": "!apod", "description": "Get NASA's Astronomy Picture of the Day"},
    "COMMANDS": {"command": "!commands", "description": "List all commands for naxxatrabot"},
    "TRIVIA": {"command": "!trivia",
               "description": """Fetch a trivia based on numbers, date, year. Try the following:
                   !trivia random
                   !trivia today
                   !trivia 42
                   !trivia year_2021
                   !trivia 03/14
                """
                }
}

# DB Tables
TABLES = {
    "APOD": "apod"
}

