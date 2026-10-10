# Bash Keywords

In Bash, **keywords** (also called **reserved words**) are words that have special meaning to the shell. They control the flow of execution and define syntactic structures such as loops, conditionals, and functions. Keywords cannot be used as command names in contexts where the shell would interpret them syntactically.

| **Category**          | **Keyword**             | **Description**                                                              |
|-----------------------|-------------------------|------------------------------------------------------------------------------|
| Control Structures    | `if`                    | Starts a conditional block.                                                  |
|                       | `then`                  | Marks the start of a block to execute if the condition is true.              |
|                       | `else`                  | Marks the block to execute if the condition is false.                        |
|                       | `elif`                  | Adds an additional condition to an `if` block.                               |
|                       | `fi`                    | Ends an `if` block.                                                          |
|                       | `case`                  | Starts a multi-branch conditional statement.                                 |
|                       | `esac`                  | Ends a `case` block.                                                         |
|                       | `select`                | Creates an interactive menu for user selection.                              |
| Loops                 | `for`                   | Starts a loop that iterates over a list.                                     |
|                       | `while`                 | Starts a loop that runs while a condition is true.                           |
|                       | `until`                 | Starts a loop that runs until a condition becomes true.                      |
|                       | `do`                    | Marks the start of a loop body.                                              |
|                       | `done`                  | Marks the end of a loop body.                                                |
| Function Definition   | `function`              | Defines a function.                                                          |
| Miscellaneous         | `time`                  | Measures the execution time of a command or pipeline.                        |
|                       | `[[`                    | Starts an extended conditional test expression.                              |
|                       | `]]`                    | Ends an extended conditional test expression.                                |
|                       | `{` and `}`             | Groups commands into a block and executes them in the current shell.         |
|                       | `coproc`                | Starts a coprocess (a background process connected to the shell via pipes).  |

> These keywords are covered in detail in [Conditional Statements](22_conditional.md), [Loops](23_loop.md), and [Functions](25_function.md).

You can verify whether a word is a keyword using the `type` built-in:

    $ type for
    for is a shell keyword

## Bash Built-in Utilities

A **built-in utility** is a command that is implemented directly inside the Bash shell itself rather than as a separate executable on disk. Built-in commands are faster than external commands because they run within the current shell process — there is no need to create (fork) a new process.

| **Category**                      | **Command**       | **Description**                                                                |
|-----------------------------------|-------------------|--------------------------------------------------------------------------------|
| **Environment and Variables**     | `export`          | Marks variables to be exported to child processes.                             |
|                                   | `unset`           | Removes a variable or function.                                                |
|                                   | `declare`         | Declares variables and assigns them attributes.                                |
|                                   | `typeset`         | Synonym for `declare`; retained for compatibility with older scripts.          |
|                                   | `local`           | Declares a variable with local scope inside a function.                        |
|                                   | `alias`           | Defines or displays aliases.                                                   |
|                                   | `unalias`         | Removes an alias.                                                              |
|                                   | `command`         | Runs a command, bypassing shell function lookup.                               |
| **Input/Output**                  | `echo`            | Prints text to standard output.                                                |
|                                   | `printf`          | Formats and prints text to standard output.                                    |
|                                   | `read`            | Reads a line of input from standard input.                                     |
| **Information**                   | `type`            | Displays information about a command (alias, built-in, keyword, or external).  |
|                                   | `help`            | Displays help for built-in commands.                                           |
|                                   | `history`         | Displays or manipulates the command history.                                   |
| **Arithmetic**                    | `let`             | Evaluates arithmetic expressions.                                              |
| **Control Flow**                  | `return`          | Exits a function and optionally returns a status code.                         |
|                                   | `break`           | Exits a loop prematurely.                                                      |
|                                   | `continue`        | Skips the rest of the current loop iteration and moves to the next one.        |
|                                   | `exec`            | Replaces the current shell process with another command.                       |
|                                   | `exit`            | Exits the shell with a status code.                                            |
|                                   | `eval`            | Evaluates a string as a shell command.                                         |
| **File and Directory Operations** | `cd`              | Changes the current working directory.                                         |
|                                   | `pwd`             | Prints the current working directory.                                          |
|                                   | `pushd`           | Saves the current directory and switches to a new one.                         |
|                                   | `popd`            | Returns to the last directory saved on the directory stack.                    |
|                                   | `dirs`            | Displays the directory stack.                                                  |
| **Process Management**            | `kill`            | Sends a signal to a process.                                                   |
|                                   | `wait`            | Waits for a background process to finish.                                      |
|                                   | `jobs`            | Lists background jobs.                                                         |
|                                   | `bg`              | Resumes a stopped job in the background.                                       |
|                                   | `fg`              | Brings a job to the foreground.                                                |
| **Shell Options**                 | `shopt`           | Toggles Bash-specific shell options.                                           |
|                                   | `set`             | Sets or unsets shell options and positional parameters.                        |
| **Miscellaneous**                 | `source`          | Reads and executes commands from a file in the current shell.                  |
|                                   | `.`               | Same as `source`.                                                              |
|                                   | `true`            | Does nothing and returns a success status (exit code 0).                       |
|                                   | `false`           | Does nothing and returns a failure status (exit code 1).                       |
|                                   | `test`            | Evaluates a conditional expression.                                            |
|                                   | `shift`           | Shifts positional parameters to the left.                                      |
|                                   | `trap`            | Catches signals or events and executes specified commands.                     |

