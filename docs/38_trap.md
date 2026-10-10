# Trap

The `trap` built-in command lets a script intercept signals and other events, and run specific commands in response. This is commonly used to clean up temporary files, restore settings, or log errors before a script exits — whether it ends normally or is interrupted.

## Syntax

```bash
trap 'commands' SIGNAL [SIGNAL ...]
```

- `commands` — one or more commands to execute when the signal is received.
- `SIGNAL` — one or more signal names or numbers to catch.

You can specify signals by name (e.g., `SIGINT`) or by number (e.g., `2`). The `SIG` prefix is optional — `INT` and `SIGINT` are equivalent.

## Common Signals

| Signal    | Number | Trigger                                                     |
|-----------|--------|-------------------------------------------------------------|
| `SIGINT`  | 2      | The user presses Ctrl+C.                                    |
| `SIGTERM` | 15     | A termination request (e.g., from `kill`).                  |
| `SIGHUP`  | 1      | The controlling terminal is closed.                         |
| `EXIT`    | N/A    | The script exits (normally or abnormally). Bash-specific.   |
| `ERR`     | N/A    | A command exits with a non-zero status. Bash-specific.      |
| `DEBUG`   | N/A    | Before every simple command is executed. Bash-specific.     |

> **Note:** `EXIT`, `ERR`, and `DEBUG` are pseudo-signals — they are not real POSIX signals but special event hooks provided by Bash.

## Cleanup on Exit

A common use of `trap` is to register a cleanup function that runs when the script exits, regardless of how it ends. Trapping `EXIT` ensures cleanup happens even if the script is interrupted:

```bash
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/my_temp_file
}

trap cleanup SIGINT SIGTERM EXIT

touch /tmp/my_temp_file

echo "Processing... Press Ctrl+C to exit."
sleep 100
```

In this example, the `cleanup` function is called whether the script finishes the `sleep`, the user presses Ctrl+C (`SIGINT`), or the process receives a `SIGTERM`. Since `EXIT` is also trapped, cleanup runs on normal completion too.

> **Note:** When `EXIT` is trapped alongside other signals, the `EXIT` trap still fires after the signal-specific trap. There is no need to call `exit` inside a cleanup function that is already attached to `EXIT`.

## Restoring State

Another practical use is saving and restoring external state — such as terminal settings — so the script leaves the environment unchanged:

```bash
stty -g > /tmp/term_settings

restore_terminal() {
    echo "Restoring terminal settings..."
    stty $(cat /tmp/term_settings)
    rm -f /tmp/term_settings
}

trap restore_terminal EXIT

stty -echo

echo "Enter password: "
read password

echo "Processing..."
sleep 5
```

Here, the current terminal settings are saved before `stty -echo` disables input echoing. The `EXIT` trap guarantees the original settings are restored when the script ends.

## Error Trapping

`trap 'commands' ERR` executes the specified commands whenever any command exits with a non-zero status. The special variable `$LINENO` reports the line number where the error occurred:

```bash
#!/bin/bash

trap 'echo "Error occurred at line $LINENO"; exit 1' ERR

echo "Running..."
false
echo "This line won't be executed."
```

Since `false` always returns a non-zero exit status, the `ERR` trap fires immediately, printing the line number and exiting the script.

> **Note:** For more debugging techniques including `set -x`, `set -e`, and `trap DEBUG`, see [Debugging Bash Scripts](43_debugging.md).

## Ignoring and Resetting Traps

You can ignore a signal by trapping it with an empty string, or reset it to the default behavior with a dash (`-`):

```bash
trap '' SIGINT      # Ignore Ctrl+C — the script cannot be interrupted
echo "Try pressing Ctrl+C..."
sleep 5

trap - SIGINT       # Restore default Ctrl+C behavior
echo "Ctrl+C works normally again."
sleep 5
```

## Listing Active Traps

Running `trap` with no arguments prints all currently set traps:

```bash
trap 'echo bye' EXIT
trap

# Output:
# trap -- 'echo bye' EXIT
```

This is useful for debugging or verifying which traps are active in the current shell.

---

[← Previous: Regex](37_reg_exp.md) | [Next: Shell Options →](39_shell_options.md)
