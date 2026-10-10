# Function

A function is a reusable block of code that performs a specific task. Functions help you organize your script into smaller, more readable, and maintainable pieces.

## Defining a Function

You can define a function with or without the `function` keyword.

**With the `function` keyword (Bash-specific):**

```bash
function greet {
    echo "Hello from the function!"
}

greet
```

**Without the `function` keyword (POSIX-compatible):**

```bash
greet() {
    echo "Hello from the function!"
}

greet
```

> When using the `function` keyword, the parentheses `()` after the name are optional. Omitting `function` is more portable and works in all POSIX-compliant shells, so it is the preferred style.

## Local Variables

By default, variables in Bash are global. The `local` keyword declares a variable that is scoped to the function where it is defined. This prevents the function from accidentally modifying a variable with the same name outside the function.

```bash
global_var="I am global"

my_function() {
    local global_var="I am local"
    echo "Inside function: $global_var"   # Output: I am local
}

my_function
echo "Outside function: $global_var"      # Output: I am global
```

## Passing Parameters

You pass parameters to a function the same way you pass arguments to a script. Inside the function, they are accessed using positional parameters: `$1`, `$2`, ..., `$n`.

```bash
greet() {
    echo "Hello, $1!"
}

greet "Alice"  # Output: Hello, Alice!
```

Here is another example with multiple parameters:

```bash
calculate_sum() {
    local a=$1   # First argument
    local b=$2   # Second argument
    local sum=$((a + b))
    echo "Sum is: $sum"
}

calculate_sum 5 10  # Output: Sum is: 15
```

## Pass by Value

When you pass a variable to a function, Bash substitutes the variable's **value** before the function receives it. The function works on a copy, so any modifications inside the function **do not** affect the original variable.

```bash
modify_variable() {
    local var=$1
    var="modified"
    echo "Inside function: $var"    # Output: modified
}

original="original"
modify_variable "$original"
echo "Outside function: $original"  # Output: original
```

## Pass by Name Reference

Bash 4.3+ supports **namerefs** (`local -n`), which let a function refer to another variable **by name**. Instead of passing the value, you pass the variable's name, and changes made through the nameref affect the original variable directly.

```bash
modify_variable() {
    local -n ref=$1   # ref becomes an alias for the named variable
    ref="modified"    # Modifies the original variable
}

my_var="original"
modify_variable my_var          # Pass the name, not the value
echo "my_var: $my_var"          # Output: my_var: modified
```

> Notice that we pass `my_var` (the name) rather than `"$my_var"` (the value).

## Passing an Array

Since arrays cannot be passed by value in Bash, you pass the **name** of the array and use a nameref to access it inside the function.

**Reading an array:**

```bash
print_array() {
    local -n array_ref=$1          # Create a nameref to the array
    echo "${array_ref[@]}"         # Print all elements
}

my_array=("apple" "banana" "cherry")
print_array my_array               # Output: apple banana cherry
```

**Modifying an array:**

```bash
append_to_array() {
    local -n array_ref=$1          # Create a nameref to the array
    array_ref+=("new_item")        # Append an element
}

my_array=("apple" "banana")
append_to_array my_array
echo "${my_array[@]}"              # Output: apple banana new_item
```

Because the nameref points to the original array, any changes made through it **do** affect the caller's array.

## Return Values

Bash functions do not return arbitrary values the way functions do in other languages. Instead, there are two mechanisms:

- **`return`** — Sets the function's exit status (an integer from 0 to 255). By convention, `0` means success and any non-zero value means failure. For more on exit status codes and how they work, see [Exit Status](27_exit_status.md).

- **`echo`** — Prints output that the caller can capture with command substitution.

**Using `return` for exit status:**

```bash
check_even() {
    if (( $1 % 2 == 0 )); then
        return 0  # Success (even)
    else
        return 1  # Failure (odd)
    fi
}

check_even 4

if [[ $? -eq 0 ]]; then
    echo "Even number!"
else
    echo "Odd number!"
fi
```

**Using `echo` to return a value:**

```bash
add_numbers() {
    local result=$(( $1 + $2 ))
    echo "$result"
}

sum=$(add_numbers 3 7)
echo "The sum is $sum"  # Output: The sum is 10
```

> Command substitution (`$(...)`) captures only `stdout`. Any `stderr` output from the function is **not** captured and is still printed to the terminal. See [Command Substitution](29_command_substitution.md) for details on handling `stderr` and exit codes.

**Combining both in a single function:**

A function can use `echo` to output a computed value and `return` to indicate success or failure at the same time.

```bash
divide() {
    if (( $2 == 0 )); then
        return 1  # Failure: division by zero
    fi
    echo $(( $1 / $2 ))
    return 0      # Success
}

result=$(divide 10 2)
if [[ $? -eq 0 ]]; then
    echo "Result: $result"   # Output: Result: 5
else
    echo "Error: division by zero"
fi

result=$(divide 10 0)
if [[ $? -eq 0 ]]; then
    echo "Result: $result"
else
    echo "Error: division by zero"  # Output: Error: division by zero
fi
```

## Redefining a Function

Bash allows you to redefine a function by declaring a new function with the same name. The new definition overrides the previous one.

```bash
my_function() {
    echo "First version."
}

my_function  # Output: First version.

# Redefine the function
my_function() {
    echo "Overridden version."
}

my_function  # Output: Overridden version.
```

You can make a function read-only so it cannot be redefined:

```bash
my_func() {
    echo "This is a readonly function."
}

readonly -f my_func

# Attempting to redefine will produce an error
my_func() {
    echo "Re-defined"
}
```

---

[← Previous: Arrays](24_arrays.md) | [Next: Alias →](26_alias.md)
