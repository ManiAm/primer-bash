# Shell Types

Every Bash session can be classified along two independent axes: **interactive vs non-interactive** and **login vs non-login**. Understanding these distinctions matters because they determine which configuration files the shell reads at startup and how the shell behaves. This page explains each type, shows how to identify it, and demonstrates the differences with a hands-on example.

## Interactive vs Non-Interactive Shells

### Interactive Shell

An **interactive shell** is a shell session where the user types commands directly into a terminal and receives output in real time. The shell displays a prompt, waits for input, executes the command, and then displays the next prompt. Features such as command history, tab completion, and prompt customization (`PS1`) are available only in interactive shells.

Opening an interactive Bash shell:

    $ bash

Opening an interactive Bash shell on a remote host:

    $ ssh user@remote-host

**Checking whether a shell is interactive**

The special variable `$-` contains single-character flags that describe the current shell's settings. If the `i` flag is present, the shell is interactive:

```bash
[[ $- == *i* ]] && echo "Interactive" || echo "Non-Interactive"
```

> For a complete list of special variables in Bash, see [Special Variables](14_special_variables.md).

### Non-Interactive Shell

A **non-interactive shell** runs without user interaction. Instead of displaying a prompt and waiting for input, it executes the commands or script passed to it and then exits. Non-interactive shells are ideal for automating tasks.

Executing a script:

    $ bash script.sh

Executing a command string directly:

    $ bash -c 'echo "This is a non-interactive shell"'

Running a command on a remote host without opening a session:

    $ ssh user@remote-host date

Scheduled via a cron job:

    * * * * * /path/to/script.sh

## Login vs Non-Login Shells

### Login Shell

A **login shell** is the first shell session that starts when a user logs into the system. Its job is to initialize the user's environment from scratch by reading login-specific configuration files that set up environment variables, paths, and other session-wide settings.

A login shell is started:

- When you log in through a **TTY** (console) or **SSH session**, or
- When you explicitly start a shell with the `--login` flag or a leading hyphen (e.g., `-bash`).

> For details on which configuration files a login shell reads — and in what order — see [Shell Config](02_shell_config.md#bash-configuration-files).

### Non-Login Shell

A **non-login shell** is any shell that is not the initial login session. When you open a new terminal window on the desktop, or type `bash` inside an existing shell, the resulting shell is typically a non-login shell. It reads only `~/.bashrc` (not the login-specific files like `/etc/profile` or `~/.bash_profile`).

### Combining the Two Axes

Because interactive/non-interactive and login/non-login are independent, four combinations are possible:

| Type                             | Example                              | Config Files Read               |
|----------------------------------|--------------------------------------|---------------------------------|
| Interactive login                | `bash --login`, `ssh user@host`      | `/etc/profile`, `~/.bash_profile` (or fallbacks), `~/.bashrc`* |
| Interactive non-login            | `bash` (from a terminal)             | `~/.bashrc`                     |
| Non-interactive login            | `bash --login -c date`               | `/etc/profile`, `~/.bash_profile` (or fallbacks) |
| Non-interactive non-login        | `bash script.sh`, `bash -c '...'`    | None (by default)               |

\* `~/.bashrc` is loaded only if `~/.bash_profile` (or `~/.profile`) explicitly sources it, which is the common convention.

### Checking for a Login Shell

Use the `shopt` built-in to check whether the current shell is a login shell:

    $ shopt login_shell

- **`login_shell on`** — the shell is a login shell.
- **`login_shell off`** — the shell is a non-login shell.

### Terminal Emulators and Login Shells

A terminal emulator (e.g., GNOME Terminal, Konsole, or xterm) usually launches an **interactive non-login** shell when opened from the desktop. This means it reads `~/.bashrc` but skips the login configuration files.

If you need login shell behavior in your terminal emulator, you can change this. For example, in GNOME Terminal:

1. Go to **Edit → Preferences → Profile → Command**.
2. Check **"Run command as a login shell"**.

Once enabled, every new terminal tab or window will behave as a login shell and read the full set of login configuration files.

## Hands-On: Observing Configuration File Order

This exercise uses a Docker container to demonstrate exactly which configuration files run — and in what order — for each shell type.

### Setting Up the Container

Pull the Ubuntu 20.04 Docker image:

    $ docker pull ubuntu:20.04

Run the container:

    $ docker run -d -it --name shell-test ubuntu:20.04

Open an interactive shell inside the container:

    $ docker exec -it shell-test /bin/bash

Install a text editor:

    $ apt update
    $ apt-get install nano

### Adding Trace Messages

Open each of the following files with `nano` and add an `echo` command at the beginning and end of the file:

- `/etc/profile`
- `~/.profile`
- `~/.bashrc`

For example, add `echo "/etc/profile start"` as the first line and `echo "/etc/profile end"` as the last line of `/etc/profile`. Repeat this pattern for the other two files.

Once the edits are saved, exit the container and re-enter it to test each shell type.

### Testing Login Shells

**Non-interactive login shell:**

    $ bash --login -c "shopt login_shell"

    /etc/profile start
    /etc/profile end
    ~/.profile start
    ~/.profile end
    login_shell     on

Only the login configuration files run. The shell reads `/etc/profile` first, then `~/.profile`.

**Interactive login shell:**

    $ bash --login

    /etc/profile start
    /etc/profile end
    ~/.profile start
    ~/.bashrc start
    ~/.bashrc end
    ~/.profile end

This time `~/.bashrc` also runs. This is because `~/.profile` explicitly sources `~/.bashrc` — a common convention on Debian-based systems. The login shell itself does not read `~/.bashrc` directly.

### Testing Non-Login Shells

**Non-interactive non-login shell:**

    $ bash -c "shopt login_shell"

    login_shell     off

No configuration files run at all. The shell simply executes the given command and exits.

**Interactive non-login shell:**

    $ bash

    ~/.bashrc start
    ~/.bashrc end

Only `~/.bashrc` runs. This is the typical behavior when you open a new terminal window on the desktop or type `bash` inside an existing shell.

---

[← Previous: Bash](03_bash.md) | [Next: Auto-Completion →](05_auto_completion.md)
