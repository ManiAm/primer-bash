# Shell Expansions

Shell expansion is the process by which Bash interprets and transforms special symbols, patterns, or variables in a command **before** executing it. This allows you to dynamically generate text, compute values, and manipulate strings — all within the shell.

Bash performs the following types of expansion (each covered below unless noted):

- Brace expansion
- Tilde expansion
- Arithmetic expansion
- Parameter expansion
- Filename expansion (globbing) — covered separately in [Globbing (Filename Expansion)](18_globbing.md)

## Brace Expansion

Brace expansion generates a set or sequence of strings. The shell expands the braces **before** any other expansion takes place.

```bash
echo {A,B,C}       # Output: A B C
echo {1..5}        # Output: 1 2 3 4 5
echo {a..c}{1..3}  # Output: a1 a2 a3 b1 b2 b3 c1 c2 c3

ls {file1,file2,file3}.txt  # Expands to: file1.txt file2.txt file3.txt
```

## Tilde Expansion

The tilde (`~`) is expanded to home directory paths.

```bash
echo ~        # Output: /home/username  (your home directory)
echo ~user1   # Output: /home/user1     (user1's home directory)
echo ~/docs   # Output: /home/username/docs
```

## Arithmetic Expansion

The `$(( ))` syntax evaluates arithmetic expressions and returns the result.

```bash
echo $((3 + 5))      # Output: 8

x=10
echo $((x * 2))      # Output: 20

echo $((10 / 3))     # Output: 3 (integer division)
echo $((10 % 3))     # Output: 1 (remainder)
```

## Parameter Expansion

Parameter expansion is a mechanism that lets you retrieve and manipulate the value of variables at runtime. It uses the `${ }` syntax and supports a wide range of operations.

### Default and Alternative Values

These forms let you provide fallback values or enforce that a variable is set.

| Syntax                  | Description                                            | Example                                  | Output                   |
|-------------------------|--------------------------------------------------------|------------------------------------------|--------------------------|
| `${var:-default}`       | Use `default` if `$var` is **unset or empty**.         | `name=""` <br> `echo ${name:-John}`      | `John`                   |
| `${var:=default}`       | **Assign** `default` to `$var` if unset or empty.      | `unset name` <br> `echo ${name:=John}`   | `John` (name is now set) |
| `${var:+value}`         | Use `value` only if `$var` is **set and non-empty**.   | `name="Alice"` <br> `echo ${name:+Found}`| `Found`                  |
| `${var:?error}`         | Print `error` and exit if `$var` is unset or empty.    | `echo ${name:?Name is missing}`          | Error: Name is missing   |

### Length Calculation

| Syntax            | Description                          | Example                          | Output     |
|-------------------|--------------------------------------|----------------------------------|------------|
| `${#var}`         | Get the **length** of the value.     | `var="hello"` <br> `echo ${#var}`| `5`        |

### Substring Extraction

| Syntax                      | Description                                            | Example                                      | Output     |
|-----------------------------|--------------------------------------------------------|----------------------------------------------|------------|
| `${var:offset}`             | Extract from **offset** to the end.                    | `var="hello world"` <br> `echo ${var:6}`     | `world`    |
| `${var:offset:length}`      | Extract **length** characters starting at **offset**.  | `var="hello world"` <br> `echo ${var:0:5}`   | `hello`    |

### String Removal (Prefix)

Remove a pattern from the **beginning** of a string.

| Syntax                  | Description                                                        | Example                                       | Output              |
|-------------------------|--------------------------------------------------------------------|-----------------------------------------------|---------------------|
| `${var#pattern}`        | Remove the **shortest** prefix match.                              | `var="hello.world.txt"` <br> `echo ${var#*.}` | `world.txt`         |
| `${var##pattern}`       | Remove the **longest** prefix match.                               | `var="hello.world.txt"` <br> `echo ${var##*.}`| `txt`               |

### String Removal (Suffix)

Remove a pattern from the **end** of a string.

| Syntax                  | Description                                                        | Example                                       | Output              |
|-------------------------|--------------------------------------------------------------------|-----------------------------------------------|---------------------|
| `${var%pattern}`        | Remove the **shortest** suffix match.                              | `var="hello.world.txt"` <br> `echo ${var%.*}` | `hello.world`       |
| `${var%%pattern}`       | Remove the **longest** suffix match.                               | `var="hello.world.txt"` <br> `echo ${var%%.*}`| `hello`             |

### String Replacement

| Syntax                            | Description                                                   | Example                                              | Output              |
|-----------------------------------|---------------------------------------------------------------|------------------------------------------------------|---------------------|
| `${var/pattern/replacement}`      | Replace the **first** match.                                  | `var="apple apple"` <br> `echo ${var/apple/grape}`   | `grape apple`       |
| `${var//pattern/replacement}`     | Replace **all** matches.                                      | `var="apple apple"` <br> `echo ${var//apple/grape}`  | `grape grape`       |
| `${var/#pattern/replacement}`     | Replace only if the pattern matches at the **start**.         | `var="apple orange"` <br> `echo ${var/#apple/grape}` | `grape orange`      |
| `${var/%pattern/replacement}`     | Replace only if the pattern matches at the **end**.           | `var="apple orange"` <br> `echo ${var/%orange/grape}`| `apple grape`       |

### Case Modification

| Syntax                   | Description                                    | Example                                | Output           |
|--------------------------|-------------------------------------------------|----------------------------------------|------------------|
| `${var^}`                | Capitalize the **first** character.             | `var="hello"` <br> `echo ${var^}`      | `Hello`          |
| `${var^^}`               | Convert **all** characters to uppercase.        | `var="hello"` <br> `echo ${var^^}`     | `HELLO`          |
| `${var,}`                | Lowercase the **first** character.              | `var="HELLO"` <br> `echo ${var,}`      | `hELLO`          |
| `${var,,}`               | Convert **all** characters to lowercase.        | `var="HELLO"` <br> `echo ${var,,}`     | `hello`          |

---

[← Previous: File & Directory Ops](16_file_dir.md) | [Next: Globbing →](18_globbing.md)
