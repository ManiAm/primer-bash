# Built-in Shell Variables

Built-in shell variables are predefined by Bash to store information about its own state and behavior. The shell creates and maintains these variables automatically — you can read their values and, in most cases, modify them to change how the shell operates.

For the complete reference, see the [Bash Variables](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html) section of the Bash manual.

## Shell Identity

| **Variable**    | **Description**                                                                    |
|-----------------|------------------------------------------------------------------------------------|
| `BASH`          | The full path to the Bash executable.                                              |
| `BASH_VERSION`  | A string describing the version of the running Bash (e.g., `5.1.16(1)-release`).   |
| `BASH_VERSINFO` | An array containing version components (major, minor, patch, etc.).                |
| `BASHPID`       | The process ID of the current Bash process.                                        |
| `SHELL`         | The path to the user's default login shell (e.g., `/bin/bash`).                    |
| `SHLVL`         | The shell nesting level (incremented each time a new Bash instance starts).        |

## Operating System and Host

| **Variable** | **Description**                                                                    |
|--------------|------------------------------------------------------------------------------------|
| `HOSTNAME`   | The name of the current host.                                                      |
| `HOSTTYPE`   | The CPU architecture (e.g., `x86_64`).                                             |
| `MACHTYPE`   | A GNU-style string describing the system (e.g., `x86_64-pc-linux-gnu`).            |
| `OSTYPE`     | The operating system name (e.g., `linux-gnu`, `darwin21`).                          |

## Directory and Navigation

| **Variable** | **Description**                                                                    |
|--------------|------------------------------------------------------------------------------------|
| `PWD`        | The current working directory.                                                     |
| `OLDPWD`     | The previous working directory (set by `cd`).                                      |
| `DIRSTACK`   | An array containing the directory stack managed by `pushd` and `popd`.             |

## User and Process

| **Variable**    | **Description**                                                                 |
|-----------------|---------------------------------------------------------------------------------|
| `UID`           | The real user ID of the current user (read-only).                               |
| `EUID`          | The effective user ID of the current user (read-only).                          |
| `GROUPS`        | An array of group IDs the current user belongs to (read-only).                  |
| `PPID`          | The process ID of the shell's parent process (read-only).                       |
| `BASH_SUBSHELL` | Incremented by one each time a subshell is entered.                             |

## Locale and Terminal

| **Variable** | **Description**                                                                    |
|--------------|------------------------------------------------------------------------------------|
| `LANG`       | The default locale setting (e.g., `en_US.UTF-8`).                                 |
| `LINES`      | The number of rows in the terminal window.                                         |
| `COLUMNS`    | The number of columns in the terminal window.                                      |

## Prompt

These variables control the shell prompt. For details and examples, see [Shell Prompt](07_shell_prompt.md).

| **Variable**     | **Description**                                                              |
|------------------|------------------------------------------------------------------------------|
| `PS1`            | The primary prompt string.                                                   |
| `PS2`            | The secondary (continuation) prompt string.                                  |
| `PS3`            | The prompt for the `select` command.                                         |
| `PS4`            | The debugging prompt displayed during `set -x` tracing.                      |
| `PROMPT_COMMAND` | A command executed just before displaying the primary prompt.                |

## History

These variables control command history. For details and examples, see [History Management](06_history.md).

| **Variable**   | **Description**                                                                          |
|----------------|------------------------------------------------------------------------------------------|
| `HISTSIZE`     | The maximum number of commands kept in memory.                                           |
| `HISTFILE`     | The path to the history file on disk (default: `~/.bash_history`).                       |
| `HISTFILESIZE` | The maximum number of lines stored in the history file.                                  |
| `HISTCONTROL`  | Rules for excluding commands from history (e.g., `ignoredups`, `ignorespace`).           |
| `HISTCMD`      | The history number of the current command.                                               |

## Input Parsing

| **Variable** | **Description**                                                                          |
|--------------|------------------------------------------------------------------------------------------|
| `IFS`        | Internal Field Separator used to split words (default: space, tab, newline).             |
| `REPLY`      | The default variable for the `read` built-in when no variable name is specified.         |

## Option Handling (`getopts`)

| **Variable** | **Description**                                                                          |
|--------------|------------------------------------------------------------------------------------------|
| `OPTARG`     | The argument value for the last option processed by `getopts`.                           |
| `OPTIND`     | The index of the next argument to be processed by `getopts`.                             |
| `OPTERR`     | Controls whether `getopts` prints error messages (`1` = enabled, `0` = disabled).        |

## Scripting and Debugging

| **Variable**   | **Description**                                                                       |
|----------------|---------------------------------------------------------------------------------------|
| `LINENO`       | The current line number in the script or function.                                    |
| `FUNCNAME`     | An array of function names in the current call stack.                                 |
| `BASH_SOURCE`  | An array of source filenames corresponding to `FUNCNAME`.                             |
| `BASH_LINENO`  | An array of line numbers corresponding to `FUNCNAME`.                                 |
| `BASH_COMMAND` | The command currently being executed or about to be executed.                          |
| `BASH_ARGC`    | An array of argument counts for each function in the call stack.                      |
| `BASH_ARGV`    | An array of all arguments in the current call stack.                                  |

