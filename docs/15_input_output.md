# Input and Output

Bash provides several built-in commands for printing output and reading input: `echo`, `printf`, and `read`.

## echo

`echo` is a built-in Bash command used to print text or variables to the terminal. It is commonly used to display messages, debug scripts, and provide output to the user.

Basic usage:

```bash
echo "Hello, World!"
```

To print a variable:

```bash
greeting="Hello"
echo $greeting
```

Using a variable inside a string:

```bash
greeting="Hello"
echo "$greeting, World!"
```

It is a good practice to use curly braces `{}` around the variable name to avoid ambiguity:

```bash
greeting="Hello"
echo "${greeting}, World!"
```

### Double vs. Single Quotes

Double quotes (`"`) allow variable expansion. Single quotes (`'`) treat everything as a literal string.

```bash
name="Alice"
echo "Hello, $name!"  # Output: Hello, Alice!
echo 'Hello, $name!'  # Output: Hello, $name!
```

### Suppressing the Trailing Newline

By default, `echo` adds a newline at the end of its output. To suppress it, use the `-n` option:

```bash
echo -n "Hello"
echo ", World!"  # Output: Hello, World!
```

### Escape Sequences

Special characters like `\n` (newline) and `\t` (tab) are not interpreted by `echo` by default. Use the `-e` option to enable them:

```bash
echo "Line1\nLine2"  # Output: Line1\nLine2

echo -e "Line1\nLine2"
# Output:
# Line1
# Line2

echo -e "Tabbed\tText"  # Output: Tabbed    Text

echo -e "\e[31mThis text is red\e[0m"  # ANSI escape code for red text
```

## printf

`printf` provides formatted output and is more consistent and portable than `echo`. It is modeled after the C language's `printf` function.

Unlike `echo`, `printf` does **not** add a trailing newline automatically — you must include `\n` explicitly:

```bash
printf "This is printf\n"
# Output:
# This is printf

printf "Name: %s\nAge: %d\n" "Alice" 25
# Output:
# Name: Alice
# Age: 25
```

### Format Placeholders

`printf` uses placeholders (format specifiers) to control how values are formatted in the output:

| Placeholder | Description                             | Example                        | Output           |
|-------------|-----------------------------------------|--------------------------------|------------------|
| **`%s`**    | String                                  | `printf "%s\n" "Hello"`        | Hello            |
| **`%d`**    | Integer (signed)                        | `printf "%d\n" 123`            | 123              |
| **`%i`**    | Integer (same as `%d`)                  | `printf "%i\n" -123`           | -123             |
| **`%u`**    | Unsigned integer                        | `printf "%u\n" 123`            | 123              |
| **`%f`**    | Floating-point number                   | `printf "%f\n" 123.456`        | 123.456000       |
| **`%.2f`**  | Floating-point with 2 decimal places    | `printf "%.2f\n" 123.456`      | 123.46           |
| **`%x`**    | Hexadecimal (lowercase)                 | `printf "%x\n" 255`            | ff               |
| **`%X`**    | Hexadecimal (uppercase)                 | `printf "%X\n" 255`            | FF               |
| **`%o`**    | Octal number                            | `printf "%o\n" 10`             | 12               |
| **`%c`**    | First character of the argument         | `printf "%c\n" "A"`            | A                |
| **`%%`**    | Literal `%` symbol                      | `printf "%%\n"`                | %                |

## read

The `read` command reads a line of input from standard input (e.g., the keyboard) or from a file and stores it into one or more variables.

### Commonly Used Options

| Option | Description                                                           |
|--------|-----------------------------------------------------------------------|
| `-p`   | Display a prompt message before reading input.                        |
| `-s`   | Silent mode — input is not echoed to the terminal (useful for passwords). |
| `-r`   | Raw mode — disables backslash escaping so `\n`, `\\`, etc. are read literally. |
| `-a`   | Read input into an indexed array instead of a single variable.        |

### Reading User Input

Prompt the user and store the response in a variable:

```bash
echo "Enter your name:"
read name
echo "Hello, $name!"
```

Using `-p` to combine the prompt and `read` in one command:

```bash
read -p "Enter your age: " age
echo "You are $age years old."
```

Using `-s` to hide sensitive input:

```bash
read -s -p "Enter your password: " password
echo -e "\nPassword entered."
```

Reading multiple values into separate variables:

```bash
echo "Enter your first and last name:"
read first_name last_name
echo "Hello, $first_name $last_name!"
```

### Reading from Files

When reading from files or strings, the input may contain literal backslashes (e.g., file paths, regex patterns). Use `-r` (raw mode) to prevent `read` from interpreting them as escape characters.

Read a file line by line using a `while` loop with input redirection:

```bash
while read -r line; do
  echo "Line: $line"
done < file.txt
```

`IFS` (Internal Field Separator) controls how input is split into fields (see [IFS](13_built_in_variables.md#ifs-internal-field-separator) for a full explanation). You can set it inline with `read` to parse delimited data like CSV without affecting the rest of the script:

```bash
while IFS=',' read -r col1 col2; do
    echo "Column 1: $col1, Column 2: $col2"
done < data.csv
```

### Splitting a String with Here-Strings

A **here-string** (`<<<`) feeds a string directly to a command's standard input. Combined with `read`, it is a convenient way to split a string into variables:

```bash
read -r name age <<< "Alice 30"
echo "Name: $name"   # Output: Name: Alice
echo "Age: $age"     # Output: Age: 30
```

To split on a custom delimiter, set `IFS` inline:

```bash
IFS=',' read -r name age <<< "Alice,30"
echo "Name: $name"   # Output: Name: Alice
echo "Age: $age"     # Output: Age: 30
```

Use `-a` to read words into an array:

```bash
read -r -a fruits <<< "apple banana cherry"

echo "${fruits[@]}"   # Output: apple banana cherry
echo "${fruits[0]}"   # Output: apple
echo "${fruits[1]}"   # Output: banana
echo "${fruits[2]}"   # Output: cherry
```

---

[← Previous: Special Variables](14_special_variables.md) | [Next: File & Directory Ops →](16_file_dir.md)
