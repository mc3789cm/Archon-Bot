"""
Logging prefixes for console output.

Use these constants at the start of each local print statement.

- QSTN_LOG -> Waiting for user input
- INFO_LOG -> Routine information
- WARN_LOG -> Unexpected, but non-breaking events
- EROR_LOG -> Error that stops a function
- CRIT_LOG -> Critical error that stops the whole program

Each prefix includes ANSI color codes for quick visual recognition.
"""

QSTN_LOG = "[ \033[1;37mQSTN\033[0m ]"
INFO_LOG = "[ \033[0;32mINFO\033[0m ]"
WARN_LOG = "[ \033[0;33mWARN\033[0m ]"
EROR_LOG = "[ \033[0;31mEROR\033[0m ]"
CRIT_LOG = "[ \033[1;31mCRIT\033[0m ]"