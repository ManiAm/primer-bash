# Auto-Completion

Bash auto-completion lets you press the `Tab` key to complete partially typed commands, filenames, variables, and other input. It reduces typing, speeds up your workflow, and helps prevent errors in the terminal.

Auto-completion is powered by the **Readline** library, which Bash uses for all interactive input handling. Readline supports programmable behavior, allowing completions to change based on context.

## Default Completions

Bash provides several categories of completion out of the box, with no extra configuration required.

### File and Directory Completion

Bash can auto-complete filenames and directory paths. If you type a partial name without a path, Bash matches against entries in the current working directory:

    $ ls Doc [Tab]
    $ ls Documents/

If you include a path prefix, Bash matches within that directory instead:

    $ cd /etc/netw [Tab]
    $ cd /etc/network/

If there is only one match, Bash completes it automatically. If there are multiple matches, a single `Tab` press does nothing. Pressing `Tab` twice lists all candidates:

    $ cd /etc/net [Tab][Tab]

    netplan/             network/             networkd-dispatcher/

When the number of possible completions is very large, Bash asks for confirmation instead of flooding the terminal:

    Display all <number> possibilities? (y or n)

You can configure the threshold at which Bash prompts by setting the `completion-query-items` Readline variable. For example, to prompt only when there are more than 50 matches:

    bind 'set completion-query-items 50'

To display all possibilities without ever asking, set the value to `-1`:

    bind 'set completion-query-items -1'

Add the `bind` command to your `~/.bashrc` to make the setting permanent. After editing `~/.bashrc`, reload it with:

    source ~/.bashrc

### Command Completion

Bash can auto-complete the names of executable commands:

    $ pyth [Tab]
    python

If multiple matches exist, pressing `Tab` twice shows them all:

    python3   python3.12   python3.8   python3.8-config   python3-config   python3-futurize   python3-pasteurize

In Linux, a file is treated as a command only if **both** of the following are true:

- It has executable permissions (`chmod +x`).
- It is located in a directory listed in `PATH`.

If either condition is missing, Bash will not auto-complete the file as a command.

**Example — executable permission and auto-completion:**

Assume a script called `myscript.sh` exists in `/usr/local/bin` (which is in your `PATH`), but it does **not** have executable permission:

    -rw-r--r-- 1 root root 0 Dec 17 11:26 myscript.sh

Typing the script's name and pressing `Tab` produces no completion:

    $ mysc [Tab]

Now grant executable permission:

    $ chmod +x /usr/local/bin/myscript.sh

Try again — Bash completes the name because the script is now recognized as an executable command.

### Environment Variable Completion

Bash can auto-complete environment variable names when the input starts with `$`:

    $ echo $HOM [Tab]
    $ echo $HOME

### Username Completion

Bash can auto-complete usernames when the input starts with `~`:

    $ cd ~ro [Tab]
    $ cd ~root

Bash retrieves the list of usernames from `/etc/passwd`, not from the names of home directories.

## Programmable Completions

Programmable completions let you define custom completion behavior for specific commands, going beyond the built-in defaults. This is done using the `complete` built-in and, optionally, custom Bash functions.

To list all programmable completions currently defined on your system:

    $ complete -p

### Command Options Completion

Tools like Git, Docker, and kubectl ship their own completion scripts that provide context-aware suggestions for subcommands and options.

For example:

    $ git che [Tab]
    $ git checkout

The completion logic is provided by a Bash function registered with `complete`. You can inspect these registrations:

    $ complete -p git
    complete -o bashdefault -o default -o nospace -F __git_wrap__git_main git

    $ complete -p docker
    complete -F _docker docker

    $ complete -p apt-get
    complete -F _apt_get apt-get

### Long Options Completion

Long options are command-line flags that start with `--` (double dashes), such as `--help` and `--version`. Bash can auto-complete these options using built-in completion functions like `_longopt`.

> For a detailed explanation of short and long options, see [Command-line Options](41_program_options.md).

Many common utilities are registered with `_longopt`:

    <snip>
        complete -F _longopt awk
        complete -F _longopt base64
        complete -F _longopt bash
        complete -F _longopt cat
        complete -F _longopt cp
        complete -F _longopt cut
        complete -F _longopt date
    <snip>

For example, typing `cat --` and pressing `Tab` twice shows all available long options for `cat`:

    $ cat --[Tab][Tab]

    --help              --number-nonblank   --show-ends         --show-tabs         --version
    --number            --show-all          --show-nonprinting  --squeeze-blank

### Hostname Completion

`_known_hosts` is a Bash completion function that completes hostnames. It retrieves names from sources such as:

- The user's SSH known-hosts file (`~/.ssh/known_hosts`)
- The global known-hosts file (`/etc/ssh/ssh_known_hosts`)
- Possibly `/etc/hosts` and DNS entries, depending on system configuration

Here are some examples of commands registered with `_known_hosts`:

    complete -F _known_hosts dig
    complete -F _known_hosts ftp
    complete -F _known_hosts mtr
    complete -F _known_hosts ssh-installkeys
    complete -F _known_hosts telnet
    complete -F _known_hosts traceroute

For example:

    $ telnet loc [Tab]
    $ telnet localhost

### Custom Word List Completion

You can define your own list of words for auto-completion using `complete -W`:

    complete -W "start stop restart status" mycmd

Now when you type the command and press `Tab`:

    $ mycmd [Tab]

    restart  start    status   stop

---

[← Previous: Shell Types](04_shell_type.md) | [Next: History →](06_history.md)
