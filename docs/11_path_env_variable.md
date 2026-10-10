# PATH

The `PATH` environment variable is a colon-separated list of directories that the shell searches when you enter a command. The shell checks each directory from left to right and runs the first matching executable it finds.

```bash
echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

If the command is not found in any of the listed directories, the shell returns a "command not found" error:

```bash
mycmd
bash: mycmd: command not found
```

## Locating Commands

The `which` command shows the full path of the executable that the shell would run:

```bash
which echo
/usr/bin/echo
```

Use `which -a` to display all matching executables across every directory in `PATH`:

```bash
which -a echo
/usr/bin/echo
/bin/echo
```

The shell uses the **first match** found based on the order of directories in `PATH`.

The `type -a` command provides more detailed output, including shell builtins:

```bash
type -a echo
echo is a shell builtin
echo is /usr/bin/echo
echo is /bin/echo
```

The output shows that `echo` is both a shell builtin and an external binary. When you run `echo`, the builtin version is used by default because builtins take priority over external binaries.

## Modifying PATH

You can add directories to `PATH` so that custom scripts and programs can be run by name without specifying their full paths.

Because `PATH` is already an exported environment variable, assigning a new value updates it for the current shell and any child processes:

```bash
PATH=$PATH:/custom/path
```

This change only lasts for the current session. To make it persistent across sessions, add the assignment to a shell configuration file such as `~/.bashrc` or `~/.profile`.

> For details on which configuration file to use, see [Shell Configuration Files](02_shell_config.md). For a broader overview of exporting and persisting environment variables, see [Environment Variables](10_env_variables.md).

**Security note:** Avoid adding `.` (the current directory) to `PATH`. Doing so can lead to accidental execution of malicious scripts placed in your working directory.

## `hash` Builtin

When you run a command, the shell searches through the directories in `PATH` to locate it. To speed up repeated use, the shell caches the full path of each resolved command in an internal hash table.

To view the cached commands and how many times each has been used:

```bash
hash
hits    command
   1    /usr/bin/printenv
   4    /usr/bin/bash
   1    /usr/bin/git
  10    /usr/bin/sudo
   6    /usr/bin/docker
   2    /usr/bin/ls
```

The `hits` column shows the number of times the command has been executed since it was cached.

To clear the hash table (for example, after installing a new version of a program in a different location):

```bash
hash -r
```

---

[← Previous: Env Variables](10_env_variables.md) | [Next: sudo & Variables →](12_sudo_and_variables.md)
