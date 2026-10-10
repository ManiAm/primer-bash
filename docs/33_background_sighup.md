# SIGHUP and Process Detachment

`SIGHUP` (Signal Hang Up) is a signal sent to a process when its controlling terminal is closed.

The name comes from the early days of Unix, when physical terminals were connected to mainframes via serial lines. When a user disconnected — by logging out or losing the connection — the operating system detected the "hang up" and sent `SIGHUP` to all processes associated with that terminal.

## The Problem: Background Processes and SIGHUP

A background process is still tied to the terminal session that started it. When you close the terminal, the shell sends `SIGHUP` to all its child processes — both foreground and background. For most processes, receiving `SIGHUP` causes them to terminate.

> **Note:** Some long-running processes (such as servers) interpret `SIGHUP` as a signal to reload their configuration files rather than terminate.

**Demonstration:**

Start a background process in the first terminal:

```bash
sleep 30 &
echo $!
```

In a second terminal, verify that the process is running:

```bash
ps -p <PID>
```

Close the first terminal, then check again from the second terminal:

```bash
ps -p <PID>
```

The process is gone — it was terminated by `SIGHUP`.

## Solutions: Detaching from the Terminal

Three tools let you keep a process running after the terminal closes: `nohup`, `disown`, and `setsid`. Each works differently.

### `nohup` Command

The `nohup` (no hang-up) command makes a process immune to `SIGHUP`, ensuring it continues running even after the terminal is closed:

```bash
nohup myscript.sh &
```

By default, `nohup` redirects stdout and stderr to a file called `nohup.out`. You can override this with explicit redirection:

```bash
# Redirect stdout and stderr to separate files
nohup myscript.sh 1> output.log 2> error.log &

# Redirect both to the same file
nohup myscript.sh 1> combined.log 2>&1 &
```

**Example:**

Start a background process with `nohup` in the first terminal:

```bash
nohup sleep 30 &
echo $!
```

In a second terminal, verify that the process is running:

```bash
ps -p <PID>

# Sample output:
#     PID TTY          TIME   CMD
#   18358 pts/7    00:00:00  sleep
```

Close the first terminal. In the second terminal, verify that the process is **still running**:

```bash
ps -p <PID>

# Sample output:
#     PID TTY          TIME   CMD
#   18358 ?        00:00:00  sleep
```

Notice that the `TTY` column now shows `?`, meaning the process is no longer associated with any terminal.

> **Note:** Although `nohup` protects a process from `SIGHUP`, the process still appears in the shell's job table:
>
> ```bash
> nohup sleep 30 &
> jobs
> # [1]+  Running                 nohup sleep 30 &
> ```

### `disown` Command

The `disown` command removes a background process from the shell's job table. This prevents the shell from sending `SIGHUP` to the process when the shell exits.

The process must already be running in the background (started with `&`):

```bash
sleep 30 &
disown

jobs
# <empty>
```

> **Note:** `disown` does not manage output redirection. You must redirect output explicitly when starting the process to avoid broken pipe errors after the terminal closes:
>
> ```bash
> command > output.log 2> error.log &
> disown
> ```

### `setsid` Command

The `setsid` (set session ID) command runs a process in a completely new session, fully detached from the current terminal:

```bash
setsid command
```

When `setsid` runs a command:

- It creates a new session.
- The process becomes the leader of that new session and a new process group.
- It has no controlling terminal, so it is completely unaffected by terminal signals.

This is the most thorough form of detachment and is commonly used for creating daemon-like processes (see [Daemon Process](34_dameon_process.md)).

Like `disown`, `setsid` does not handle output redirection — you must manage stdout and stderr explicitly.

## Comparison

| **Feature**                        | `nohup`                    | `disown`             | `setsid`                      |
|------------------------------------|----------------------------|----------------------|-------------------------------|
| **Type**                           | Shell wrapper (user-space) | Bash built-in        | System call                   |
| **Ignores SIGHUP**                 | Yes                        | Yes (via detachment) | Yes (no controlling terminal) |
| **Works on already running jobs**  | No                         | Yes                  | No                            |
| **Creates new session**            | No                         | No                   | Yes                           |
| **Removes from shell job table**   | No                         | Yes                  | N/A                           |
| **Redirects output automatically** | Yes (`nohup.out`)          | No                   | No                            |

**In short:**

- `nohup` → Keep a process running after logout by ignoring `SIGHUP`.
- `disown` → Detach an already running job from the shell's job table.
- `setsid` → Run a process in a completely new session (true daemon-style detachment).

## Example: Running a Long-Lived Background Service

Here is a minimal script that logs a timestamp every 5 seconds:

```bash
#!/bin/bash
# myservice.sh

while true; do
    date >> /tmp/myservice.log
    sleep 5
done
```

Use `setsid` to run it as a detached background process:

    setsid ./myservice.sh 1> myservice.stdout.log 2> myservice.stderr.log < /dev/null &

The process continues running even if you log out, because `setsid` places it in a new session with no controlling terminal.

> **Note:** This is a detached background process, not a true daemon — the parent shell is still running. It becomes an orphan (and behaves like a daemon) only when the shell eventually exits. For true daemon creation, see [Daemon Process](34_dameon_process.md).

## Detachment vs. Orphaning

Detachment and orphaning are related but distinct concepts:

**Detachment** means a process is protected from terminal signals (`SIGHUP`). It happens immediately when you use `nohup`, `disown`, or `setsid`. The process can survive the terminal closing, but the shell is still its parent in the kernel's process tree.

**Orphaning** means a process's parent has exited. When that happens, the kernel re-parents the process to `init` (PID 1) or `systemd`, which becomes its new parent. This happens later — when the shell actually exits.

Consider this timeline:

```
1. You run:          nohup sleep 300 &
                     └── sleep is DETACHED (immune to SIGHUP)
                     └── Parent is still the shell

2. You close the terminal:
                     └── Shell exits
                     └── sleep becomes an ORPHAN
                     └── Kernel re-parents it to init/systemd
```

Without detachment, the process would be killed by `SIGHUP` at step 2 and never get the chance to be re-parented. Detachment is what allows a process to **survive** becoming an orphan.

> **Note:** Daemon processes rely on this mechanism — they intentionally detach and allow their parent to exit. For more details, see [Daemon Process](34_dameon_process.md).

---

[← Previous: Background](32_background.md) | [Next: Daemon Process →](34_dameon_process.md)
