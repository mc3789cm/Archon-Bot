"""
Prefixes for all logging messages.
"""

QSTN_LOG = "[ \033[1;37mQSTN\033[0m ]"
"""Use when you’re waiting for user input."""

INFO_LOG = "[ \033[0;32mINFO\033[0m ]"
"""Use in routine information messages."""

WARN_LOG = "[ \033[0;33mWARN\033[0m ]"
"""Use when an unexpected event and/or argument is passed, but it’s not stopping the continuation of the function(s)."""

EROR_LOG = "[ \033[0;31mEROR\033[0m ]"
"""Use when a function fails and can’t continue properly. If possible, rollback changes, if any, for better redundancy. """

CRIT_LOG = "[ \033[1;31mCRIT\033[0m ]"
"""Use when an event/argument would result in the complete stoppage of Archon."""