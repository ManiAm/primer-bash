# Globbing (Filename Expansion)

Globbing is the shell's way of matching filenames and paths using special wildcard characters. Instead of typing every filename by hand, you write a short pattern and let Bash find the files that match.

> **Note:** Globbing patterns are **not** regular expressions. They follow simpler rules and are used exclusively for matching filenames.

## Wildcard Patterns

| Pattern   | Description                                             | Example           | Matches                                     |
|-----------|---------------------------------------------------------|-------------------|---------------------------------------------|
| `*`       | Match zero or more characters.                          | `*.txt`           | `notes.txt`, `a.txt`                        |
| `?`       | Match exactly **one** character.                        | `file?.txt`       | `file1.txt`, `fileA.txt` (not `file10.txt`) |
| `[...]`   | Match any **one** character listed inside the brackets. | `file[123].txt`   | `file1.txt`, `file2.txt`, `file3.txt`       |
| `[!...]`  | Match any **one** character **not** listed.             | `file[!3].txt`    | `file1.txt`, `file2.txt` (not `file3.txt`)  |

A range can be used inside brackets: `[a-z]` matches any lowercase letter, `[0-9]` matches any digit.

```bash
ls *              # List all non-hidden files
ls *.txt          # List all files ending in .txt
ls file?.txt      # Match file1.txt, fileA.txt, etc.
ls file[1-4].txt  # Match file1.txt through file4.txt
ls file[!3].txt   # Match all single-character suffixes except 3
```

### Hidden Files

By default, `*` and `?` do **not** match files or directories that start with a dot (`.`). These are considered hidden files. To match them, use the `.*` pattern explicitly:

```bash
ls *    # Does NOT list .bashrc, .profile, etc.
ls .*   # Lists hidden files like .bashrc, .profile as well
```

## Unmatched Patterns

If no files match a glob pattern, Bash returns the **literal pattern** instead of an error:

```bash
echo inventory*   # Output: inventory*  (no matching files)
```

This is the default because it is the safest behavior — if the pattern silently expanded to nothing, commands like `rm *.tmp` could lose their arguments and behave unpredictably. Returning the literal string makes the mismatch visible and easy to debug.

To change this behavior, Bash provides two opt-in options:

```bash
shopt -s nullglob   # Unmatched patterns expand to an empty string
shopt -s failglob   # Unmatched patterns cause an immediate error
```

```bash
shopt -s nullglob
echo inventory*     # Output: (empty)
```

## Recursive Matching with globstar

By default, `*` only matches files in the current directory. To match files across all subdirectories, enable the `globstar` option and use `**`:

```bash
shopt -s globstar

ls **/*.txt   # List all .txt files in the current directory and every subdirectory
```

You can also iterate over all subdirectories:

```bash
shopt -s globstar

for dir in **/; do
    echo "Directory: $dir"
done
```

> **Tip:** Recursive matching can be slow on very large directory trees. For better performance and portability across different shells, consider using the `find` command instead.

## Preventing Globbing

Sometimes you want to use wildcard characters literally without Bash expanding them. There are three ways to do this.

### Escape Individual Characters

Place a backslash (`\`) before each wildcard character:

```bash
echo \*          # Output: *
echo file\?.txt  # Output: file?.txt
```

### Quote the String

Wrap the text in single or double quotes to prevent expansion:

```bash
echo '*'         # Output: *
echo "*.txt"     # Output: *.txt
```

### Disable Globbing Temporarily

Use `set -f` to turn off globbing and `set +f` to turn it back on:

```bash
set -f
echo *           # Output: *  (no expansion)
set +f
```

## Globbing with Variables

When a variable contains a glob pattern and is used **unquoted**, Bash expands the pattern at the time the variable is used:

```bash
pattern="*.txt"
echo $pattern    # Expands: lists matching .txt files
```

To prevent accidental expansion, **quote your variables** or use `set -f`:

```bash
pattern="*.txt"

echo "$pattern"  # No expansion: prints the literal string *.txt

set -f
echo $pattern    # Output: *.txt
set +f
```

---

[← Previous: Shell Expansions](17_shell_expansions.md) | [Next: Test Command →](19_test_command.md)
