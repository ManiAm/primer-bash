# Shell Options

Shell options are configurable settings that control how Bash parses commands, handles errors, manages history, and processes patterns. They let you customize the shell's behavior for both interactive use and scripting.

Bash shell options fall into two categories:

- **`set` options** — control execution behavior, error handling, and debugging. Managed with `set -o` / `set +o`.
- **`shopt` options** — control shell features like pattern matching and history management. Managed with `shopt -s` / `shopt -u`.

## `set` Options

`set` options control command execution, error handling, and debugging. Most are defined by the POSIX standard and work across different shells (Bash, Zsh, sh, etc.). A few (like `pipefail`) are Bash-specific.

Enable an option:

    set -o option_name

Disable an option:

    set +o option_name

> **Note:** The syntax may seem backwards: `-` enables and `+` disables. Think of `-` as "turn on this flag" and `+` as "remove this flag."

### Common `set` Options

Many `set` options also have a single-character shorthand. You can use either form:

```bash
set -o errexit    # enable (long form)
set -e            # enable (shorthand)

set +o errexit    # disable (long form)
set +e            # disable (shorthand)
```

| Option               | Flag | Description                                                                                     |
|----------------------|------|-------------------------------------------------------------------------------------------------|
| `errexit`            | `e`  | Exit immediately if a command exits with a non-zero status.                                     |
| `nounset`            | `u`  | Treat unset variables as an error during parameter expansion.                                   |
| `pipefail`           | —    | Return the exit status of the last failed command in a pipeline (instead of the last command).  |
| `xtrace`             | `x`  | Print each command and its arguments before execution (useful for debugging).                   |
| `verbose`            | `v`  | Print shell input lines as they are read.                                                       |
| `noclobber`          | `C`  | Prevent overwriting existing files with output redirection (`>`).                               |
| `noglob`             | `f`  | Disable filename expansion (globbing).                                                          |
| `noexec`             | `n`  | Read commands but do not execute them (useful for syntax checking).                             |
| `allexport`          | `a`  | Automatically export all variables and functions defined in the shell.                          |
| `errtrace`           | `E`  | Ensure `ERR` traps are inherited by shell functions, subshells, and command substitutions.      |
| `functrace`          | `T`  | Ensure `DEBUG` and `RETURN` traps are inherited by shell functions and subshells.               |
| `hashall`            | `h`  | Cache command locations after first lookup to speed up repeated execution.                      |
| `histexpand`         | `H`  | Enable history expansion using `!` (e.g., `!!` for the last command).                           |
| `history`            | —    | Enable command history recording.                                                               |
| `ignoreeof`          | —    | Prevent the shell from exiting when receiving EOF (Ctrl+D).                                     |
| `interactive-comments`| —   | Allow comments (`#`) in interactive shells.                                                     |
| `keyword`            | `k`  | Allow variable assignments anywhere on the command line, not just before the command.           |
| `monitor`            | `m`  | Enable job control in interactive shells.                                                       |
| `notify`             | `b`  | Report background job completion immediately instead of waiting for the next prompt.            |
| `onecmd`             | `t`  | Execute one command and then exit.                                                              |
| `physical`           | `P`  | Resolve symbolic links to their physical directory paths.                                       |
| `posix`              | —    | Enable strict POSIX-compliant behavior.                                                         |
| `privileged`         | `p`  | Disable processing of `~/.bashrc` and `~/.profile` for security in setuid scripts.              |
| `braceexpand`        | —    | Enable brace expansion (e.g., `{a,b,c}` expands to `a b c`).                                    |
| `emacs`              | —    | Use Emacs-style key bindings for command-line editing.                                          |
| `vi`                 | —    | Use Vi-style key bindings for command-line editing.                                             |
| `nolog`              | —    | Disable logging of function definitions in the history file.                                    |

### Practical Example — Strict Mode

A widely adopted practice is to enable a "strict mode" at the top of scripts, combining `errexit`, `nounset`, and `pipefail` to catch common errors early. For a detailed walkthrough with examples, see [Debugging Bash Scripts — Strict Mode](43_debugging.md#strict-mode-set--euo-pipefail).

### Listing Current `set` Options

Use `set -o` with no arguments to display the current state of all options:

```bash
set -o
# allexport       off
# braceexpand     on
# errexit         off
# ...
```

## `shopt` Options

`shopt` (shell option) is a Bash-specific command that controls additional shell features not covered by `set`. These options are unique to Bash and are not part of the POSIX standard.

Enable an option:

    shopt -s option_name

Disable an option:

    shopt -u option_name

### Common `shopt` Options

| Option       | Description                                                             |
|--------------|-------------------------------------------------------------------------|
| `cdspell`    | Automatically correct minor typos in directory names used with `cd`.    |
| `checkhash`  | Verify a cached command path still exists before executing it.          |
| `cmdhist`    | Save multiline commands as a single entry in the history.               |
| `dotglob`    | Include hidden files (starting with `.`) in pathname expansion.         |
| `extglob`    | Enable extended pattern matching operators (e.g., `?(pat)`, `+(pat)`). |
| `extdebug`   | Enable extended debugging features for use with `trap DEBUG`.           |
| `globstar`   | Enable recursive globbing with `**` (e.g., `**/*.txt`).                |
| `histappend` | Append to the history file on exit instead of overwriting it.           |
| `huponexit`  | Send `SIGHUP` to all running jobs when an interactive login shell exits.|
| `nocaseglob` | Perform case-insensitive pathname expansion.                            |
| `nullglob`   | Expand unmatched glob patterns to an empty string instead of literally. |
| `progcomp`   | Enable programmable completion features.                                |
| `promptvars` | Expand variables and command substitutions in prompt strings.           |
| `sourcepath` | Search `$PATH` when resolving filenames passed to `source` / `.`.      |

### Practical Example — Safer Glob Handling

Combining `shopt` options makes file-processing loops more robust:

```bash
shopt -s nullglob    # unmatched globs expand to nothing (no error)
shopt -s dotglob     # include hidden files

for file in /tmp/myapp_*; do
    echo "Processing: $file"
done

# Without nullglob, if no files match, the loop body runs once
# with the literal string '/tmp/myapp_*' — which is rarely intended.
```

### Listing Current `shopt` Options

Use `shopt` with no arguments to display all options and their states:

```bash
shopt
# cdspell         off
# cmdhist         on
# dotglob         off
# ...
```

To check a single option:

```bash
shopt extglob
# extglob         on
```

---

[← Previous: Trap](38_trap.md) | [Next: Program Args →](40_program_args.md)
