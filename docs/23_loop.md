# Loops

Bash provides three looping constructs: `for`, `while`, and `until`. Each repeats a block of commands, but they differ in how they decide when to stop.

## for loop

A `for` loop iterates over a list of items, executing a block of commands once for each item.

```bash
for var in list; do
    # Commands to execute
    echo "$var"
done
```

### Iterating over a range

Use brace expansion to loop through a sequence of numbers:

```bash
for i in {1..5}; do
    echo "Number: $i"
done
```

### Iterating over a list of strings

When the list contains multiple words, Bash splits them on whitespace by default. This behaviour is controlled by the `IFS` variable (see [IFS](13_built_in_variables.md#ifs-internal-field-separator) for a full explanation).

In this example, the string is split on spaces into three separate names:

```bash
string="Alice Bob Charlie"

for name in $string; do
    echo "Hello, $name!"
done
```

To split on a different character, change `IFS` before the loop:

```bash
IFS=','
string="Alice,Bob,Charlie"

for name in $string; do
    echo "Hello, $name!"
done
```

### Handling items with spaces

To iterate over items that contain spaces, quote each item individually:

```bash
for file in "File 1.txt" "File 2.txt"; do
    echo "$file"
done
```

When reading lines from a file, set `IFS` to a newline so that each line is treated as a single item:

```bash
IFS=$'\n'

for line in $(cat file.txt); do
    echo "$line"
done
```

### C-style syntax

Bash also supports a C-style `for` loop with an initialiser, condition, and increment:

```bash
for ((i=1; i<=5; i++)); do
    echo "Iteration $i"
done
```

### Empty iterations

When a glob pattern matches no files, Bash keeps the literal pattern instead of expanding it to nothing. This can cause unintended behaviour:

```bash
FILES="/var/log2/*"

for file in $FILES; do
    echo "Processing $file"  # Prints the literal pattern if no files match
done
```

**Solution 1** — Enable `nullglob` so that unmatched patterns expand to an empty string:

```bash
shopt -s nullglob

FILES="/var/log2/*"

for file in $FILES; do
    echo "Processing $file"
done
```

**Solution 2** — Store the results in an array and check before looping:

```bash
FILES=(/var/log2/*)

if [ -e "${FILES[0]}" ]; then
    for file in "${FILES[@]}"; do
        echo "Processing $file"
    done
else
    echo "No files found."
fi
```

### Skipping iterations

Use `continue` to skip the current iteration and move to the next one:

```bash
for i in {1..5}; do
    if [ "$i" -eq 3 ]; then
        continue
    fi
    echo "Number: $i"
done
```

### Exiting early

Use `break` to exit the loop immediately:

```bash
for i in {1..10}; do
    if [ "$i" -eq 5 ]; then
        echo "Breaking at $i"
        break
    fi
done
```

## while loop

A `while` loop executes a block of commands repeatedly as long as its condition evaluates to true. The condition is checked **before** each iteration.

```bash
while [ CONDITION ]; do
    # Commands to execute
done
```

Use `[ ]` for basic conditions or `[[ ]]` for more advanced conditions. Refer to [Test Command](19_test_command.md) for details.

### Counting example

```bash
counter=1

while [ $counter -le 5 ]; do
    echo "Counter is $counter"
    ((counter++))
done
```

### Reading a file line by line

The most common way to read a file line by line is to redirect the file into the loop:

```bash
while read line; do
    echo "$line"
done < file.txt
```

To read from a command's output, use process substitution:

```bash
while read line; do
    echo "Line: $line"
done < <(ls -1 *.txt)
```

## until loop

The `until` loop is the opposite of `while`. It executes a block of commands repeatedly **until** its condition evaluates to true — in other words, it runs as long as the condition is false.

```bash
until [ CONDITION ]; do
    # Commands to execute
done
```

### Example

```bash
counter=1

until [ $counter -gt 5 ]; do
    echo "Counter is $counter"
    ((counter++))
done
```

> **Tip:** Use `while` when you want the loop to run while a condition is true, and `until` when you want it to run while a condition is false.

---

[← Previous: Conditional Statements](22_conditional.md) | [Next: Arrays →](24_arrays.md)
