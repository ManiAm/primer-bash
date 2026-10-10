# Special Variables

Special variables are reserved variables that Bash sets and maintains automatically. They provide information about the script's arguments, process state, and execution results. These variables are **read-only** — you cannot assign values to them directly.

For the complete reference, see the [Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html) section of the Bash manual.

## Script Arguments

| Variable           | Description                                                                                         |
|--------------------|-----------------------------------------------------------------------------------------------------|
| `$0`               | The name of the script or current shell.                                                            |
| `$1`, `$2`, `...`  | Positional parameters — arguments passed to the script (`$1` is the first, `$2` the second, etc.). |
| `$#`               | The number of positional parameters passed to the script.                                           |
| `$@`               | All positional parameters as separate, individually quoted strings.                                 |
| `$*`               | All positional parameters joined into a single string, separated by the first character of `IFS`.   |

## Process and Exit Status

| Variable | Description                                                                      |
|----------|----------------------------------------------------------------------------------|
| `$?`     | The exit status of the last executed command (`0` = success, non-zero = error).  |
| `$$`     | The process ID (PID) of the current shell or script.                             |
| `$!`     | The PID of the most recently started background process.                         |
| `$-`     | The set of option flags currently enabled in the shell (e.g., `himBHs`).         |

> **See also:** [Exit Status](27_exit_status.md) for `$?`, [Background Processes](32_background.md) for `$!`, and [Command-line Arguments](40_program_args.md) for `$1`, `$@`, `$#`, and `shift`.

## Examples

### Positional Parameters

Save the following script as `script.sh`:

```bash
#!/bin/bash

echo "First Argument: $1"
echo "Second Argument: $2"

echo "Number of Arguments: $#"
echo "All Arguments (\$@): $@"
echo "All Arguments (\$*): $*"
```

Run it with two arguments:

```
$ ./script.sh arg1 arg2
First Argument: arg1
Second Argument: arg2
Number of Arguments: 2
All Arguments ($@): arg1 arg2
All Arguments ($*): arg1 arg2
```

### Exit Status (`$?`)

```bash
ls non_existent_file
echo "Exit status: $?"
# Exit status: 2
```

### Current Script PID (`$$`)

```bash
echo "Current script PID: $$"
```

### Background Process PID (`$!`)

```bash
sleep 10 &
echo "Background process PID: $!"
```

## The `$0` Variable

`$0` holds the name or path used to invoke the current script or shell.

Consider this script saved as `script.sh`:

```bash
#!/bin/bash

echo "$0"
```

Running the script directly:

```
$ ./script.sh
./script.sh
```

Running the script via the interpreter:

```
$ bash ./script.sh
./script.sh
```

In an interactive shell, `$0` contains the interpreter's name:

```
$ echo $0
/bin/bash
```

The same applies to a non-interactive shell without a script file:

```
$ bash -c 'echo $0'
bash
```

If the script is **sourced** instead of executed, `$0` remains the name of the parent shell — not the sourced file:

```
$ source script.sh
/bin/bash
```

## The `${BASH_SOURCE[0]}` Variable

`${BASH_SOURCE[0]}` is a Bash-specific variable that always contains the file path of the currently executing script, regardless of whether it was sourced or executed directly.

This makes it more reliable than `$0` for determining a script's location, especially in modular projects where scripts source other files. For most Bash scripting, prefer `${BASH_SOURCE[0]}` over `$0` when you need a consistent reference to the script file.

However, `${BASH_SOURCE[0]}` is **not portable** and works only in Bash.

## Getting the Script's Directory

Consider the following directory structure:

```
myproject/
├── script.sh -> subdir/script.sh   (symlink)
└── subdir/
    └── script.sh
```

### Approach 1: Resolve Symbolic Links

Returns the directory of the **actual file**, following any symlinks:

```bash
#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
echo "Script directory: $SCRIPT_DIR"
```

```
$ ./myproject/script.sh
Script directory: /home/maniam/myproject/subdir
```

### Approach 2: Preserve Symbolic Links

Returns the directory of the **symlink itself**, without resolving it:

```bash
#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath -s "${BASH_SOURCE[0]}")")
echo "Script directory: $SCRIPT_DIR"
```

```
$ ./myproject/script.sh
Script directory: /home/maniam/myproject
```

Use **Approach 1** when you need the path to the real file (e.g., for debugging or locating resources relative to the actual script). Use **Approach 2** when you want to maintain the symlink structure.

---

[← Previous: Built-in Variables](13_built_in_variables.md) | [Next: Input and Output →](15_input_output.md)
