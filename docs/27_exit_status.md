# Exit Status

Every command in Bash produces an **exit status** (also called an **exit code**) when it finishes. This is a small integer between 0 and 255 that tells the shell whether the command succeeded or failed.

- **0** — Success. The command completed without errors.
- **Non-zero (1–255)** — Failure. The specific value often hints at what went wrong.

The exit status is how scripts make decisions. Constructs like `if`, `&&`, and `||` all rely on it.

## Checking the Exit Status

The special variable `$?` holds the exit status of the most recently executed command:

```bash
ls /tmp
echo $?    # 0 — ls succeeded
```

```bash
ls /nonexistent_path
echo $?    # 2 — ls failed (no such file or directory)
```

`$?` is updated after **every** command — including the `[` test command used inside `if` statements. This means you must read it immediately after the command you care about.

Consider this example:

```bash
ls /nonexistent_path          # Exit code is 2

if [ $? -eq 127 ]; then      # ✔ $? is 2 (from ls) — test fails, 2 ≠ 127
    echo "Command not found"
elif [ $? -eq 2 ]; then      # ✘ $? is now 1 (from the previous [ test), not 2 from ls!
    echo "Misuse error"
fi
```

The first `[ $? -eq 127 ]` correctly reads the `ls` exit code (`2`), but the comparison fails. Now `$?` holds the exit code of the `[` command itself (`1` for false) — the original value from `ls` is lost. The second `elif` never matches, even though the real exit code was `2`.

To safely check `$?` more than once, save it to a variable immediately:

```bash
ls /nonexistent_path
exit_code=$?

if [ $exit_code -eq 2 ]; then
    echo "Misuse error"
elif [ $exit_code -eq 1 ]; then
    echo "General error"
else
    echo "Something else: $exit_code"
fi
```

> **Rule of thumb:** If you need `$?` in more than one place, always capture it in a variable right after the command.

## Common Exit Codes

Exit codes can vary between applications, but the following values have well-established meanings in Bash and Unix systems.

### General Exit Codes

| Exit Code | Meaning                   | Description                                                                                |
|-----------|---------------------------|--------------------------------------------------------------------------------------------|
| **0**     | Success                   | The command completed successfully.                                                        |
| **1**     | General Error             | Catch-all for unspecified errors.                                                          |
| **2**     | Misuse of Shell Built-ins | Syntax or usage error in a shell command (e.g., invalid flags or missing arguments).       |
| **124**   | Command Timed Out         | The command exceeded the time limit set by the `timeout` utility.                          |
| **126**   | Command Cannot Execute    | The file exists but cannot be executed (e.g., missing execute permission).                 |
| **127**   | Command Not Found         | The command does not exist or is not in `$PATH`.                                           |
| **128**   | Invalid Exit Argument     | An invalid argument was passed to the `exit` built-in.                                     |
| **255**   | Exit Code Out of Range    | The exit code fell outside the 0–255 range. Many shells treat this as an error.            |

### Signal-Based Exit Codes

When a process is terminated by a signal, the shell reports its exit code as:

```
Exit Code = 128 + Signal Number
```

This lets you determine which signal killed the process.

| Exit Code | Signal    | Common Cause                          |
|-----------|-----------|---------------------------------------|
| **129**   | SIGHUP    | Terminal closed or connection lost    |
| **130**   | SIGINT    | User pressed Ctrl+C                   |
| **131**   | SIGQUIT   | User pressed Ctrl+\                   |
| **132**   | SIGILL    | Illegal CPU instruction               |
| **133**   | SIGTRAP   | Breakpoint or trace trap              |
| **134**   | SIGABRT   | Process called `abort()`              |
| **135**   | SIGBUS    | Bus error (bad memory access)         |
| **136**   | SIGFPE    | Floating-point exception (e.g., ÷ 0)  |
| **137**   | SIGKILL   | Forcibly killed (`kill -9`)           |
| **139**   | SIGSEGV   | Segmentation fault                    |
| **141**   | SIGPIPE   | Wrote to a pipe with no reader        |
| **143**   | SIGTERM   | Graceful termination request          |

> For more on signals and how to handle them, see [SIGHUP](33_background_sighup.md) and [`trap`](38_trap.md).

## Examples

### Exit Code 1 — General Error

```bash
du --invalid-option
echo $?    # 1
```

### Exit Code 2 — Misuse of Shell Built-ins

```bash
if then
# bash: syntax error near unexpected token `then'
echo $?    # 2
```

### Exit Code 124 — Command Timed Out

```bash
timeout 3s sleep 5
echo $?    # 124 — sleep was killed after 3 seconds
```

### Exit Code 126 — Cannot Execute

```bash
mkdir test_dir
./test_dir
# bash: ./test_dir: Is a directory
echo $?    # 126
```

### Exit Code 127 — Command Not Found

```bash
nonexistent_command
# bash: nonexistent_command: command not found
echo $?    # 127
```

### Exit Code 130 — Interrupted by Ctrl+C

```bash
sleep 60
# (press Ctrl+C)
echo $?    # 130
```

## Capturing the Exit Status in Other Languages

### Python

Use the `subprocess` module to run commands and inspect their exit status:

```python
import subprocess

result = subprocess.run(['ls', '/some/path'])
print(result.returncode)    # 0 if successful, non-zero on failure
```

### C

Use the `wait()` or `waitpid()` system calls to capture a child process's exit status. These functions are covered in process-management references for C.

---

[← Previous: Alias](26_alias.md) | [Next: Command Execution →](28_command_execution.md)
