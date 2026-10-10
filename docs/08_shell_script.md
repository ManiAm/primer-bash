# Shell Scripts

A shell script is a text file containing a sequence of commands written in a shell's scripting language. When you run a shell script, the shell (e.g., Bash, Zsh) acts as an interpreter — it reads the file line by line, parses each command, and executes it immediately. If a line contains an error, the shell detects it only when execution reaches that line.

Shell scripts are used to automate repetitive tasks, manage systems, and execute complex workflows without manual intervention. They can include commands, variables, loops, and conditional logic. The file typically has a `.sh` extension, though this is not mandatory.

## Writing and Running a Script

Here is a simple shell script that greets the user:

```bash
#!/bin/bash

# A simple script to greet the user
echo "Enter your name:"
read name
echo "Hello, $name! Welcome to the shell scripting world."
```

Create a file called `greet.sh` and paste the script into it. There are two ways to run it:

**Option 1 — Pass the file to an interpreter directly:**

    $ bash ./greet.sh

**Option 2 — Make the file executable and run it:**

    $ chmod +x greet.sh
    $ ./greet.sh

## Shebang

A **shebang** is the first line in a script file that tells the operating system which interpreter should be used to execute the script. It starts with `#!` followed by the absolute path to the interpreter:

```bash
#!/bin/bash
```

This ensures the correct interpreter is used regardless of which shell invokes the script. For example, if the shebang is set to `#!/bin/bash`, the script will always run in Bash — even if you execute it from Zsh or another shell.

The shebang works because `#` marks the start of a comment in most scripting languages. The interpreter specified in the shebang ignores the `#!...` line as a comment, while the operating system reads it to determine which program should execute the file.

### Missing Shebang

If a script lacks a shebang, it may still run when passed to an interpreter explicitly:

    $ bash script.sh

However, if executed directly (`./script.sh`), the current shell attempts to interpret it. This can lead to errors if the script uses syntax that the current shell does not support.

### `#!/usr/bin/env`

`/usr/bin/env` is a standard utility that locates a program by searching the directories listed in the `PATH` environment variable. It is commonly used in shebang lines to make scripts more portable:

```bash
#!/usr/bin/env bash
```

When the script runs, `/usr/bin/env bash`:

1. Searches each directory in `PATH` for an executable named `bash`.
2. Executes the first match it finds.

This approach avoids hard-coding a path like `/bin/bash` or `/usr/local/bin/bash`, which may differ across systems. It is especially useful for languages such as Python, Perl, or Ruby where the interpreter location varies.

| **Shebang**               | **Interpreter**         | **Use**                               |
|---------------------------|-------------------------|---------------------------------------|
| `#!/usr/bin/env bash`     | Bash via `env`          | Locates `bash` in the user's `PATH`.  |
| `#!/usr/bin/env python3`  | Python 3 Interpreter    | For Python 3 scripts.                 |
| `#!/usr/bin/env perl`     | Perl Interpreter        | For Perl scripts.                     |
| `#!/usr/bin/env ruby`     | Ruby Interpreter        | For Ruby scripts.                     |

## `source` Command

The `source` command (or its shorthand `.`) executes a script within the **current** shell environment rather than in a new subshell. This means any variables, functions, or settings defined in the script remain available after it finishes:

```bash
source greet.sh

# or

. greet.sh
```

This is useful when you need a script to modify the current environment — for example, updating variables or applying new shell configuration.

## Comparing Execution Methods

| **Command**             | **Runs in Subshell?** | **Requires Shebang?** | **Requires Execute Permission?** |
|-------------------------|-----------------------|-----------------------|----------------------------------|
| `bash ./myscript.sh`    | Yes                   | No                    | No                               |
| `./myscript.sh`         | Yes                   | Yes                   | Yes                              |
| `source myscript.sh`    | No                    | No                    | No                               |

> For more on how subshells work and how they differ from the current shell, see [Sub-Shells](35_subshell.md).

---

[← Previous: Shell Prompt](07_shell_prompt.md) | [Next: Shell Variables →](09_shell_variables.md)
