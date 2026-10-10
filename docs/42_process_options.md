# Processing Options

In Bash, you can process command-line options using several approaches:

- **Manual parsing** — loop through arguments with `while` and `case`
- **`getopts`** — a shell builtin for short options
- **`getopt`** — an external utility that supports both short and long options
- **Third-party tools** — libraries such as [getoptions](https://github.com/ko1nksm/getoptions), [shflags](https://github.com/kward/shflags), and [argbash](https://github.com/matejak/argbash)

The following table compares the most common approaches:

| Feature                                 | `getopts`              | `getopt`                | `getoptions`              | `argbash`                 |
|-----------------------------------------|------------------------|-------------------------|---------------------------|---------------------------|
| **Implementation**                      | Shell builtin command  | External command        | Shell script              | Code generator (M4)       |
| **Portability**                         | Yes                    | No                      | Yes                       | ⚠ Bash ≥ 3.0             |
| **Short option beginning with `-`**     | ✔️                     | ✔️                     | ✔️                        | ✔️                        |
| **Short option beginning with `+`**     | ⚠ zsh, ksh, mksh only  | ❌                     | ✔️                        | ❌                        |
| **Combining short options**             | ✔️                     | ✔️                     | ✔️                        | ✔️                        |
| **Long option beginning with `--`**     | ❌                     | ⚠ GNU only             | ✔️                        | ✔️                        |
| **Long option beginning with `-`**      | ❌                     | ⚠ GNU only             | ✔️ limited                | ❌                        |
| **Abbreviating long options**           | ❌                     | ⚠ GNU only             | ✔️                        | ❌                        |
| **Optional argument**                   | ❌                     | ⚠ GNU only             | ✔️                        | ❌                        |
| **Option after arguments**              | ❌                     | ⚠ GNU only             | ✔️                        | ✔️                        |
| **Stop option parsing with `--`**       | ✔️                     | ✔️                     | ✔️                        | ✔️                        |
| **Scanning modes**                      | ❌                     | ⚠ GNU only             | ✔️ + and enhancement      | ❌                        |
| **Subcommand**                          | ❌                     | ❌                     | ✔️                        | ❌                        |
| **Validation by pattern matching**      | ❌                     | ❌                     | ✔️                        | ⚠ experimental            |
| **Custom validation**                   | ❌                     | ❌                     | ✔️                        | ⚠ experimental            |
| **Custom error handler**                | ✔️                     | ❌                     | ✔️ more flexible          | ✔️                        |
| **Automatic help generation**           | ❌                     | ❌                     | ✔️                        | ✔️                        |

## Manual Parsing

The simplest approach is to loop through command-line arguments using `while` and `shift`:

```bash
#!/bin/bash

while [ $# -gt 0 ]; do
    echo "Argument: $1"
    shift
done
```

Invoking the script:

```bash
example.sh -c -l -f backup.tar --verbose --exclude=*.tmp -- file.txt
```

Output:

    Argument: -c
    Argument: -l
    Argument: -f
    Argument: backup.tar
    Argument: --verbose
    Argument: --exclude=*.tmp
    Argument: --
    Argument: file.txt

This script does not distinguish between options, option arguments, or positional arguments. It treats every input as a plain argument and prints it. To properly handle options, you need to add parsing logic using a `case` statement. Here is an improved version that distinguishes between options and positional arguments:

```bash
#!/bin/bash

### Default values ###

# short options
compact=false
list=false

# short option with parameter
file=""

# long option
verbose=false

# long option with parameter
exclude=""

# positional arguments
args=()

######################

# Help menu function
show_help() {
    echo "Usage: $0 [OPTIONS] -- [FILE]"
    echo
    echo "Options:"
    echo "  -c                  Compact mode"
    echo "  -l                  Enable list mode"
    echo "  -f <filename>       Specify a file"
    echo "  --verbose           Enable verbose mode"
    echo "  --exclude=<pattern> Exclude files matching pattern"
    echo "  -h, --help          Show this help message"
    echo
}

# Error function
error() {
    echo "Error: $1"
    echo "Try '$0 --help' for more information."
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c)
            compact=true
            shift
            ;;
        -l)
            list=true
            shift
            ;;
        -f)
            # making sure $2 is non-empty and does not start with -
            if [[ -n "$2" && ! "$2" =~ ^- ]]; then
                file="$2"
                shift 2
            else
                error "Option -f requires a filename argument."
            fi
            ;;
        --verbose)
            verbose=true
            shift
            ;;
        --exclude=*)
            exclude="${1#*=}"
            shift
            ;;
        --)
            shift
            while [[ $# -gt 0 ]]; do
                args+=("$1")
                shift
            done
            ;;
        -*|--*)
            error "Invalid option: $1"
            ;;
        *)
            args+=("$1")
            shift
            ;;
    esac
done

# Show parsed options
echo "Compact: $compact"
echo "List: $list"
echo "File: $file"
echo "Verbose: $verbose"
echo "Exclude: $exclude"
echo "Positional args: ${args[*]}"

# Example usage of options
if [ "$verbose" = true ]; then
    echo "Verbose mode enabled."
fi
```

Invoking the script:

```bash
example.sh -c -l -f backup.tar --verbose --exclude=*.tmp -- file.txt
```

Output:

    Compact: true
    List: true
    File: backup.tar
    Verbose: true
    Exclude: *.tmp
    Positional args: file.txt
    Verbose mode enabled.

Invoking the script with the `-h` or `--help` option:

```bash
example.sh -h
```

Output:

    Usage: example.sh [OPTIONS] -- [FILE]

    Options:
    -c                  Compact mode
    -l                  Enable list mode
    -f <filename>       Specify a file
    --verbose           Enable verbose mode
    --exclude=<pattern> Exclude files matching pattern
    -h, --help          Show this help message

Invoking the script with an invalid option:

```bash
example.sh -z
```

Output:

    Error: Invalid option: -z
    Try './example.sh --help' for more information.

The script also recognizes options that appear after positional arguments:

```bash
example.sh file.txt -c
```

**Limitations**

Manual parsing does not support combining short options. For example, `-c -l` works, but `-cl` does not:

```bash
example.sh -cl    # invalid!
```

It also does not support abbreviating long options:

```bash
example.sh --verb    # invalid!
```

Both `getopts` and `getopt` handle combined short options automatically.

## getopts

`getopts` is a built-in Bash command for parsing short options. It handles option validation, argument extraction, and error reporting.

**Syntax**

    getopts optstring variable

- `optstring` — defines the valid options and their argument requirements.
- `variable` — stores the current option letter being processed.

**Optstring Rules**

| Rule                  | Meaning                                                                                |
|-----------------------|----------------------------------------------------------------------------------------|
| Plain letter          | Defines a valid option. For example, `c` allows `-c`.                                  |
| Letter followed by `:` | The option requires an argument. For example, `f:` means `-f` expects a value.        |
| Leading `:`           | Enables silent error handling. Without it, `getopts` prints its own error messages. With it, you can handle errors yourself using the `?` and `:` cases. |

**Example:** `:clf:` means silent mode is on, `-c` and `-l` take no argument, and `-f` requires an argument.

**Key Variables**

| Variable   | Description                                                              |
|------------|--------------------------------------------------------------------------|
| `OPTARG`   | Holds the argument value for the current option (when it requires one). In silent mode, it also holds the offending option letter on errors. |
| `OPTIND`   | Tracks the index of the next argument to be processed. After `getopts` finishes, use `shift $((OPTIND - 1))` to remove the processed options from `$@` so you can handle the remaining arguments. |

Since `getopts` does not support long options (e.g., `--verbose`), you can combine it with manual parsing to handle both short and long options:

```bash
#!/bin/bash

# Initialize variables with default values
compact=false
list=false
file=""
verbose=false
exclude=""
args=()

# Parse short options using getopts
while getopts ":clf:" opt; do
    case $opt in
        c) compact=true ;;          # -c (no argument)
        l) list=true ;;             # -l (no argument)
        f) file="$OPTARG" ;;        # -f <argument>
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Missing argument: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

# Shift past the processed short options
shift $((OPTIND - 1))

# Parse long options and positional arguments manually
while [ $# -gt 0 ]; do
    case "$1" in
        --verbose)                  # --verbose (no argument)
            verbose=true
            ;;
        --exclude=*)                # --exclude=<value>
            exclude="${1#*=}"       # Extract value after '='
            ;;
        --)                         # End of options marker
            shift
            break
            ;;
        -*)                         # Invalid options
            echo "Invalid option: $1" >&2
            exit 1
            ;;
        *)                          # Positional arguments
            args+=("$1")
            ;;
    esac
    shift
done

# Print parsed values
echo "Compact: $compact"
echo "List: $list"
echo "File: $file"
echo "Verbose: $verbose"
echo "Exclude: $exclude"
echo "Arguments: ${args[*]}"
```

Note that `getopts` supports combined short options:

```bash
example.sh -cl
```

## getopt

`getopt` is an external command-line utility for parsing both short and long options. It is more flexible than `getopts` but is not a shell builtin — it must be installed on the system.

> **Note:** There are two versions of `getopt`. The traditional BSD version supports only short options. The GNU-enhanced version (commonly found on Linux) supports long options, optional arguments, abbreviations, and other advanced features. The examples below use the GNU version.

**Syntax**

```bash
PARSED=$(getopt -o SHORT_OPTIONS -l LONG_OPTIONS -- "$@")
```

- `-o clf:h` — defines short options. A colon after a letter means it requires an argument.
- `-l compact,list,file:,verbose,exclude:,help` — defines long options (comma-separated). A colon after a name means it requires an argument.
- `"$@"` — passes all script arguments to `getopt` for validation and reformatting.
- `PARSED` — receives the reformatted argument list.

After parsing, the reformatted arguments are applied with:

```bash
eval set -- "$PARSED"
```

This replaces the script's positional parameters (`$1`, `$2`, ...) with the cleaned-up output from `getopt`. The `eval` is necessary because `getopt` returns a single quoted string that needs to be re-split into individual arguments.

> **Note:** `getopt` reformats arguments into a normalized form. For example, `--exclude=*.tmp` becomes `--exclude *.tmp` (two separate arguments). This is why the `--exclude` case below uses `"$2"` and `shift 2` instead of extracting the value from `$1`.

```bash
#!/bin/bash

### Default values ###
compact=false
list=false
file=""
verbose=false
exclude=""
args=()

######################

# Help menu function
show_help() {
    echo "Usage: $0 [OPTIONS] -- [FILE]"
    echo
    echo "Options:"
    echo "  -c                  Compact mode"
    echo "  -l                  Enable list mode"
    echo "  -f <filename>       Specify a file"
    echo "  --verbose           Enable verbose mode"
    echo "  --exclude=<pattern> Exclude files matching pattern"
    echo "  -h, --help          Show this help message"
    echo
}

# Error function
error() {
    echo "Error: $1"
    echo "Try '$0 --help' for more information."
    exit 1
}

# Parse options using getopt
SHORT_OPTIONS=clf:h
LONG_OPTIONS=compact,list,file:,verbose,exclude:,help

# Validate and reformat arguments
PARSED=$(getopt -o "$SHORT_OPTIONS" -l "$LONG_OPTIONS" -- "$@")

if [[ $? -ne 0 ]]; then
    error "Failed to parse options."
fi

# Replace positional parameters with the reformatted arguments
eval set -- "$PARSED"

# Process options
while true; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--compact)
            compact=true
            shift
            ;;
        -l|--list)
            list=true
            shift
            ;;
        -f|--file)
            file="$2"
            shift 2
            ;;
        --verbose)
            verbose=true
            shift
            ;;
        --exclude)
            exclude="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            error "Invalid option: $1"
            ;;
    esac
done

# Collect positional arguments
while [[ $# -gt 0 ]]; do
    args+=("$1")
    shift
done

# Show parsed options
echo "Compact: $compact"
echo "List: $list"
echo "File: $file"
echo "Verbose: $verbose"
echo "Exclude: $exclude"
echo "Positional args: ${args[*]}"

# Example usage of options
if [ "$verbose" = true ]; then
    echo "Verbose mode enabled."
fi
```

`getopt` supports combined short options:

```bash
example.sh -cl
```

It also supports abbreviating long options:

```bash
example.sh --verb    # expands to --verbose
```

The GNU version of `getopt` also supports optional arguments using a double colon (`::`) in the option specification. For example, `-o o::` means `-o` can accept an optional value.

---

[← Previous: Program Options](41_program_options.md) | [Next: Debugging →](43_debugging.md)
