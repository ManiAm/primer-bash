# Alias

An alias is a shortcut that maps a custom name to a command or a series of commands. Aliases let you save keystrokes, enforce preferred options, and create memorable names for commands you use frequently.

Aliases are available only in the current shell session. They are not inherited by child processes or scripts.

## Defining an Alias

Use the `alias` built-in to create an alias. The general syntax is:

```bash
alias name='command'
```

The following example defines `ll` as a shortcut for `ls -alF` and `gs` as a shortcut for `git status`:

```bash
alias ll='ls -alF'
alias gs='git status'
```

> Always quote the command on the right-hand side. Single quotes are preferred because they prevent premature expansion of variables and special characters.

## Viewing Defined Aliases

Run `alias` without arguments to list all aliases defined in the current session:

```bash
alias
```

Sample output:

```
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias gs='git status'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
```

To view the definition of a specific alias, pass its name:

```bash
alias ll          # Output: alias ll='ls -alF'
```

## Removing an Alias

Use `unalias` to remove an alias from the current session:

```bash
unalias ll        # Removes the 'll' alias
```

After removal, running `ll` produces a "command not found" error (unless `ll` is also a standalone command on the system).

To remove **all** aliases at once:

```bash
unalias -a
```

## Making Aliases Persistent

Because aliases exist only in the current session, they are lost when the shell exits. To make them permanent, add your `alias` definitions to your shell configuration file (typically `~/.bashrc`).

> For details on which configuration file to use, see [Shell Configuration Files](02_shell_config.md).

## Common Use Cases

### Simplifying Long Commands

```bash
alias grep='grep --color=auto'
alias cls='clear && printf "\e[3J"'
alias serve='python3 -m http.server 8000'
```

### Correcting Common Typos

```bash
alias sl='ls'
alias c='clear'
```

### Adding Safety Prompts

The `-i` flag causes these commands to prompt for confirmation before overwriting or deleting:

```bash
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
```

Choose alias names that clearly represent their purpose. Avoid cryptic abbreviations that are difficult to remember.

## Alias Pitfalls

Redefining a command with an alias that changes its behavior in unexpected ways can be dangerous. For example:

```bash
alias rm='rm -rf'
rm file.txt        # Silently deletes recursively — not the intended behavior!
```

Be especially careful when aliasing destructive commands. Always test a new alias before relying on it.

## Bypassing an Alias

When you define an alias with the same name as an existing command, Bash prioritizes the alias. If you need to run the original command instead, use any of the following methods.

### Using the `command` Built-in

The `command` utility bypasses both aliases and shell functions, executing the original command directly:

```bash
command ls
```

### Using the Full Path

Specify the absolute path to the executable:

```bash
/bin/ls
```

### Using a Backslash Prefix

Any form of quoting on the command name prevents alias expansion. A backslash before the first character is the quickest way to do this:

```bash
alias grep='grep --color=auto'

\grep pattern file | wc -l   # Raw output without ANSI color codes
```

---

[← Previous: Function](25_function.md) | [Next: Exit Status →](27_exit_status.md)
