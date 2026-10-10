# Environment Variables

If you define a variable like `MY_VAR`, it is only a shell variable.

It exists in the current shell session and is not accessible to any child processes (subshells) spawned by the shell.

```bash
MY_VAR="hello"
echo $MY_VAR        # Outputs: hello
bash                # Start a new subshell
echo $MY_VAR        # Outputs nothing because MY_VAR is not exported
```

When you use the `export` command, the variable becomes an **environment variable**. This means it is not only available in the current shell session but is also passed to any child processes (subshells) or programs started by the shell.

```bash
MY_VAR="hello"
export MY_VAR
bash                # Start a new subshell
echo $MY_VAR        # Outputs: hello
```

In other words, the `export` command marks a variable to be inherited by child processes.

Note that changes made to an environment variable in a child process do not affect the parent shell.

You can define and export a variable in a single command:

```bash
export MY_VAR="hello"
```

To remove the export property from a previously exported variable:

```bash
export -n MY_VAR
```

The variable still exists in the current shell as a shell variable but is no longer passed to child processes.

To view all environment variables:

```bash
printenv
```

It is a common convention to use uppercase names for environment variables and lowercase names for local shell variables. However, this is just a convention and not enforced by Bash.

## Persistent Environment Variables

Temporary environment variables only exist for the duration of the terminal session in which they are defined. Persistent environment variables are automatically set each time a new session begins. They retain their values across different terminal sessions.

To make environment variables persistent, add them to one of the shell's configuration files.

> For a detailed breakdown of which configuration files are read and when, see [Shell Configuration Files](02_shell_config.md).

Which file you use depends on when you want the variable to be available:

**For a Specific User**

Add the variable definition to:

- `~/.bashrc`: Used for non-login interactive shells.
- `~/.bash_profile`: Used for login shells.

**For All Users**

Add the variable definition to:

- `/etc/environment`: Used for environment variables only, not shell functions.
    - It is not a shell script and only allows simple `KEY=VALUE` pairs (no commands or expansions).
    - It is read by PAM (Pluggable Authentication Modules) during login.
    - It sets the default environment variables for all users.

- `/etc/bash.bashrc`: Used for non-login interactive shells.

- `/etc/profile`: Used for login shells.

## Common Environment Variables

The POSIX standard defines a set of environment variables with standardized meanings. If a system provides these variables, conformant programs must interpret them consistently. POSIX does not mandate that every variable must exist in all processes, but if one is present, its behavior is well defined.

> For the full specification, see the [POSIX Environment Variables](https://pubs.opengroup.org/onlinepubs/9799919799/) documentation.

The tables below list commonly encountered environment variables, organized by category.

> Variables that are specific to Bash internals (such as `PS1`–`PS4`, `RANDOM`, `HISTSIZE`, and `PPID`) are covered in [Built-in Shell Variables](13_built_in_variables.md). Special variables like `$?`, `$$`, and `$@` are covered in [Special Variables](14_special_variables.md).

**User and Directory**

| Variable    | Description                                                    |
|-------------|----------------------------------------------------------------|
| `USER`      | The current logged-in user's name.                             |
| `LOGNAME`   | The login name of the current user (POSIX-specified).          |
| `HOME`      | The home directory of the current user.                        |
| `PWD`       | The current working directory.                                 |
| `OLDPWD`    | The previous working directory (before the last `cd` command). |
| `TMPDIR`    | The directory for storing temporary files.                     |

**Search Paths**

| Variable    | Description                                          |
|-------------|------------------------------------------------------|
| `PATH`      | Colon-separated list of directories to search for executable files. |
| `CDPATH`    | Colon-separated search path for the `cd` command.    |
| `MANPATH`   | Colon-separated search path for manual pages.        |

> For a detailed guide on `PATH`, see [PATH](11_path_env_variable.md).

**Shell and Editors**

| Variable    | Description                                          |
|-------------|------------------------------------------------------|
| `SHELL`     | Path to the current user's default login shell.      |
| `EDITOR`    | Default text editor for command-line programs.       |
| `VISUAL`    | Preferred visual (full-screen) text editor.          |

**Locale and Time Zone**

| Variable      | Description                                                      |
|---------------|------------------------------------------------------------------|
| `LANG`        | Default locale for all locale categories.                        |
| `LC_ALL`      | Overrides all individual `LC_*` settings when set.               |
| `LC_CTYPE`    | Locale for character classification and case conversion.         |
| `LC_MESSAGES` | Locale for system messages and translations.                     |
| `LC_MONETARY` | Locale for monetary formatting.                                  |
| `LC_NUMERIC`  | Locale for numeric formatting.                                   |
| `LC_TIME`     | Locale for date and time formatting.                             |
| `LC_COLLATE`  | Locale for string comparison and sorting order.                  |
| `TZ`          | Time zone setting (e.g., `America/New_York`, `UTC`).             |

**Terminal**

| Variable    | Description                                          |
|-------------|------------------------------------------------------|
| `TERM`      | The terminal type (e.g., `xterm-256color`).          |
| `LINES`     | Number of lines (rows) in the terminal window.       |
| `COLUMNS`   | Number of columns in the terminal window.            |

**Mail**

| Variable    | Description                                                    |
|-------------|----------------------------------------------------------------|
| `MAIL`      | Path to the user's incoming mailbox file.                      |
| `MAILCHECK` | Interval (in seconds) between checks for new mail.            |
| `MAILPATH`  | Colon-separated list of mail files to check for incoming mail. |

**Pager**

| Variable    | Description                                          |
|-------------|------------------------------------------------------|
| `PAGER`     | Default program for paging through long output (e.g., `less`). |

---

[← Previous: Shell Variables](09_shell_variables.md) | [Next: PATH →](11_path_env_variable.md)
