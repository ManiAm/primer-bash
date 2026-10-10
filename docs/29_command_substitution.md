# Command Substitution

Command substitution allows you to capture the output of a command and use it as part of another command or assign it to a variable.

## Syntax

There are two syntax forms for command substitution:

| Syntax          | Form               |
|-----------------|--------------------|
| `$(command)`    | Modern (preferred) |
| `` `command` `` | Legacy (backticks) |

```bash
result=$(command)

result=`command`
```

The `$()` syntax is preferred because it is easier to read and supports clean nesting. Backticks require escaping for nested substitutions, which quickly becomes hard to follow:

```bash
# Nested substitution — backtick syntax (harder to read)
result=`echo \`date\``

# Nested substitution — $() syntax (cleaner)
result=$(echo $(date))
```

## Examples

### Assign Output to a Variable

```bash
current_date=$(date)
echo "Today's date is: $current_date"
```

### Use Output Inline

The substitution is evaluated first, and its result is embedded directly into the command:

```bash
tar -czf backup-$(date +%Y-%m-%d).tar.gz /path/to/files
```

### Use Output as an Argument

```bash
echo "The number of files is: $(ls | wc -l)"
```

### Iterate Over Output

```bash
files=$(ls /var/log)

for file in $files; do
    echo "Processing: $file"
done
```

### Nested Substitution

```bash
echo "Current user is: $(whoami), home directory is: $(echo $HOME)"
```

## Handling `stderr`

Command substitution captures only `stdout`. Error messages (`stderr`) are **not** captured — they are still printed to the terminal.

```bash
result=$(ls invalid_directory)
echo "Result: $result"
# "Result:" is empty; the error message was printed separately
```

To capture both `stdout` and `stderr`, redirect `stderr` into `stdout` (for more on redirection, see [Redirection](31_redirection.md)):

```bash
result=$(ls invalid_directory 2>&1)
echo "Result: $result"
```

To suppress `stderr` entirely:

```bash
result=$(ls invalid_directory 2>/dev/null)
echo "Result: $result"
```

## Checking the Exit Status

Command substitution preserves the exit status of the substituted command in `$?`. It is good practice to check it before using the result:

```bash
result=$(ls invalid_directory 2>/dev/null)
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "Command failed with exit code: $exit_code"
else
    echo "Command succeeded"
    echo "Result: $result"
fi
```

> `$?` is updated after **every** command. Saving it to a variable immediately ensures the original exit code is not lost. See [Exit Status](27_exit_status.md) for a detailed explanation.

---

[← Previous: Command Execution](28_command_execution.md) | [Next: Command Chaining →](30_command_chaining.md)
