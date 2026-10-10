# Shell Variables

In Bash, variables store data that can be referenced and manipulated throughout a script or command-line session. A variable is essentially a named placeholder for information such as strings, numbers, or command output.

The following line defines a variable named `VAR_NAME` and assigns it a value:

```bash
VAR_NAME="Hello"
```

There must be no spaces around the `=` sign:

```bash
VAR_NAME = "Hello"    # Syntax error
```

## Variable Names

Variable names are case-sensitive in Bash:

```bash
VAR="hello"
var="world"

echo $VAR  # Output: hello
echo $var  # Output: world
```

Here, `VAR` and `var` are two distinct variables.

**Naming rules:**

- Names can contain letters, numbers, and underscores (`_`).
- Names must start with a letter or an underscore — not a number.
- Special characters such as `-`, `@`, `$`, `!`, `*`, `#`, `&`, `=`, and `?` cannot be used in variable names.

Examples of invalid variable names:

```bash
# Starting with a number
1var="Hello"

# Containing special characters
var-name="Hello"
var@name="Hello"
var$name="Hello"

# Containing a space
var name="Hello"

# Using reserved characters
var*name="Hello"
var#name="Hello"
```

> **Note:** Bash keywords such as `for`, `if`, and `while` can technically be used as variable names in simple assignments (e.g., `for="Hello"` is valid syntax). However, doing so is strongly discouraged because it creates confusing, hard-to-maintain code.

## Referring to Variables

To retrieve a variable's value, prefix its name with a dollar sign (`$`):

```bash
name="Alice"
echo $name  # Output: Alice
```

Variables are expanded inside double-quoted strings but not inside single-quoted strings:

```bash
name="Bob"
echo "Hello, $name!"   # Output: Hello, Bob!
echo 'Hello, $name!'   # Output: Hello, $name! (no variable expansion)
```

## Concatenation

To concatenate a variable with adjacent text, use curly braces `{}` to delimit the variable name:

```bash
fruit="apple"
echo "I like ${fruit}s"  # Output: I like apples
```

Without curly braces, Bash looks for a variable named `fruits`, which does not exist:

```bash
fruit="apple"
echo "I like $fruits"  # Output: I like
```

To append text to an existing variable:

```bash
STR="first string"
STR=${STR}:end
echo $STR  # Output: first string:end
```

To prepend text to an existing variable:

```bash
STR="first string"
STR=start:${STR}
echo $STR  # Output: start:first string
```

## Default Type

In Bash, all variables are treated as strings by default. Consider the following example:

```bash
num=10
num=num+5
echo $num  # Output: num+5
```

The value `10` is stored as a string. The second assignment does not perform arithmetic — Bash treats `num+5` as a literal string.

## Performing Arithmetic

Bash provides several ways to perform arithmetic:

- Arithmetic expansion: `$(( ))`
- Arithmetic evaluation: `(( ))`
- The `let` command
- The `expr` command

**Using `$(( ))`**

Arithmetic expansion evaluates an expression and returns the result:

```bash
num=10
num=$((num + 5))   # Not to be confused with command substitution: $( ... )
echo $num          # Output: 15
```

**Using `(( ))`**

Arithmetic evaluation performs calculations without the `$` prefix:

```bash
num=10
((num = num + 5))
echo $num  # Output: 15
```

**Using `let`**

The `let` command evaluates arithmetic expressions:

```bash
num=10
let num=num+5
echo $num  # Output: 15
```

**Using `expr`**

The `expr` command is an external utility. Operators and operands must be separated by spaces:

```bash
num=10
num=$(expr $num + 5)
echo $num  # Output: 15
```

## Floating-Point Arithmetic

Bash does not natively support floating-point arithmetic. For decimal calculations, use external tools such as `bc` or `awk`:

```bash
num1=3.5
num2=1.2
result=$(echo "$num1 + $num2" | bc)
echo $result  # Output: 4.7
```

## Integer Variables

You can explicitly declare a variable as an integer using `declare -i`. Bash then performs arithmetic on assignments automatically:

```bash
declare -i num=10
num=num+5
echo $num  # Output: 15
```

Assigning a non-numeric value to an integer variable sets it to `0`:

```bash
declare -i num
num="abc"
echo $num  # Output: 0
```

If the assigned string begins with digits, Bash uses the numeric prefix and ignores the rest:

```bash
declare -i num
num="123abc"
echo $num  # Output: 123
```

## Undefined Variables

An undefined variable is one that has never been assigned a value. Referencing it expands to an empty string:

```bash
echo "$undefined_var"  # Output: (nothing)
```

You can test whether a variable is defined using the `-v` test (Bash 4.2+):

```bash
if [ -v undefined_var ]; then
    echo "Variable exists"
else
    echo "Variable is undefined"  # This will print
fi
```

## Using `unset`

The `unset` command removes a variable, making it undefined:

```bash
myvar="hello"
echo $myvar  # Output: hello

unset myvar
echo $myvar  # Output: (nothing)
```

`unset` does not produce an error if the variable does not exist:

```bash
unset nonexistent_var  # No error
```

## Empty Variables

A variable can be explicitly defined with an empty value:

```bash
var=
echo "$var"  # Output: (nothing)
```

This is useful when you need to ensure a variable exists but has no initial value.

You can test for an empty (or undefined) variable using `-z`:

```bash
var=

if [ -z "$var" ]; then
    echo "Variable is empty or undefined"
else
    echo "Variable is not empty"
fi
```

## Readonly Variables

A readonly variable cannot be changed or unset after it has been declared. It is used to define constants that must remain fixed throughout a script's execution.

To declare a readonly variable:

```bash
readonly VAR_NAME=value
```

Alternatively, use the `declare` command:

```bash
declare -r VAR_NAME=value
```

Attempting to modify a readonly variable produces an error:

```bash
#!/bin/bash

readonly PI=3.14159
echo "The value of PI is $PI"

PI=3.14  # Error: PI: readonly variable
```

## Types of Shell Variables

Everything discussed so far — defining, naming, referencing, and modifying variables — applies to **local shell variables**: variables that exist only in the current shell session and are not visible to child processes.

However, Bash supports several other types of variables as well, each with a different scope and purpose:

| **Type**                    | **Example**               | **Description**                        |
|-----------------------------|---------------------------|----------------------------------------|
| **Local shell variable**    | `MY_VAR="Hello!"`         | Exists only in the current shell.      |
| **Environment variable**    | `export ENV_VAR="World!"` | Passed to child processes (inherited). |
| **Built-in shell variable** | `$BASH_VERSION`           | Managed by Bash internally.            |
| **Special shell variable**  | `$?`, `$$`, `$!`, `$@`   | Represent shell state or metadata.     |

- A **local** variable is defined in the current shell session. It is not passed to child processes or subshells.
- An **environment** variable is exported to child processes and subshells using the `export` command.
- A **built-in** variable is predefined by the shell to store information about its own state or behavior.
- A **special** variable is a reserved, read-only variable that the shell maintains automatically. It may be referenced but not assigned to.

> Each type is covered in its own section: [Environment Variables](10_env_variables.md), [Built-in Shell Variables](13_built_in_variables.md), and [Special Variables](14_special_variables.md).

To display all shell variables and functions:

    declare

The `-p` flag displays variable declarations along with their attributes and values:

    declare -p

To display only environment variables:

    printenv

---

[← Previous: Shell Script](08_shell_script.md) | [Next: Env Variables →](10_env_variables.md)
