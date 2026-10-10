# `sudo` and Variables

When you run a command with `sudo`, it spawns a new process with elevated (root) privileges. Because this new process starts with a clean environment, shell and environment variables from your current session are not automatically available inside it.

The `/etc/sudoers` file controls `sudo` behavior, including how environment variables are handled.

## `env_reset`

The `env_reset` option is enabled by default. It resets the environment to a minimal, secure set of variables to prevent potentially unsafe values from being passed to privileged commands.

```
Defaults env_reset
```

The following variables are included in this minimal environment:

| Variable           | Description                                                                                         |
|--------------------|-----------------------------------------------------------------------------------------------------|
| `HOME`             | The home directory of the target user (usually root).                                               |
| `LOGNAME`          | The login name of the user invoking `sudo`.                                                         |
| `PATH`             | The executable search path, often set to `/usr/sbin:/usr/bin:/sbin:/bin` for security.              |
| `PWD`              | The current working directory from which the command was executed.                                   |
| `SHELL`            | The shell defined for the invoking user.                                                            |
| `USER`             | The effective user name (target user, often root).                                                  |
| `SUDO_USER`        | The username of the user who invoked `sudo`.                                                        |
| `SUDO_UID`         | The user ID (UID) of the user who invoked `sudo`.                                                   |
| `SUDO_GID`         | The group ID (GID) of the user who invoked `sudo`.                                                  |
| `SUDO_COMMAND`     | The command being executed by `sudo`.                                                               |
| `LANG` and `LC_*`  | Locale settings to preserve language and region preferences.                                        |

## `env_keep`

The `env_keep` option specifies variables that should be preserved even when `env_reset` is enabled.

For example, the following line in `/etc/sudoers` ensures that `HOME` and `MAIL` are not reset when using `sudo`:

```
Defaults env_keep += "HOME MAIL"
```

To inspect the environment that `sudo` provides:

```bash
sudo printenv
```

## Examples

**Variable expansion before `sudo`**

In this example, the shell expands `$MYVAR` before `sudo` runs, so the value is passed as a literal string:

```bash
MYVAR="hello"
sudo echo $MYVAR  # Output: hello
```

The current shell resolves `$MYVAR` to `hello` first, so the command that `sudo` actually executes is `echo hello`.

**Variable expansion inside `sudo`**

When variable expansion needs to happen inside the `sudo`-executed process, the variable is not available:

```bash
MYVAR="hello"
sudo bash -c 'echo $MYVAR'  # Output: (empty)
```

The single quotes prevent the current shell from expanding `$MYVAR`. Inside the new shell started by `sudo`, `MYVAR` is not defined because `env_reset` discards it.

**Exporting alone is not enough**

Even after exporting the variable, it is still discarded by `env_reset`:

```bash
export MYVAR="hello"
sudo bash -c 'echo $MYVAR'  # Output: (empty)
```

The `export` command makes the variable available to child processes, but `sudo` resets the environment before starting its child process.

**Preserving the environment with `-E`**

The `-E` flag tells `sudo` to preserve the caller's environment:

```bash
export MYVAR="hello"
sudo -E bash -c 'echo $MYVAR'  # Output: hello
```

Preserving the entire environment is generally not recommended because it can expose sensitive or unsafe variables to privileged processes.

**Adding a variable to `env_keep`**

To selectively preserve a specific variable, add it to `env_keep` in the sudoers configuration:

```
Defaults env_keep += "MYVAR"
```

After this change, the variable is preserved without needing `-E`:

```bash
export MYVAR="hello"
sudo bash -c 'echo $MYVAR'  # Output: hello
```

---

[← Previous: PATH](11_path_env_variable.md) | [Next: Built-in Variables →](13_built_in_variables.md)
