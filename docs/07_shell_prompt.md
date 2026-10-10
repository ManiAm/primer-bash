# Shell Prompt

The shell prompt is the text displayed in the terminal when Bash is ready to accept a new command. A typical prompt looks like this:

    user@hostname:~$

It usually includes contextual information such as the current username, hostname, and working directory. You can customize the prompt to display additional details, change colors, or include dynamic information like the current Git branch.

## Why Customize the Prompt

- **Productivity** — display useful context (current directory, Git branch, exit status) so you run fewer extra commands.
- **Clarity** — distinguish between different users, servers, or shell sessions at a glance, which is especially helpful when working over SSH.
- **Aesthetics** — add colors and symbols to make the terminal easier to scan.

## Prompt Variables

Bash uses a set of special **PS** (**P**rompt **S**tring) variables to control the prompt:

| **Variable** | **Purpose**                                                    | **Default**  |
|--------------|----------------------------------------------------------------|--------------|
| `PS0`        | Displayed after you enter a command, before it executes        | *(empty)*    |
| `PS1`        | Primary prompt, shown when the shell is ready for input        | `\u@\h:\w\$` |
| `PS2`        | Continuation prompt, shown when a command spans multiple lines | `> `         |
| `PS3`        | Prompt used by the `select` built-in                           | `#? `        |
| `PS4`        | Debugging prompt, shown during execution tracing (`set -x`)    | `+ `         |

### `PS1` — The Primary Prompt

`PS1` is the variable you will customize most often. Its default value on many systems is `\u@\h:\w\$ `, which produces a prompt like `user@hostname:~$ `.

To change the prompt for the current session:

    $ PS1='[\u@\h \W]\$ '
    [user@hostname ~]$

To make the change permanent, add the assignment to your `~/.bashrc` file:

    echo "PS1='[\u@\h \W]\$ '" >> ~/.bashrc

### `PS2` — The Continuation Prompt

When a command spans multiple lines, Bash displays `PS2` instead of `PS1`. The default is `> `:

    $ echo "hello
    > world"
    hello
    world

### `PS0` — The Pre-Execution Prompt

`PS0` is displayed after you press `Enter` but before the command runs. It is empty by default and rarely used, but it can be helpful for logging or timing:

    $ export PS0='[Executing: \D{%T}]\n'
    $ ls
    [Executing: 14:35:12]
    file1.txt  file2.txt

### `PS3` and `PS4`

`PS3` is the prompt shown by the `select` built-in when it asks the user to pick an item. `PS4` is the prefix printed before each traced command when debugging with `set -x`.

## Escape Sequences

Prompt variables support special escape sequences that insert dynamic information. Each sequence is prefixed with a backslash (`\`).

### User and Host

| **Sequence** | **Description**                          | **Example Output**   |
|--------------|------------------------------------------|----------------------|
| `\u`         | Username of the current user             | `user`               |
| `\h`         | Hostname up to the first `.`             | `myhost`             |
| `\H`         | Full hostname                            | `myhost.domain.com`  |

### Directory

| **Sequence** | **Description**                                       | **Example Output**  |
|--------------|-------------------------------------------------------|---------------------|
| `\w`         | Current working directory (full path, `~` for home)   | `~/projects`        |
| `\W`         | Basename of the current working directory             | `projects`          |

### Date and Time

| **Sequence** | **Description**                         | **Example Output**  |
|--------------|-----------------------------------------|---------------------|
| `\d`         | Date in "Weekday Month Day" format      | `Tue Sep 26`        |
| `\t`         | Time in 24-hour `HH:MM:SS` format       | `14:35:12`          |
| `\T`         | Time in 12-hour `HH:MM:SS` format       | `02:35:12`          |
| `\@`         | Time in 12-hour AM/PM format            | `02:35 PM`          |
| `\A`         | Time in 24-hour `HH:MM` format          | `14:35`             |

### Shell and Terminal

| **Sequence** | **Description**                          | **Example Output**     |
|--------------|------------------------------------------|------------------------|
| `\s`         | Name of the shell                        | `bash`                 |
| `\v`         | Shell version (major.minor)              | `5.1`                  |
| `\V`         | Shell version with patch level           | `5.1.16(1)-release`    |
| `\j`         | Number of jobs managed by the shell      | `2`                    |
| `\l`         | Terminal device name                     | `tty1`                 |

### History and Command Numbers

| **Sequence** | **Description**                          | **Example Output**  |
|--------------|------------------------------------------|---------------------|
| `\!`         | History number of the current command    | `123`               |
| `\#`         | Command number in the current session    | `45`                |
| `\$`         | `$` for regular users, `#` for root      | `$`                 |

### Special Characters

| **Sequence** | **Description**                                           |
|--------------|-----------------------------------------------------------|
| `\n`         | Newline                                                   |
| `\r`         | Carriage return                                           |
| `\\`         | Literal backslash                                         |
| `\[`         | Begin a non-printing sequence (used with color codes)     |
| `\]`         | End a non-printing sequence                               |

The `\[` and `\]` sequences are required when embedding ANSI color codes in the prompt. They tell Bash that the enclosed characters are non-printing, so it can calculate the prompt length correctly and avoid display glitches.

## Adding Colors

ANSI escape codes let you add color to the prompt. Wrap each color code in `\[` and `\]` so Bash handles line wrapping correctly:

    PS1='\[\033[32m\]\u@\h\[\033[0m\]:\[\033[34m\]\w\[\033[0m\]\$ '

This displays the username and hostname in green, the working directory in blue, and resets to the default color after each segment.

Common color codes:

| **Code**   | **Color** |
|------------|-----------|
| `\033[30m` | Black     |
| `\033[31m` | Red       |
| `\033[32m` | Green     |
| `\033[33m` | Yellow    |
| `\033[34m` | Blue      |
| `\033[35m` | Magenta   |
| `\033[36m` | Cyan      |
| `\033[37m` | White     |
| `\033[0m`  | Reset     |

## `PROMPT_COMMAND`

The `PROMPT_COMMAND` variable specifies a command that Bash executes just before displaying the prompt. It runs every time a new prompt is about to appear, making it useful for dynamic updates.

For example, to display the current date and time before each prompt:

    $ export PROMPT_COMMAND='echo "[$(date +%T)]"'

Common uses include updating terminal titles, logging commands, and synchronizing history across sessions.

> For details on using `PROMPT_COMMAND` to synchronize history across terminals, see [History Management](06_history.md).

---

[← Previous: History](06_history.md) | [Next: Shell Script →](08_shell_script.md)
