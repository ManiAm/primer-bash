# Debugging Bash Scripts

Debugging is the process of identifying and fixing errors or unexpected behavior in a script. Because Bash scripts often automate critical tasks, undetected bugs can lead to failures, data loss, or incorrect results. Bash provides several built-in tools for tracing execution, inspecting variables, and catching errors early.

## Print Debug Messages

The simplest debugging technique is adding print statements to trace variable values and execution flow. Since Bash has no built-in logging library, a common approach is to write a small helper function:

```bash
#!/bin/bash

debug_mode=true

log_debug() {
    if [ "$debug_mode" = true ]; then
        echo "DEBUG: $1"
    fi
}

name="Alice"
log_debug "Name is $name"
echo "Hello, $name"
```

Setting `debug_mode` to `false` silences all debug output without removing the calls from the script.

> **Note:** For more structured logging with severity levels, timestamps, and output formatting, see the [shell-logger](https://github.com/rcmdnk/shell-logger) framework on GitHub.

## Pausing Execution with `read`

You can pause a script at specific points using `read`, giving you time to inspect output or the environment before continuing:

```bash
#!/bin/bash

echo "Step 1 completed"
read -p "Press Enter to continue..."
echo "Step 2 completed"
```

This is useful during development to verify intermediate results before the script moves on.

## Verbose and Trace Modes

Bash offers two built-in modes that display commands as a script runs. Both help you follow what the script is doing, but they show different levels of detail.

### Verbose Mode (`set -v`)

Verbose mode prints each line of the script exactly as written in the source code — before any variable expansion or command substitution takes place. Enable it with `set -v` and disable it with `set +v`:

```bash
#!/bin/bash

set -v

echo "Hello"
VAR="World"
echo $VAR
```

Output:

```
echo "Hello"
Hello
VAR="World"
echo $VAR
World
```

Notice that `echo $VAR` is printed literally — the variable is not expanded in the output. This makes verbose mode useful for verifying that the script's source text matches what you expect.

### Trace Mode (`set -x`)

Trace mode also prints each command before executing it, but *after* all variable expansion and command substitution. This means you see the actual values the shell is working with. Enable it with `set -x` and disable it with `set +x`:

```bash
#!/bin/bash

set -x  # Enable trace mode

name="John"
echo "Hello $name"

set +x  # Disable trace mode

echo "This line is not traced."
```

Output:

```
+ name=John
+ echo 'Hello John'
Hello John
+ set +x
This line is not traced.
```

The `+` prefix on each line indicates a traced command, making it easy to distinguish commands from their output.

#### Customizing the Trace Prefix with `PS4`

The `PS4` variable controls the prefix printed before each traced command. The default is `+ `. You can change it to include useful context such as the line number:

```bash
#!/bin/bash

export PS4='+$LINENO: '
set -x

name="John"
echo "Hello $name"
```

Output:

```
+6: name=John
+7: echo 'Hello John'
Hello John
```

> **Note:** `$LINENO` is a built-in variable that holds the current line number in the script.

### Verbose vs Trace — Comparison

Running the same script with each mode highlights the difference:

**Verbose (`set -v`)** — shows raw source:

```
echo $VAR
World
```

**Trace (`set -x`)** — shows expanded values:

```
+ echo World
World
```

| Feature              | `-v` (Verbose)                              | `-x` (Trace)                                          |
|----------------------|---------------------------------------------|--------------------------------------------------------|
| **What it prints**   | Commands exactly as written in the script.  | Commands with variables and substitutions expanded.    |
| **When it prints**   | Before parsing and expansion.               | After expansion, before execution.                     |
| **Prefix**           | None.                                       | `+` (customizable via `PS4`).                          |
| **Best for**         | Inspecting script syntax and flow.          | Debugging actual values and execution.                 |

> **Tip:** You can enable both modes at the same time (`set -xv`) to see the raw source *and* the expanded commands side by side.

## Strict Mode

Strict mode makes scripts fail fast on errors instead of silently continuing. It combines three options:

| Option           | Flag | Effect                                                             |
|------------------|------|--------------------------------------------------------------------|
| `set -e`         | `e`  | Exit immediately if any command returns a non-zero status.         |
| `set -u`         | `u`  | Treat references to unset variables as errors.                     |
| `set -o pipefail`| —    | A pipeline fails if *any* command in it fails (not just the last). |

Each option can be enabled individually using its long or short form:

```bash
#!/bin/bash
set -o errexit       # exit on any command failure       (short: set -e)
set -o nounset       # error on undefined variables      (short: set -u)
set -o pipefail      # catch failures inside pipelines

echo "Name: $USER"
ls /nonexistent        # script exits here due to 'set -e'
echo "This line never runs."
```

These three options are typically combined into a single line at the top of a script:

```bash
set -euo pipefail      # same as: set -o errexit -o nounset -o pipefail
```

> **Note:** For the full list of `set` and `shopt` options, see [Shell Options](39_shell_options.md).

## Debugging with `trap`

The `trap` command can run code automatically when an error occurs. Combining `trap ... ERR` with `$LINENO` pinpoints exactly where a failure happened:

```bash
#!/bin/bash

trap 'echo "Error at line $LINENO"; exit 1' ERR

echo "Running..."
false                          # Non-zero exit triggers the ERR trap
echo "This line never runs."
```

> **Note:** For a full introduction to `trap`, including cleanup on exit, signal handling, and resetting traps, see [Trap](38_trap.md).

## Putting It All Together

Here is a script template that combines the most useful debugging techniques into a robust starting point:

```bash
#!/bin/bash

# Trace mode — show expanded commands with line numbers
export PS4='+$LINENO: '
set -x

# Strict mode — fail fast on errors
set -euo pipefail

# Error trap — report where failures occur
trap 'echo "Error at line $LINENO"; exit 1' ERR

# --- Script logic below ---

echo "Running..."
false                          # Triggers the ERR trap
echo "This line never runs."
```

## Bash Debug Extension for VS Code

The [Bash Debug](https://marketplace.visualstudio.com/items?itemName=rogalmic.bash-debug) extension for Visual Studio Code provides an interactive debugging environment for Bash scripts. Unlike the command-line tools described above, it offers:

- **Breakpoints** — pause execution at specific lines.
- **Step-through execution** — advance one line at a time.
- **Variable inspection** — view and watch variable values in real time.
- **Call stacks** — see the chain of function calls.

This visual approach is especially helpful for larger or more complex scripts, where tracing output in the terminal becomes difficult to follow.

---

[← Previous: Process Options](42_process_options.md)
