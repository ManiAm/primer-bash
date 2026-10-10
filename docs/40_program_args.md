# Command-Line Arguments

Command-line arguments are values provided after a script's name when it is executed. They allow you to pass input into a script without hardcoding values, making scripts flexible and reusable.

```bash
./script.sh arg1 arg2 arg3
```

Arguments are separated by spaces. Inside the script, Bash provides special variables to access them.

## Positional Parameters

Positional parameters are numbered variables that hold the arguments passed to a script:

| Parameter            | Description                                      |
|----------------------|--------------------------------------------------|
| `$0`                 | The name of the script (or command) itself.      |
| `$1`, `$2`, `$3` …   | The first, second, third argument, and so on.    |

Consider the following script saved as `example.sh`:

```bash
#!/bin/bash

echo "Script Name: $0"
echo "First Argument: $1"
echo "Second Argument: $2"
echo "Third Argument: $3"
```

Invoking the script:

```bash
./example.sh arg1 arg2 arg3
```

Output:

```
Script Name: ./example.sh
First Argument: arg1
Second Argument: arg2
Third Argument: arg3
```

## Special Variables for Arguments

Bash provides several special variables that are useful when working with command-line arguments:

| Variable | Description                                                                        |
|----------|------------------------------------------------------------------------------------|
| `$#`     | The number of positional arguments (does not count `$0`).                          |
| `$@`     | All positional arguments as separate strings (preserves quoting per argument).     |
| `$*`     | All positional arguments joined into a single string, separated by the first character of `IFS`. |

> For the full list of special variables, see [Special Variables](14_special_variables.md).

### `$@` vs `$*`

When unquoted, `$@` and `$*` behave identically. The difference matters when they are **double-quoted**:

- `"$@"` expands each argument as a **separate word** — preserving the original argument boundaries.
- `"$*"` joins all arguments into a **single word**, separated by the first character of `IFS` (a space by default).

The clearest way to see the difference is to loop over each and pass arguments that contain spaces:

```bash
#!/bin/bash

echo '--- Using "$@" ---'
for arg in "$@"; do
    echo "  [$arg]"
done

echo '--- Using "$*" ---'
for arg in "$*"; do
    echo "  [$arg]"
done
```

Invoking the script with two arguments (each containing a space):

```bash
./example.sh "hello world" "foo bar"
```

Output:

```
--- Using "$@" ---
  [hello world]
  [foo bar]

--- Using "$*" ---
  [hello world foo bar]
```

In summary:
- With `"$@"`, the loop runs **twice** — once per original argument.
- With `"$*"`, the loop runs **once** because all arguments are merged into a single string.

> **Tip:** Always prefer `"$@"` when passing or iterating over arguments. It preserves each argument exactly as it was provided, including any spaces within them.

## `shift` Command

The `shift` command removes positional parameters from the left, shifting the remaining ones down by a specified count.

```bash
shift [n]
```

- `n` — the number of positions to shift (default is `1`).
- After shifting, `$1` takes the value that was in `$2`, `$2` takes the value from `$3`, and so on.
- Parameters that are shifted out are discarded, and `$#` decreases accordingly.
- `$0` (the script name) is never affected by `shift`.

```bash
#!/bin/bash

echo "Before shift: '$1' '$2' '$3'"
echo "Argument count: $#"

shift

echo "After shift:  '$1' '$2' '$3'"
echo "Argument count: $#"
```

Invoking the script:

```bash
./script.sh apple banana cherry
```

Output:

```
Before shift: 'apple' 'banana' 'cherry'
Argument count: 3
After shift:  'banana' 'cherry' ''
Argument count: 2
```

After `shift`, `apple` is discarded, `banana` moves to `$1`, `cherry` moves to `$2`, `$3` becomes empty, and `$#` drops from 3 to 2.

## Looping Through All Arguments

### Using `for` with `"$@"`

The simplest way to iterate over all arguments is a `for` loop with `"$@"`:

```bash
#!/bin/bash

for arg in "$@"; do
    echo "$arg"
done
```

### Using `while` with `shift`

Alternatively, use a `while` loop that processes `$1` and removes it with `shift` on each iteration. The loop continues until no arguments remain:

```bash
#!/bin/bash

while [ $# -gt 0 ]; do
    echo "Argument: $1"
    shift
done
```

Both approaches produce the same result. The `for` loop is more concise, while the `while`/`shift` pattern is useful when you need to consume arguments selectively (e.g., parsing flags and their values).

---

[← Previous: Shell Options](39_shell_options.md) | [Next: Program Options →](41_program_options.md)
