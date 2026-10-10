# Test Command

The `test` command evaluates conditional expressions and returns an exit status indicating whether the condition is true or false. It is the foundation of decision-making in Bash scripts — used with `if` statements, loops, and other control structures.

```
test EXPRESSION
```

- Exit status `0` — the condition is **true**.
- Exit status `1` — the condition is **false**.

```bash
test 5 -gt 3      # Test if 5 is greater than 3
echo $?            # Output: 0 (true)

test 5 -lt 3      # Test if 5 is less than 3
echo $?            # Output: 1 (false)

test -f /etc/passwd
echo $?            # Output: 0 if the file exists
```

> **Note:** The specific operators used with `test` (such as `-gt`, `-f`, and `-z`) are covered in [Test Operators](20_test_operators.md).

## `[ ]` — Single Brackets

`[ ]` is a synonym for the `test` command. The opening bracket `[` is actually a command (just like `test`), and the closing bracket `]` is its required last argument.

It is POSIX-compliant and works in all POSIX-compatible shells (e.g., `sh`, `dash`, `bash`).

> **Important:** Spaces are required after `[` and before `]`, as well as around operators.

```bash
[ 5 -gt 3 ]        # Test if 5 is greater than 3
echo $?             # Output: 0 (true)

[ 5 -lt 3 ]        # Test if 5 is less than 3
echo $?             # Output: 1 (false)
```

## Limitations of `test` and `[ ]`

The `test` command and `[ ]` are simple and portable, but they have several limitations that can lead to errors. The sections below cover each one. All of these are resolved by `[[ ]]`, which is introduced afterward.

### Quoting Variables

Always quote variables that may contain spaces or special characters. Without quotes, Bash splits the value into multiple words before `test` sees it, causing unexpected errors:

```bash
a="hello world"
test "$a" = "hello"
echo $?              # Output: 1 (false — strings are not equal)
```

Without the quotes around `$a`, Bash would expand it to `test hello world = hello`, which has too many arguments and produces an error.

### Compound Expressions

The shell operators `&&` (AND) and `||` (OR) are interpreted by the shell **before** they reach the `test` command. This means they split the command into separate parts rather than combining conditions within a single `test`:

```bash
age=20
test $age -ge 18 && $age -le 65    # Wrong!
```

Here, `&&` terminates the `test` command after `-ge 18`. The shell then tries to execute `$age -le 65` (i.e., `20 -le 65`) as a standalone command, which fails.

**Workaround 1** — chain separate `test` (or `[ ]`) commands:

```bash
age=20
test $age -ge 18 && test $age -le 65
echo $?             # Output: 0 (true — both conditions met)
```

**Workaround 2** — use `-a` (AND) and `-o` (OR) inside `test`:

```bash
age=20
test $age -ge 18 -a $age -le 65
echo $?             # Output: 0 (true)
```

> **Note:** POSIX marks `-a` and `-o` as obsolescent. Prefer chaining separate `test` commands or using `[[ ]]` for compound conditions.

### No Pattern Matching

The `test` command and `[ ]` do **not** perform pattern matching. They treat all values as literal strings. This causes problems when a variable holds a glob pattern.

Consider a directory containing these files:

```
myfile.txt  myfile1.txt  myfile2.txt
```

The following script produces an error:

```bash
file="myfile.txt"
pattern="my*"

[ $file = $pattern ]
```

Because `$pattern` is unquoted, Bash performs globbing **before** `[ ]` runs. The pattern `my*` expands to all matching filenames, so the command becomes:

```
[ myfile.txt = myfile.txt myfile1.txt myfile2.txt ]
```

This has too many arguments for `[ ]`, so it produces an error.

Quoting the variable prevents glob expansion, but `[ ]` still compares the strings literally:

```bash
[ "$file" = "$pattern" ]
echo $?              # Output: 1 (false — literal "myfile.txt" ≠ literal "my*")
```

The error is gone, but the comparison fails because `[ ]` treats `my*` as the literal string `my*`, not as a wildcard pattern.

## `[[ ]]` — Double Brackets

`[[ ]]` is an enhanced test construct available in Bash (and a few other advanced shells like Zsh). It is generally preferred in Bash scripts because it resolves the limitations of `test` and `[ ]` described above.

> **Note:** `[[ ]]` is **not** POSIX-compliant. If portability across different shells is required, use `[ ]` instead.

### No Quoting Required for Variables

Unlike `[ ]`, `[[ ]]` does not perform word splitting on variables, so quoting is optional in most cases:

```bash
a="hello world"

[[ $a = "hello world" ]]
echo $?              # Output: 0 (true)

[[ $a = "hello" ]]
echo $?              # Output: 1 (false)
```

### Logical Operators Inside `[[ ]]`

`[[ ]]` supports `&&` and `||` directly within the expression:

```bash
age=20
[[ $age -ge 18 && $age -le 65 ]]
echo $?              # Output: 0 (true)
```

### Glob Pattern Matching

When the right-hand side of `=` is unquoted inside `[[ ]]`, it is treated as a glob pattern:

```bash
file="myfile.txt"
pattern="my*"

[[ $file = $pattern ]]
echo $?              # Output: 0 (true — "myfile.txt" matches the pattern "my*")
```

### Regex Matching with `=~`

`[[ ]]` also supports extended regular expressions using the `=~` operator:

```bash
a="hello"
[[ $a =~ ^h.*o$ ]]
echo $?              # Output: 0 (true — "hello" matches the regex)
```

---

[← Previous: Globbing](18_globbing.md) | [Next: Test Operators →](20_test_operators.md)
