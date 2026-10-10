# Daemon Process

A **daemon** is a background process that is detached from its controlling terminal and has intentionally become an orphan. In other words, it combines three things:

- **Background process** — It runs without blocking the terminal, freeing the shell for other work (see [Background Process](32_background.md)).

- **Detached from the terminal** — It is immune to `SIGHUP`, so closing the terminal does not kill it (see [SIGHUP and Process Detachment](33_background_sighup.md)).

- **Orphaned** — Its parent has exited, so the kernel re-parents it to `init` (PID 1) or `systemd`, making it independent of any user session.

In Unix-like systems, daemons often have names ending in `d` — for example, `sshd` (SSH server), `httpd` (HTTP server), and `crond` (cron scheduler). They are typically used for long-running services such as web servers, task schedulers, and system monitors.

Daemons typically start automatically at system boot and stop at shutdown.

## How Daemons Are Created

Creating a daemon involves a standard sequence of steps:

1. **Fork and detach** — Launch a child process in a new session, detached from the controlling terminal.
2. **Orphan** — The parent exits immediately, orphaning the child. The kernel re-parents it to `init` (PID 1) or `systemd`.
3. **Redirect I/O** — Redirect stdin, stdout, and stderr to `/dev/null` or to log files.
4. **Clean up** (optional) — Change the working directory to `/` and reset the file permissions mask (`umask`).

The following script performs all of these steps internally — you just run it and it daemonizes itself:

```bash
#!/bin/bash
# mydaemon.sh

# Function that contains the daemon's main loop
run_daemon() {
    while true; do
        echo "$(date): Daemon is running..."
        sleep 5
    done
}

# Daemonize: re-launch this script in a new session, then exit the parent
daemonize() {

    # If this is the original invocation:
    if [ "$1" != "__daemon__" ]; then
        # Step 1: Fork and detach — re-launch in a new session
        setsid "$0" __daemon__ 1> /dev/null 2>&1 &
        # Step 2: Orphan — parent exits, child is re-parented to init/systemd
        exit 0
    fi

    # This point is reached only by the re-launched child.
    # Step 3: Redirect I/O
    exec 1> mydaemon.stdout.log 2> mydaemon.stderr.log < /dev/null

    # Run the daemon function
    run_daemon
}

# Start the daemonization process
daemonize "$1"
```

**How it works:**

1. `setsid` re-launches the script in a new session (step 1), then the parent exits, orphaning the child (step 2).
2. The re-launched child redirects its file descriptors to log files (step 3) and enters the main loop.

**Usage:**

Make the script executable and start it:

    $ chmod +x mydaemon.sh
    $ ./mydaemon.sh

Verify the process is running:

    $ ps aux | grep mydaemon

Sample output:

    maniam     20211  0.0  0.0   9500  3408 ?    S    20:48   0:00 /bin/bash ./mydaemon.sh __daemon__

Notice the `?` in the TTY column — the process has no controlling terminal.

You can also check the log files:

    $ ls -l mydaemon.stdout.log mydaemon.stderr.log

To stop the daemon:

    $ kill <PID>

---

[← Previous: SIGHUP](33_background_sighup.md) | [Next: Subshell →](35_subshell.md)