> Many of these built-ins are covered in depth in later sections, including [Input and Output](15_input_output.md), [File and Directory Operations](16_file_dir.md), [Alias](26_alias.md), [Shell Options](39_shell_options.md), [Background Processes](32_background.md), and [`trap`](38_trap.md).

You can check what type of command a name refers to using the `type` built-in:

    $ type cd
    cd is a shell builtin

    $ type find
    find is hashed (/usr/bin/find)

    $ type ls
    ls is aliased to `ls --color=auto'

A command name can exist as both a built-in and an external binary. Use `type -a` to see all matches:

    $ type -a echo
    echo is a shell builtin
    echo is /usr/bin/echo
    echo is /bin/echo

When a name matches both a built-in and an external command, the built-in takes precedence. So when you run `echo`, the built-in version is executed by default.

## Installing Bash from Source

This section walks through compiling Bash from source inside a Docker container. Using a container keeps your host system clean and provides a reproducible environment.

Pull the Ubuntu 20.04 Docker image:

    $ docker pull ubuntu:20.04

Run the container:

    $ docker run -d -it --name bash-install ubuntu:20.04

Open an interactive shell inside the container:

    $ docker exec -it bash-install /bin/bash

Install the required build dependencies:

    $ apt update
    $ apt-get install -y wget build-essential

Change to the home directory:

    $ cd ~

Visit the GNU Bash official website to find available versions: https://ftp.gnu.org/gnu/bash/

Download the desired version (replace `x.y.z` with the actual version number):

    $ wget http://ftp.gnu.org/gnu/bash/bash-x.y.z.tar.gz

Extract the source code and enter the directory:

    $ tar -xvzf bash-x.y.z.tar.gz
    $ cd bash-x.y.z

From here you can choose between a **system-wide** (replaces the existing Bash) or a **local** (installs alongside the existing Bash) installation.

### System-Wide Installation

Configure the build to install into `/usr`:

    $ ./configure --prefix=/usr

Compile the source code:

    $ make -j$(nproc)

Verify that the new Bash binary was built successfully:

    $ ./bash --version

Install it system-wide (this replaces the existing `/usr/bin/bash`):

    $ make install

### Local Installation

Configure the build to install into `/usr/local`:

    $ ./configure --prefix=/usr/local

Compile the source code:

    $ make -j$(nproc)

Verify that the new Bash binary was built successfully:

    $ ./bash --version

Install it:

    $ make install

The system Bash at `/bin/bash` remains untouched. The newly installed version is placed in `/usr/local/bin`:

    $ type -a bash
    bash is /usr/local/bin/bash
    bash is /usr/bin/bash
    bash is /bin/bash

When you run `bash`, the newly installed version is executed because `/usr/local/bin` appears before `/usr/bin` in `PATH`:

    $ bash --version

---

[← Previous: Shell Config](02_shell_config.md) | [Next: Shell Types →](04_shell_type.md)
