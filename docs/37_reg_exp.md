# Regex in Bash

A regular expression (regex) is a pattern-matching syntax used to search, match, and manipulate strings based on specific patterns. It uses metacharacters (like `^`, `$`, `*`, `+`, `.`, etc.) to define flexible search rules.

> **Note:** Regex is different from globbing. Globbing is a simpler pattern-matching technique used only for file and directory name matching in shell commands (see [Globbing](18_globbing.md)). Regex, on the other hand, is used to match patterns within text content.

## BRE vs ERE

Basic Regular Expressions (BRE) and Extended Regular Expressions (ERE) are two regex flavors defined by the POSIX standard. They differ in how certain special characters are interpreted:

- **BRE** — Parentheses `()`, braces `{}`, and pipe `|` must be escaped with `\` to act as special operators (e.g., `\(group\)`, `\{2,3\}`, `a\|b`). Without the backslash, they are treated as literal characters. BRE is the default syntax for `grep` and `sed`.

- **ERE** — These same operators work directly without escaping (e.g., `(group)`, `{2,3}`, `a|b`). ERE is used by `grep -E`, `sed -E`, `awk`, and Bash's `[[ ... =~ ... ]]`.

## Bash Built-in Regex

Bash supports regex matching directly inside `[[ ]]` (see [`test` Command](19_test_command.md)) using the `=~` operator:

    [[ string =~ regex ]]

The string to test is always on the **left**, and the regex pattern is always on the **right**.

It returns:

- `0` (true) if the string matches the regex pattern.
- `1` (false) if no match is found.

Bash uses Extended Regular Expressions (ERE) for the `=~` operator.

> **Note:** Always double-quote variables on the left side to prevent word splitting:
>
>     [[ "$var" =~ pattern ]]
>
> Do **not** quote the regex pattern on the right side — quoting it turns the pattern into a literal string match.

### Literal Match

```bash
[[ "apple" =~ "apple" ]] && echo "Match!"   # Matches the exact string 'apple'
```

### Anchors — Start (`^`) and End (`$`)

Anchors ensure the pattern matches a specific position in the string. Use `^` to match the start and `$` to match the end. Combine both for an exact full-string match:

```bash
[[ "apple123" =~ ^apple ]]    && echo "Starts with 'apple'"
[[ "apple123" =~ 123$ ]]      && echo "Ends with '123'"
[[ "apple"    =~ ^apple$ ]]   && echo "Exact match: 'apple'"
```

### Dot (`.`) — Any Character

The dot matches any single character except a newline (`\n`):

```bash
[[ "a1b" =~ a.b ]]       && echo "Match!"   # '.' matches '1'
[[ "a1b2c3" =~ a.b.c. ]] && echo "Match!"   # Each '.' matches one character
```

To match a literal dot, escape it with a backslash:

```bash
[[ "file.txt" =~ file\.txt ]] && echo "Match!"   # Matches exact 'file.txt'
```

### Alternation (`|`)

Use `|` inside a group to match one of several alternatives:

```bash
[[ "orange" =~ ^(apple|banana|orange)$ ]] && echo "Fruit matched!"
```

### Character Classes

Character classes define a set of characters that can match at a given position:

```bash
[[ "apple" =~ [aeiou] ]]     && echo "Contains a vowel!"
```

Use a hyphen for ranges, and `^` inside brackets to negate:

```bash
[[ "abc123" =~ [a-z] ]]      && echo "Contains a lowercase letter!"
[[ "abc123" =~ [0-9] ]]      && echo "Contains a digit!"
[[ "123abc" =~ [^0-9] ]]     && echo "Contains a non-digit character!"
```

POSIX defines named character classes that work portably across locales. They must be used inside an additional set of brackets (e.g., `[[:digit:]]`):

| POSIX Class  | Equivalent Regex | Description              |
|--------------|------------------|--------------------------|
| `[:alnum:]`  | `[a-zA-Z0-9]`    | Alphanumeric characters  |
| `[:alpha:]`  | `[a-zA-Z]`       | Alphabetic characters    |
| `[:digit:]`  | `[0-9]`          | Digits (0–9)             |
| `[:lower:]`  | `[a-z]`          | Lowercase letters        |
| `[:upper:]`  | `[A-Z]`          | Uppercase letters        |
| `[:space:]`  | `[ \t\r\n\f\v]`  | Whitespace characters    |
| `[:punct:]`  | `[!"#$%&'()*]`   | Punctuation symbols      |
| `[:xdigit:]` | `[0-9a-fA-F]`    | Hexadecimal digits       |

```bash
[[ "hello world" =~ [[:space:]] ]] && echo "Contains whitespace!"
```

### Quantifiers

Quantifiers control how many times the preceding element must occur:

| Quantifier | Meaning               |
|------------|-----------------------|
| `*`        | Zero or more times    |
| `+`        | One or more times     |
| `?`        | Zero or one time      |
| `{n}`      | Exactly n times       |
| `{n,m}`    | Between n and m times |

```bash
[[ "aabbcc" =~ a+b+c+ ]]  && echo "Matched!"   # One or more of each
[[ "ab" =~ a{1,2}b ]]      && echo "Matched!"   # 'a' appears 1 or 2 times
[[ "abc" =~ a.*c ]]        && echo "Matched!"   # 'a', then 0+ characters, then 'c'
```

### Groups and Captures (`BASH_REMATCH`)

Parentheses `()` create capture groups. When a `=~` match succeeds, Bash stores the results in the `BASH_REMATCH` array:

- `BASH_REMATCH[0]` — The entire matched string.
- `BASH_REMATCH[1]` — The first captured group.
- `BASH_REMATCH[2]` — The second captured group, and so on.

```bash
if [[ "hello123" =~ ^([a-z]+)([0-9]+)$ ]]; then
    echo "Full match: ${BASH_REMATCH[0]}"   # hello123
    echo "Text: ${BASH_REMATCH[1]}"          # hello
    echo "Number: ${BASH_REMATCH[2]}"        # 123
fi
```

### Practical Example — File Extension Validation

Combining several regex features to validate a filename:

```bash
if [[ "document.pdf" =~ ^.+\.(pdf|doc|txt)$ ]]; then
    echo "Valid file: extension is '${BASH_REMATCH[1]}'"
fi
```

---

[← Previous: Process Substitution](36_process_substition.md) | [Next: Trap →](38_trap.md)