## Pattern Matching

| **Variable**   | **Description**                                                                       |
|----------------|---------------------------------------------------------------------------------------|
| `BASH_REMATCH` | An array of matches from the most recent `=~` regex operation.                        |
| `GLOBIGNORE`   | A colon-separated list of patterns excluded from filename expansion.                  |

## Programmable Completion

These variables are available inside completion functions. They are rarely needed outside of custom tab-completion scripts.

| **Variable**               | **Description**                                                        |
|----------------------------|------------------------------------------------------------------------|
| `COMP_CWORD`               | Index of the word containing the cursor in `COMP_WORDS`.               |
| `COMP_LINE`                | The full text of the current command line.                              |
| `COMP_POINT`               | The cursor position (character index) in `COMP_LINE`.                  |
| `COMP_WORDS`               | An array of individual words on the current command line.              |
| `COMP_WORDBREAKS`          | Characters that separate words for completion purposes.                |
| `COMPREPLY`                | An array that completion functions populate with possible matches.     |
| `BASH_COMPLETION_VERSINFO` | An array containing the version of the completion system.              |

## Shell Options

| **Variable**      | **Description**                                                               |
|-------------------|-------------------------------------------------------------------------------|
| `BASHOPTS`        | A colon-separated list of enabled shell options (from `shopt`).               |
| `SHELLOPTS`       | A colon-separated list of enabled shell options (from `set`).                 |
| `POSIXLY_CORRECT` | When set, Bash runs in POSIX-compliant mode.                                  |

## Miscellaneous

| **Variable**   | **Description**                                                                    |
|----------------|------------------------------------------------------------------------------------|
| `_`            | The last argument of the previous command.                                         |
| `RANDOM`       | Returns a random integer between 0 and 32767 each time it is referenced.           |
| `SECONDS`      | The number of seconds since the shell was started (can be reset).                  |
| `PIPESTATUS`   | An array of exit statuses from the commands in the most recent pipeline.           |
| `MAPFILE`      | The default array for the `mapfile` (or `readarray`) built-in.                     |
| `MAILCHECK`    | Interval in seconds between mail checks (default: `60`).                           |
| `IGNOREEOF`    | Number of consecutive EOF characters required before the shell exits.              |
| `BASH_ALIASES` | An associative array of currently defined aliases.                                 |
| `BASH_CMDS`    | An associative array of hashed command paths.                                      |

## Examples

**Check the Bash version:**

```bash
echo "$BASH_VERSION"
# 5.1.16(1)-release
```

**Use `RANDOM` to generate a random number:**

```bash
echo $RANDOM
# 17243
```

**Measure script execution time with `SECONDS`:**

```bash
SECONDS=0
sleep 2
echo "Elapsed: ${SECONDS} seconds"
# Elapsed: 2 seconds
```

**Inspect the exit status of each command in a pipeline:**

```bash
true | false | true
echo "${PIPESTATUS[@]}"
# 0 1 0
```

## IFS (Internal Field Separator)

`IFS` is one of the most important built-in variables. It tells Bash which characters to use as boundaries when splitting text into separate words.

### Default value

By default, `IFS` contains three characters — space, tab, and newline — so Bash splits on any whitespace:

```bash
printf "%q" "$IFS"  # Output: $' \t\n'
```

### How Bash uses IFS

Bash consults `IFS` in two main situations:

1. **Word splitting** — When an unquoted variable is expanded, Bash splits the result into separate words at each `IFS` character.

    ```bash
    greeting="Hello World"
    for word in $greeting; do
        echo "$word"
    done
    # Hello
    # World
    ```

2. **The `read` built-in** — When `read` receives input, it splits the line into variables using `IFS` as the delimiter.

    ```bash
    echo "Alice 30" | read -r name age
    # name=Alice, age=30
    ```

### Changing IFS

You can change `IFS` to split on a different character. A common pattern is parsing comma-separated data:

```bash
IFS=','
string="Alice,Bob,Charlie"

for name in $string; do
    echo "$name"
done
# Alice
# Bob
# Charlie
```

### Setting IFS inline

To change `IFS` for a single command without affecting the rest of the script, set it inline before the command:

```bash
IFS=',' read -r col1 col2 col3 <<< "Alice,Bob,Charlie"
echo "$col1"  # Alice
echo "$col2"  # Bob
echo "$col3"  # Charlie
```

### Preserving line breaks

When reading multi-line input, set `IFS` to a newline so that each line stays intact:

```bash
IFS=$'\n'

for line in $(cat file.txt); do
    echo "$line"
done
```

### Restoring IFS

If you change `IFS` globally, save the original value first and restore it when finished to avoid unexpected side effects in the rest of the script:

```bash
OLD_IFS="$IFS"
IFS=','

# ... do work ...

IFS="$OLD_IFS"
```

> **Tip:** Prefer setting `IFS` inline (e.g., `IFS=',' read -r ...`) whenever possible. This limits the change to a single command and avoids the need to save and restore.

---

[← Previous: sudo & Variables](12_sudo_and_variables.md) | [Next: Special Variables →](14_special_variables.md)
