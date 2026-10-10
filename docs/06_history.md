# History Management

Bash keeps a list of every command you enter during a session in an **in-memory history list**. When the session ends, that list is written to the `~/.bash_history` file so it persists across sessions.

## Viewing History

Display the full in-memory history with line numbers:

    $ history

Display only the last *n* commands:

    $ history 10

Search the history for a specific pattern using `grep`:

    $ history | grep ssh

## Clearing History

Clear the in-memory history for the current session:

    $ history -c

Clear the `~/.bash_history` file on disk:

    $ > ~/.bash_history

To fully reset history (both in-memory and on disk), combine both commands:

    $ history -c && > ~/.bash_history

## Writing History to Disk

By default, Bash writes the in-memory history to `~/.bash_history` when a session ends. You can also write it manually at any time.

Overwrite the history file with the current session's history:

    $ history -w

Append the current session's history to the history file without overwriting it:

    $ history -a

Appending is useful when you run multiple terminal sessions in parallel and want to preserve history from all of them.

## History Environment Variables

Several environment variables control how Bash stores and manages command history.

| **Variable**       | **Purpose**                                      | **Example Value**                    |
|--------------------|--------------------------------------------------|--------------------------------------|
| `HISTSIZE`         | Number of commands kept in memory                | `2000`                               |
| `HISTFILE`         | Path to the history file on disk                 | `/home/user/.bash_history`           |
| `HISTFILESIZE`     | Maximum number of lines in the history file      | `5000`                               |
| `HISTCONTROL`      | Rules for excluding commands from history        | `ignoreboth`                         |
| `HISTIGNORE`       | Colon-separated patterns of commands to exclude  | `ls:cd:pwd:clear`                    |
| `HISTTIMEFORMAT`   | Timestamp format prepended to each history entry | `%Y-%m-%d %H:%M:%S `                 |
| `PROMPT_COMMAND`   | Command executed before each prompt display      | `history -a; history -c; history -r` |

### `HISTCONTROL`

`HISTCONTROL` controls which commands are excluded from the history list:

- `ignoredups` — ignore a command if it is identical to the one entered immediately before it.
- `ignorespace` — ignore a command if it starts with a space character.
- `ignoreboth` — enable both `ignoredups` and `ignorespace`.

For example, to enable both rules:

    export HISTCONTROL=ignoreboth

### `PROMPT_COMMAND`

`PROMPT_COMMAND` specifies a command (or commands) that Bash executes just before displaying each prompt. It is often used to keep history synchronized across multiple open terminals:

    export PROMPT_COMMAND='history -a; history -c; history -r'

This appends the current session's new entries to the file, clears the in-memory list, and reloads it from the file — so every terminal sees a shared, up-to-date history.

> For more on `PROMPT_COMMAND` and prompt customization, see [Shell Prompt](07_shell_prompt.md).

## Navigating History with Arrow Keys

Press the **Up** arrow key to scroll backward through previous commands and the **Down** arrow key to scroll forward. Press `Enter` to execute the displayed command, or use the **Left** and **Right** arrow keys to edit it first.

This approach works well for recent commands but becomes slow when you need to find something from hundreds of entries.

## Repeating Commands with `!`

The `!` character (called *bang*) provides shortcuts for re-executing previous commands:

| **Syntax**   | **Action**                                            |
|--------------|-------------------------------------------------------|
| `!!`         | Repeat the last command                               |
| `!n`         | Run command number *n* from history                   |
| `!-n`        | Run the command *n* entries back from the current one |
| `!string`    | Run the most recent command that starts with *string* |

For example, to find and re-run a previous `grep` command:

    $ history | grep grep
      42  grep -r "TODO" src/
      87  grep error /var/log/syslog

    $ !42

Execute the last command that starts with `cd`:

    $ !cd

## Interactive Reverse Search

Reverse search lets you find a previous command by typing part of it:

1. Press `Ctrl-R` to enter reverse search mode. The prompt changes to `(reverse-i-search)`.
2. Start typing any part of the command you are looking for. Bash displays the most recent match as you type.
3. Press `Ctrl-R` again to cycle backward through older matches.
4. Once you find the command:
   - Press `Enter` to execute it immediately.
   - Press the **Right** or **Left** arrow key to place it on the command line for editing before execution.
5. Press `Ctrl-C` to cancel the search and return to a normal prompt.

---

[← Previous: Auto-Completion](05_auto_completion.md) | [Next: Shell Prompt →](07_shell_prompt.md)
