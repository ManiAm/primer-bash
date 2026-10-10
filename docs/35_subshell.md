# Subshell

A **subshell** is a child process created by forking the current shell. It receives a complete copy of the parent shell's environment — including non-exported variables, functions, and options — but operates independently. Changes made inside a subshell (such as variable assignments or directory changes) do not propagate back to the parent shell.

Subshells are created in the following situations:

- Commands are grouped in parentheses `()`
- A command substitution is performed `$(command)` (see [Command Substitution](29_command_substitution.md))
- Each command in a pipeline `|` (see [Pipeline](30_command_chaining.md#pipeline-))
- A background job is run `command &` (see [Background Process](32_background.md))

> **Note:** Running a script without `source` or `.` (e.g., `./script.sh` or `bash script.sh`) does **not** create a subshell. It launches a new shell instance via `fork + exec`, which only inherits exported environment variables — not the parent shell's full state. See [`source` Command](08_shell_script.md#source-command) for details.

## Shell Level

You can identify the subshell nesting depth by checking the `SHLVL` environment variable. Each time a new shell is spawned from an existing shell, `SHLVL` is incremented by 1:

```bash
echo $SHLVL   # output: 1

# Spawn a new interactive shell
bash

echo $SHLVL   # output: 2
```

When you log in to a terminal session, the initial shell level is typically `1`, representing the top-most shell.

To visualize the shell hierarchy, use the `pstree` command:

```bash
# $$ is the PID of the current shell
pstree -s $$

# Output:
# systemd───systemd───gnome-terminal-───bash───pstree

# Spawn a new interactive shell
bash

pstree -s $$

# Output:
# systemd───systemd───gnome-terminal-───bash───bash───pstree
```

## Parentheses `()` — Subshell Grouping

Enclosing commands in parentheses creates a subshell and executes the commands inside it. Because the subshell is a separate environment, any changes made within it are discarded when it exits:

```bash
var="parent"

(
    var="child"
    echo "Inside subshell: $var"
)

echo "Outside subshell: $var"

# Output:
# Inside subshell: child
# Outside subshell: parent
```

The same isolation applies to directory changes — the `cd` only takes effect inside the subshell:

```bash
(cd /tmp && pwd)
pwd

# Output:
# /tmp
# /home/user
```

> **Note:** This makes `()` useful for running commands that need a temporary environment (different directory, modified variables) without affecting the parent shell.

## Curly Braces `{}` — Current Shell Grouping

Curly braces group commands to execute in the **current** shell rather than a subshell. Changes made inside `{}` persist after the block finishes:

```bash
var="parent"

{
    var="child"
    echo "Inside braces: $var"
}

echo "Outside braces: $var"

# Output:
# Inside braces: child
# Outside braces: child
```

> **Note:** Curly braces require a space after `{`, a semicolon (or newline) before `}`, and are parsed as reserved words — not operators like `()`.

### Comparison

| Feature                  | `()` (Parentheses)         | `{}` (Curly Braces)        |
|--------------------------|----------------------------|----------------------------|
| **Execution context**    | Runs in a new subshell     | Runs in the current shell  |
| **Variable changes**     | Discarded after the block  | Persist after the block    |
| **Directory changes**    | Discarded after the block  | Persist after the block    |

## Background Subshell

By default, the parent shell waits for a subshell created with `()` to finish. Adding `&` after the closing parenthesis runs the subshell in the background, allowing the parent to continue immediately:

```bash
(
    sleep 3
    exit 42
) &

pid=$!

wait $pid
echo "Background subshell exit status: $?"  # Output: 42
```

In this example, `wait $pid` pauses the parent shell until the background subshell finishes, then captures its exit status.

You can use background subshells to run tasks in parallel:

```bash
(sleep 5; echo "Finished task 1") &
(sleep 2; echo "Finished task 2") &

wait  # Wait for all background jobs to finish
```

For more on background processes, `wait`, and job control, see [Background Process](32_background.md).

---

[← Previous: Daemon Process](34_dameon_process.md) | [Next: Process Substitution →](36_process_substition.md)
