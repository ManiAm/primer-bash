# Arrays

Bash supports two types of arrays:

- **Indexed Arrays** (ordered lists accessed by number)
- **Associative Arrays** (key-value pairs accessed by name)

## Indexed Arrays

An indexed array stores an ordered list of values. Each value is accessed by a numerical index starting from `0`.

### Declaring and initialising

You can initialise an array by listing its elements inside parentheses:

```bash
fruits=(apple banana cherry)
```

When elements contain spaces, quote each one individually:

```bash
words=("hello world" "bash scripting" "arrays")
```

You can also declare an empty array first and assign elements by index:

```bash
declare -a fruits

fruits[0]=apple
fruits[1]=banana
fruits[2]=cherry
```

### Accessing elements

Use `${arr[index]}` to retrieve a single element:

```bash
words=("hello world" "bash scripting" "arrays")

echo "${words[0]}"  # Output: hello world
echo "${words[2]}"  # Output: arrays
```

### Accessing all elements

Use `${arr[@]}` or `${arr[*]}` to reference every element:

```bash
fruits=(apple banana cherry)

echo "${fruits[@]}"  # Output: apple banana cherry
echo "${fruits[*]}"  # Output: apple banana cherry
```

> **Tip:** `"${arr[@]}"` expands each element as a separate word, while `"${arr[*]}"` joins all elements into a single string separated by the first character of `IFS`. Always prefer `"${arr[@]}"` when iterating or passing elements to commands.

### Appending elements

Use `+=` to append one or more elements to the end of an array:

```bash
fruits=(apple banana)
fruits+=(cherry orange)

echo "${fruits[@]}"  # Output: apple banana cherry orange
```

### Counting elements

Use `${#arr[@]}` to get the number of elements:

```bash
fruits=(apple banana cherry)

echo "${#fruits[@]}"  # Output: 3
```

### Looping through elements

Use a `for` loop with `"${arr[@]}"` to iterate over each element:

```bash
fruits=(apple banana cherry)

for fruit in "${fruits[@]}"; do
    echo "$fruit"
done
```

### Removing elements

Use `unset` to remove an element by index:

```bash
fruits=(apple banana cherry orange)

unset 'fruits[1]'

echo "${fruits[@]}"  # Output: apple cherry orange
```

> **Note:** `unset` removes the element but does **not** re-index the remaining elements. Index `1` becomes empty, and the original indices of other elements are preserved. Use `fruits=("${fruits[@]}")` afterwards if you need a contiguous array.

To delete the entire array, use `unset` on the array name:

```bash
unset fruits
```

To clear all elements while keeping the array declared, reassign it to an empty list:

```bash
fruits=()
```

### Readonly arrays

Use `readonly` to prevent an array from being modified:

```bash
readonly -a COLORS=("Red" "Green" "Blue")

COLORS[0]="Yellow"  # Error: COLORS: readonly variable
```

## Associative Arrays

An associative array stores **key-value pairs**. Each value is accessed using a unique string key instead of a numeric index. This makes associative arrays useful for configuration data, lookup tables, and mappings.

> **Note:** Associative arrays require Bash 4.0 or later.

### Declaring and assigning

You must explicitly declare an associative array with `declare -A` before using it:

```bash
declare -A fruits

fruits[apple]=red
fruits[banana]=yellow
fruits[cherry]=red
```

### Accessing values

Use `${arr[key]}` to retrieve a value by its key:

```bash
echo "${fruits[apple]}"   # Output: red
echo "${fruits[banana]}"  # Output: yellow
```

### Listing keys and values

Use `${!arr[@]}` to get all keys and `${arr[@]}` to get all values:

```bash
echo "${!fruits[@]}"  # Output: apple banana cherry
echo "${fruits[@]}"   # Output: red yellow red
```

> **Note:** Associative arrays do not guarantee a specific iteration order. The keys may appear in any order.

### Looping through an associative array

Iterate over the keys with `${!arr[@]}` and look up each value:

```bash
declare -A fruits

fruits[apple]=red
fruits[banana]=yellow
fruits[cherry]=red

for key in "${!fruits[@]}"; do
    echo "$key --> ${fruits[$key]}"
done
```

### Removing elements

Use `unset` to remove a single key-value pair or the entire array:

```bash
unset 'fruits[banana]'

echo "${!fruits[@]}"  # Output: apple cherry
```

```bash
unset fruits  # Deletes the entire array
```

## `mapfile` and `readarray`

`mapfile` and `readarray` are built-in commands that read lines from standard input into an indexed array. They are aliases for each other and behave identically.

> **Note:** Both commands require Bash 4.0 or later.

### Reading from a file

Each line of the file becomes one element in the array. The `-t` option strips the trailing newline from each line:

```bash
echo -e "apple\nbanana\ncherry" > fruits.txt

readarray -t fruits < fruits.txt

echo "${fruits[@]}"  # Output: apple banana cherry
echo "${fruits[1]}"  # Output: banana
```

### Reading from a command

Use process substitution (`< <(...)`) to read the output of a command into an array:

```bash
readarray -t lines < <(echo -e "line1\nline2\nline3")

echo "${lines[@]}"  # Output: line1 line2 line3
```

> For more on process substitution, see [Process Substitution](36_process_substition.md).

---

[← Previous: Loop](23_loop.md) | [Next: Function →](25_function.md)
