# Test Operators

The `test` command, `[ ]`, and `[[ ]]` use operators to compare strings, compare numbers, and check file attributes. This page is a reference for all available operators, organized by category.

> **Note:** For how to use `test`, `[ ]`, and `[[ ]]`, see [Test Command](19_test_command.md).

## String Operators

| **Operator**          | **Description**                                               | **Example**          |
|-----------------------|---------------------------------------------------------------|----------------------|
| `-z STRING`           | True if the string length is zero (empty).                    | `[ -z "$var" ]`      |
| `-n STRING`           | True if the string length is non-zero.                        | `[ -n "$var" ]`      |
| `STRING1 = STRING2`   | True if the strings are equal.                                | `[ "$a" = "$b" ]`    |
| `STRING1 != STRING2`  | True if the strings are not equal.                            | `[ "$a" != "$b" ]`   |
| `STRING1 < STRING2`   | True if `STRING1` sorts before `STRING2` (lexicographically). | `[ "$a" \< "$b" ]`   |
| `STRING1 > STRING2`   | True if `STRING1` sorts after `STRING2` (lexicographically).  | `[ "$a" \> "$b" ]`   |

> **Note:** Inside `[ ]`, the `<` and `>` operators must be escaped (`\<`, `\>`) to prevent the shell from interpreting them as redirection. Inside `[[ ]]`, escaping is not required.

## Numeric Operators

| **Operator** | **Description**          | **Example**           |
|--------------|--------------------------|-----------------------|
| `-eq`        | Equal to                 | `[ "$x" -eq "$y" ]`   |
| `-ne`        | Not equal to             | `[ "$x" -ne "$y" ]`   |
| `-lt`        | Less than                | `[ "$x" -lt "$y" ]`   |
| `-le`        | Less than or equal to    | `[ "$x" -le "$y" ]`   |
| `-gt`        | Greater than             | `[ "$x" -gt "$y" ]`   |
| `-ge`        | Greater than or equal to | `[ "$x" -ge "$y" ]`   |

## Why Separate String and Numeric Operators?

Bash treats numbers and strings differently when comparing values. String operators compare characters based on their ASCII (lexicographic) order, while numeric operators compare actual integer values. Mixing them up can produce surprising results.

In the example below, the string operator `\<` compares character by character. The first character of `"10"` is `'1'` (ASCII 49) and the first character of `"2"` is `'2'` (ASCII 50). Since `49 < 50`, the string `"10"` sorts *before* `"2"`:

```bash
a="10"
b="2"

if [ "$a" \< "$b" ]; then
    echo "10 is less than 2"
fi
# Output: 10 is less than 2
# Lexicographically, '1' < '2', so the condition is true.
```

To compare numbers correctly, use the numeric operators instead:

```bash
a=10
b=2

if [ "$a" -lt "$b" ]; then
    echo "10 is less than 2"
else
    echo "10 is greater than 2"
fi
# Output: 10 is greater than 2
```

## File Operators

### Existence and Type

| **Operator** | **Description**                                        | **Example**                   |
|--------------|--------------------------------------------------------|-------------------------------|
| `-e FILE`    | True if the file exists.                               | `[ -e /etc/passwd ]`          |
| `-f FILE`    | True if the file exists and is a regular file.         | `[ -f myfile.txt ]`           |
| `-d FILE`    | True if the file exists and is a directory.            | `[ -d /tmp ]`                 |
| `-s FILE`    | True if the file exists and is not empty (size > 0).   | `[ -s data.log ]`             |
| `-L FILE`    | True if the file is a symbolic link.                   | `[ -L symlink ]`              |
| `-h FILE`    | True if the file is a symbolic link (same as `-L`).    | `[ -h symlink ]`              |

### Permissions

| **Operator** | **Description**                  | **Example**          |
|--------------|----------------------------------|----------------------|
| `-r FILE`    | True if the file is readable.    | `[ -r config.cfg ]`  |
| `-w FILE`    | True if the file is writable.    | `[ -w output.txt ]`  |
| `-x FILE`    | True if the file is executable.  | `[ -x script.sh ]`   |

### Special File Types

| **Operator** | **Description**                                 | **Example**                   |
|--------------|-------------------------------------------------|-------------------------------|
| `-b FILE`    | True if the file is a block special device.     | `[ -b /dev/sda ]`             |
| `-c FILE`    | True if the file is a character special device. | `[ -c /dev/tty ]`             |
| `-p FILE`    | True if the file is a named pipe (FIFO).        | `[ -p /tmp/mypipe ]`          |
| `-S FILE`    | True if the file is a socket.                   | `[ -S /var/run/docker.sock ]` |

### Ownership and Modification

| **Operator** | **Description**                                            | **Example**          |
|--------------|------------------------------------------------------------|----------------------|
| `-N FILE`    | True if the file was modified since it was last read.      | `[ -N myfile.txt ]`  |
| `-O FILE`    | True if the file is owned by the current user.             | `[ -O myfile.txt ]`  |
| `-G FILE`    | True if the file's group matches the current user's group. | `[ -G myfile.txt ]`  |

## Variable and Shell Tests

| **Operator** | **Description**                                                        | **Example**                                |
|--------------|------------------------------------------------------------------------|--------------------------------------------|
| `-t FD`      | True if file descriptor `FD` is open and refers to a terminal (POSIX). | `[ -t 0 ]` (checks if stdin is a terminal) |
| `-v VAR`     | True if the variable is set, even if empty (Bash 4.2+).               | `[[ -v PATH ]]`                            |
| `-R VAR`     | True if the variable is a name reference via `declare -n` (Bash 4.4+).| `[[ -R refvar ]]`                          |

> **Note:** `-t` is POSIX-standard. `-v` and `-R` are Bash-specific extensions and are **not** POSIX-compliant.

---

[← Previous: Test Command](19_test_command.md) | [Next: Bash Operators →](21_bash_operators.md)
