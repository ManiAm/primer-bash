# Bash Operators

Bash supports several categories of operators for assignments, arithmetic, logic, testing, and redirection. This page provides a compact overview of each category.

## Assignment Operators

The basic assignment operator `=` sets a variable to a value. There must be **no spaces** around the `=` sign.

```bash
name="Alice"
count=10
```

### String Append with `+=`

Outside of an arithmetic context, `+=` **appends** to a string — it does not perform addition:

```bash
greeting="Hello"
greeting+=", World"
echo "$greeting"       # Output: Hello, World
```

### Arithmetic Compound Assignment

Inside `(( ))`, Bash supports the standard compound assignment operators:

| **Operator** | **Description**            | **Example**                          |
|--------------|----------------------------|--------------------------------------|
| `+=`         | Add and assign             | `(( count += 5 ))`  — adds 5        |
| `-=`         | Subtract and assign        | `(( count -= 3 ))`  — subtracts 3   |
| `*=`         | Multiply and assign        | `(( count *= 2 ))`  — multiplies    |
| `/=`         | Divide and assign          | `(( count /= 4 ))`  — divides       |
| `%=`         | Modulus and assign         | `(( count %= 3 ))`  — remainder     |

```bash
count=10
(( count += 5 ))
echo "$count"          # Output: 15
```

> **Note:** `declare -i` makes a variable integer-typed, which causes `+=` to perform arithmetic even without `(( ))`. However, using `(( ))` is clearer and preferred.

## Arithmetic Operators

Bash performs integer arithmetic inside `$(( ))` (arithmetic expansion) or `(( ))` (arithmetic evaluation).

| **Operator** | **Description**     | **Example**              |
|--------------|---------------------|--------------------------|
| `+`          | Addition            | `echo $(( 2 + 3 ))` → 5 |
| `-`          | Subtraction         | `echo $(( 5 - 3 ))` → 2 |
| `*`          | Multiplication      | `echo $(( 4 * 2 ))` → 8 |
| `/`          | Integer division    | `echo $(( 8 / 3 ))` → 2 |
| `%`          | Modulus (remainder)  | `echo $(( 5 % 2 ))` → 1 |
| `**`         | Exponentiation      | `echo $(( 2 ** 3 ))` → 8 |

> **Note:** Bash arithmetic is **integer-only**. Division truncates toward zero (e.g., `8 / 3` gives `2`, not `2.666`). For floating-point math, use external tools like `bc` or `awk`.

## Logical Operators

Logical operators control the flow of execution based on success or failure of commands.

| **Operator** | **Description** | **Example**                          |
|--------------|-----------------|--------------------------------------|
| `&&`         | Logical AND     | `[ 2 -eq 2 ] && echo "True"`         |
| `\|\|`       | Logical OR      | `[ 2 -ne 2 ] \|\| echo "Fallback"`   |
| `!`          | Logical NOT     | `! [ -f missing ] && echo "No file"` |

- `&&` — run the next command **only if** the previous one succeeds (exit status `0`).
- `||` — run the next command **only if** the previous one fails (non-zero exit status).
- `!` — negate the exit status of the following command.

> **See also:** [Command Chaining](30_command_chaining.md) covers `&&`, `||`, `;`, and pipelines in detail.

## Test Operators

Test operators are used with `test`, `[ ]`, and `[[ ]]` to compare strings, compare numbers, and check file attributes. They are covered in their own dedicated pages:

- [Test Command](19_test_command.md) — syntax and usage of `test`, `[ ]`, and `[[ ]]`.
- [Test Operators](20_test_operators.md) — complete reference for string, numeric, and file test operators.

## Redirection Operators

Redirection operators control where a command's input comes from and where its output goes.

| **Operator** | **Description**                     | **Example**                    |
|--------------|-------------------------------------|--------------------------------|
| `>`          | Redirect stdout (overwrite)         | `echo "Hello" > file.txt`     |
| `>>`         | Redirect stdout (append)            | `echo "World" >> file.txt`    |
| `2>`         | Redirect stderr                     | `command 2> error.log`        |
| `&>`         | Redirect both stdout and stderr     | `command &> output.log`       |
| `<`          | Redirect stdin from a file          | `wc -l < file.txt`            |
| `<<<`        | Here-string (stdin from a string)   | `grep foo <<< "$text"`        |

> **Note:** `&>` is a Bash extension. The POSIX-portable equivalent is `command >file 2>&1`.

> **See also:** [Redirection](31_redirection.md) covers all redirection forms in detail, including here-documents, file descriptor manipulation, and `noclobber`.

## Ternary Operator

Bash does not have a general-purpose ternary operator, but inside `(( ))` you can use the C-style conditional expression for **arithmetic** values:

```
result=$(( condition ? value_if_true : value_if_false ))
```

The `condition` is evaluated as an arithmetic expression — zero means false, non-zero means true.

```bash
a=10
b=5
max=$(( a > b ? a : b ))
echo "Max is $max"     # Output: Max is 10
```

> **Note:** This only works with integer arithmetic. For string-based conditional logic, use `if…else` statements (see [Conditional Statements](22_conditional.md)).

---

[← Previous: Test Operators](20_test_operators.md) | [Next: Conditional Statements →](22_conditional.md)
