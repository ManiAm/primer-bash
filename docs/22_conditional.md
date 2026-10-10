# Conditional Statements

Bash provides three constructs for controlling the flow of execution based on conditions: `if...else`, `case`, and `select`.

## if...else

The `if...else` statement runs different commands depending on whether a condition is true or false.

```bash
if [ condition1 ]; then
    # runs if condition1 is true
elif [ condition2 ]; then
    # runs if condition2 is true
else
    # runs if all conditions are false
fi
```

### Condition syntax

Conditions are enclosed in `[ ]` (POSIX test) or `[[ ]]` (Bash extended test). `[[ ]]` is preferred because it supports pattern matching, regex, and safer handling of special characters. Refer to [Test Command](19_test_command.md) for more detail.

> **Note:** There must be a space after `[` and before `]` (or `[[` / `]]`).

### Numeric comparison

```bash
read -p "Enter a number: " num

if [[ $num -gt 10 ]]; then
    echo "The number is greater than 10."
elif [[ $num -eq 10 ]]; then
    echo "The number is exactly 10."
else
    echo "The number is less than 10."
fi
```

### String comparison

When using `[ ]`, variables must be quoted to avoid errors with spaces or special characters. `[[ ]]` does not have this limitation.

```bash
read -p "Enter a string: " str

if [[ $str = "hello" ]]; then
    echo "You entered 'hello'."
else
    echo "You did not enter 'hello'."
fi
```

### Logical operators

Use `&&` (AND) and `||` (OR) inside `[[ ]]` to combine conditions.

With `[ ]`, use `-a` (AND) and `-o` (OR) instead, or chain separate tests with `&&` / `||` outside the brackets.

```bash
read -p "Enter your age: " age

if [[ $age -ge 18 && $age -le 65 ]]; then
    echo "You are eligible to work."
else
    echo "You are not eligible to work."
fi
```

## case

The `case` statement matches a value against a list of patterns and runs the commands for the first matching pattern. It is similar to a `switch` statement in other programming languages and is cleaner than a long chain of `if...elif...else` when handling many values.

Key rules:

- Each pattern block must end with `;;`.
- Always include a `*` (wildcard) pattern as the default to handle unmatched inputs.

### Basic example

```bash
echo "Enter a fruit:"
read fruit

case $fruit in
    apple)
        echo "You selected Apple."
        ;;
    banana)
        echo "You selected Banana."
        ;;
    orange)
        echo "You selected Orange."
        ;;
    *)
        echo "Unknown fruit."
        ;;
esac
```

### Multiple patterns per block

Use `|` to match more than one pattern in a single block.

```bash
echo "Enter a file extension:"
read ext

case $ext in
    jpg|jpeg|png)
        echo "Image file detected."
        ;;
    mp3|wav|ogg)
        echo "Audio file detected."
        ;;
    *)
        echo "Unknown file type."
        ;;
esac
```

### Glob patterns

`case` uses **glob patterns** (not regular expressions). Character classes like `[0-9]` match a single character in that range.

```bash
echo "Enter a number:"
read number

case $number in
    [0-9])
        echo "You entered a single-digit number."
        ;;
    [1-9][0-9])
        echo "You entered a two-digit number."
        ;;
    *)
        echo "Number not in range."
        ;;
esac
```

> See [Globbing](18_globbing.md) for more details.

## select

The `select` command creates a numbered menu and prompts the user to pick an option. It is useful for simple interactive scripts.

```bash
select VARIABLE in LIST
do
    COMMANDS
    break  # optional — exits the loop
done
```

How it works:

1. Bash displays each item in `LIST` with a number.
2. The user types the number of their choice.
3. The chosen value is stored in `VARIABLE`, and the `do` block runs.

> **Tip:** `select` runs in a loop. Use `break` or include an explicit "Quit" option to let the user exit. If the user enters an invalid number, `VARIABLE` will be empty — use `[[ -n $VARIABLE ]]` to check.

### Example

```bash
echo "Select your favorite fruit:"

select fruit in Apple Banana Orange Exit
do
    case $fruit in
        Apple)
            echo "You selected Apple."
            ;;
        Banana)
            echo "You selected Banana."
            ;;
        Orange)
            echo "You selected Orange."
            ;;
        Exit)
            echo "Goodbye!"
            break
            ;;
        *)
            echo "Invalid option. Try again."
            ;;
    esac
done
```

Sample output:

```
Select your favorite fruit:
1) Apple
2) Banana
3) Orange
4) Exit
#?
```

### Customising the prompt

By default, `select` displays `#?` as the prompt. Set the `PS3` variable before the `select` command to change it.

```bash
PS3="Pick a fruit (enter number): "

select fruit in Apple Banana Orange Exit
do
    case $fruit in
        Apple)  echo "You selected Apple." ;;
        Banana) echo "You selected Banana." ;;
        Orange) echo "You selected Orange." ;;
        Exit)   echo "Goodbye!"; break ;;
        *)      echo "Invalid option. Try again." ;;
    esac
done
```

---

[← Previous: Bash Operators](21_bash_operators.md) | [Next: Loops →](23_loop.md)
