# File and Directory Operations

Bash provides built-in commands for navigating and managing directories. These are especially useful in scripts or workflows that require switching between directories while keeping track of where you have been.

| Command  | Description                                                      |
|----------|------------------------------------------------------------------|
| `pwd`    | Print the current working directory.                             |
| `cd`     | Change the current working directory.                            |
| `pushd`  | Push the current directory onto a stack and change to a new one. |
| `popd`   | Pop the top directory from the stack and change to it.           |
| `dirs`   | Display the directory stack.                                     |

## pwd

The `pwd` (print working directory) command displays the full path of the directory you are currently in.

```bash
pwd             # Print the current directory, e.g., /home/user/docs
pwd -P          # Print the physical path (resolves symbolic links)
pwd -L          # Print the logical path (preserves symbolic links)
```

## cd

The `cd` (change directory) command moves you to a different directory.

```bash
cd /home/user   # Change to the specified directory
cd ..           # Move up one level to the parent directory
cd .            # Stay in the current directory (no effect)
cd ~            # Go to the home directory
cd              # Go to the home directory (same as cd ~)
cd -            # Switch to the previous directory
```

## Directory Stack: pushd, popd, and dirs

A **directory stack** is an ordered list of directories that you can push onto and pop from. Think of it like a stack of plates — you add (push) plates on top and remove (pop) them from the top. This follows the **LIFO** (Last-In, First-Out) principle: the most recently pushed directory is the first one removed.

The directory stack lets you save your place, navigate somewhere else, and then return — without having to remember full paths.

### pushd

The `pushd` command saves the current directory onto the stack and then changes to the specified directory.

```bash
pushd /etc      # Save the current directory on the stack and move to /etc
pushd /var/log  # Save /etc on the stack and move to /var/log
```

### popd

The `popd` command removes the top directory from the stack and changes to it. Use it to retrace your steps after navigating with `pushd`.

```bash
popd            # Return to the directory on top of the stack
```

### dirs

The `dirs` command displays the current directory stack. Use it to inspect the saved directories before popping them.

```bash
dirs            # Display the directory stack
dirs -v         # Display the stack with numbered indices
dirs -l         # Display full directory paths (expand ~ to /home/user)
```

## Example Workflow

The following example shows how `pushd`, `popd`, and `dirs` work together:

```bash
pwd                # /home/user
pushd /etc         # Save /home/user on the stack, move to /etc
pushd /var/log     # Save /etc on the stack, move to /var/log
dirs               # Output: /var/log /etc /home/user
popd               # Pop /var/log, move back to /etc
popd               # Pop /etc, move back to /home/user
pwd                # /home/user
```

---

[← Previous: Input and Output](15_input_output.md) | [Next: Shell Expansions →](17_shell_expansions.md)
