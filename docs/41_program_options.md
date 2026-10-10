# Program Options

Options are special arguments that modify the behavior of a command.

By convention, options are prefixed with a single hyphen (`-`) for short options and a double hyphen (`--`) for long options.

Options allow users to enable or disable features, specify settings, or provide additional instructions without changing the program code itself.

| Option Type                     | Short Form      | Long Form            |
|---------------------------------|-----------------|----------------------|
| Takes no argument (flag)        | `-f`            | `--flag`             |
| Takes one argument (parameter)  | `-p val`        | `--param val`        |
| Takes one optional argument     | `-o[DEFAULT]`   | `--option[=DEFAULT]` |

## Short Options

A single hyphen `-` followed by a single character.

```bash
ls -l
```

Multiple short options can be combined into a single group:

```bash
ls -l -a

ls -la
```

Short options can appear in any order; thus `-la` is equivalent to `-al`.

Short options are quick and concise for frequent use. However, due to the limited number of letters, their meanings are not always obvious.

## Long Options

Double hyphens `--` followed by a full word.

```bash
ls --all
```

Long options are self-explanatory and easier to read, making them better for documentation and learning. However, they are longer to type, which can slow down frequent use.

Frequently used options should have both forms for accessibility:

| Short Option | Long Option    | Description                                     |
|--------------|----------------|-------------------------------------------------|
| `-h`         | `--help`       | Display help information.                       |
| `-v`         | `--verbose`    | Enable verbose output.                          |
| `-V`         | `--version`    | Display version details.                        |
| `-r`         | `--recursive`  | Apply the command recursively.                  |
| `-f`         | `--force`      | Force an operation without confirmation.        |

## Option with One Argument (Parameter)

Short or long options can accept one argument, referred to as a parameter.

Parameters provide input values for options that require them.

Here is a short option with a parameter:

```bash
gcc -o example example.c
```

The whitespace separating the short option and its parameter is optional:

```bash
gcc -oexample example.c
```

Here is a long option with a parameter:

```bash
gcc --output example example.c
```

An equal sign (`=`) can also separate a long option from its parameter:

```bash
gcc --output=example example.c
```

## Optional Arguments

An optional argument allows an option to accept a value, but the value is not required. If no value is provided, the option uses a default value defined by the program.

Short option with an optional argument:

```bash
# Value attached directly (no space allowed)
cmd -o[DEFAULT]
```

Long option with an optional argument:

```bash
# Value attached with = (no space allowed)
cmd --output[=DEFAULT]
```

Note that optional arguments must be attached directly to the option (no space). A space would cause the parser to treat the next word as a separate positional argument.

## Combining Short and Long Options

Many programs support mixing short and long options in the same command:

```bash
tar -c -f backup.tar --verbose --exclude=*.tmp
```

- `-c` — Create a new archive (short option with no argument).
- `-f backup.tar` — Specify the archive filename (short option with parameter).
- `--verbose` — Enable detailed output (long option with no argument).
- `--exclude=*.tmp` — Exclude files matching the pattern (long option with parameter).

## Abbreviating Long Options

Many programs allow you to type a shortened version of a long option, as long as the abbreviation is unambiguous.

For example, if a command supports these long options:

    --help
    --version
    --verbose

You can abbreviate them:

    --he    → Expands to --help
    --ver   → Expands to --version (only if --verbose is not present)
    --verb  → Expands to --verbose

This saves time and effort, especially with long or complex option names.

If multiple options share the same prefix, abbreviations become ambiguous. For example, when a command supports both `--version` and `--verbose`, using `--ver` is ambiguous because it could match either one. Most tools will report an error in this case.

## Scanning Modes

Scanning modes control how a command interprets the order of options and positional arguments.

**POSIX Mode**

POSIX-compliant commands require options to appear before positional arguments. Once a positional argument is encountered, all subsequent inputs are treated as positional arguments, even if they look like options.

```bash
ls -l file.txt -a
```

In POSIX mode, `-a` is treated as a positional argument (not an option) because it appears after `file.txt`.

**Permissive Mode**

Permissive mode allows options to appear anywhere, even after positional arguments. This behavior is more flexible but non-compliant with POSIX. It is supported by GNU-style utilities like `tar`:

```bash
tar -cf archive.tar file1.txt file2.txt -v
```

Here, `-v` is still recognized as an option despite appearing after the filenames.

## End-of-Options Marker

The `--` marker signals the end of options in a command. Any arguments that appear after `--` are treated as positional arguments, even if they begin with a hyphen (`-`).

This is useful when a filename or value starts with `-` and would otherwise be mistaken for an option:

```bash
grep -e pattern -- -file.txt
```

- `-e pattern` — Short option with a parameter specifying the pattern to match.
- `--` — Marks the end of options.
- `-file.txt` — Treated as a filename, not an option.

## Repeated Options

When an option appears multiple times, its behavior depends on how the program's parser is implemented.

**Last Value Wins (Most Common)**

Many parsers, including Python's `argparse`, use the last occurrence and override previous values:

```bash
wget -O output1.txt -O output2.txt https://www.digitalocean.com/robots.txt
```

Here, the file is saved to `output2.txt`.

**First Value Wins**

Less common; the first occurrence takes priority:

```bash
curl -o output1.txt -o output2.txt https://www.digitalocean.com/robots.txt
```

**Append Values**

Some programs collect all values from repeated options into a list:

```bash
# Adds all paths to the compiler's include search list
gcc -I /path1 -I /path2 -I /path3 main.c

# Searches for .txt files across all specified directories
find /dir1 /dir2 /dir3 -name "*.txt"
```

**Accumulate Flags**

Some programs treat repeated flags as incrementing a level, commonly used for verbosity:

```bash
# Normal verbosity
tar -v -cf archive.tar files/

# Higher verbosity
tar -v -v -cf archive.tar files/
```

**Error on Conflict**

Some programs reject conflicting repeated options and report an error:

```bash
tar -cf archive.tar -cf another.tar source
```

## Subcommands

Commands can have nested subcommands to organize functionality hierarchically. Each subcommand behaves as an independent command with its own set of options and arguments.

For example, the `git` command has subcommands such as `add`, `commit`, and `push`:

```bash
git add file.txt
git commit -m "Message"
git push origin main
```

> For information on positional arguments and special variables, see [Program Args](40_program_args.md).
>
> For processing options with `getopts`, `getopt`, and manual parsing, see [Process Options](42_process_options.md).

---

[← Previous: Program Args](40_program_args.md) | [Next: Process Options →](42_process_options.md)
