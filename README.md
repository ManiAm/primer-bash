# Bash Primer

A comprehensive reference for Bash shell scripting — from basics to advanced topics.

## Introduction

| # | Topic | Description |
|---|-------|-------------|
| 01 | [Unix Shells](docs/01_introduction.md) | Shell overview, history, and major shell families |
| 02 | [Shell Configuration Files](docs/02_shell_config.md) | Login vs non-login shells, `.bashrc`, `.profile`, etc. |

## Shell Basics

| # | Topic | Description |
|---|-------|-------------|
| 03 | [Bash Keywords](docs/03_bash.md) | Reserved words and built-in keywords |
| 04 | [Interactive vs Non-Interactive Shells](docs/04_shell_type.md) | Shell modes and how to detect them |
| 05 | [Auto-Completion](docs/05_auto_completion.md) | Tab completion and programmable completion |
| 06 | [History Management](docs/06_history.md) | Command history, search, and `HISTCONTROL` |
| 07 | [Shell Prompt](docs/07_shell_prompt.md) | Customizing `PS1`, escape sequences, colors |
| 08 | [Shell Scripts](docs/08_shell_script.md) | Writing and executing shell scripts, shebang |

## Variables

| # | Topic | Description |
|---|-------|-------------|
| 09 | [Shell Variables](docs/09_shell_variables.md) | Variables, naming, types, and arithmetic |
| 10 | [Environment Variables](docs/10_env_variables.md) | `export`, child processes, and persistence |
| 11 | [PATH](docs/11_path_env_variable.md) | The `PATH` variable and command lookup |
| 12 | [`sudo` and Variables](docs/12_sudo_and_variables.md) | How `sudo` affects the environment |
| 13 | [Built-in Shell Variables](docs/13_built_in_variables.md) | `HOME`, `PWD`, `SHELL`, `USER`, etc. |
| 14 | [Special Variables](docs/14_special_variables.md) | `$?`, `$$`, `$!`, `$@`, `$#`, and more |

## Input / Output & File Operations

| # | Topic | Description |
|---|-------|-------------|
| 15 | [Input and Output](docs/15_input_output.md) | `echo`, `printf`, and `read` |
| 16 | [File and Directory Operations](docs/16_file_dir.md) | `cp`, `mv`, `rm`, `mkdir`, `find`, `tar`, etc. |
| 17 | [Shell Expansions](docs/17_shell_expansions.md) | Brace, tilde, parameter, arithmetic expansions |
| 18 | [Globbing (File Expansion)](docs/18_globbing.md) | Wildcards: `*`, `?`, `[…]`, extended globs |

## Tests & Operators

| # | Topic | Description |
|---|-------|-------------|
| 19 | [`test` Command](docs/19_test_command.md) | `test`, `[`, and `[[` syntax |
| 20 | [Test Operators](docs/20_test_operators.md) | File, string, and integer test operators |
| 21 | [Bash Operators](docs/21_bash_operators.md) | Assignment, arithmetic, logical, test, and redirection operators |

## Control Flow & Data Structures

| # | Topic | Description |
|---|-------|-------------|
| 22 | [Conditional Statements](docs/22_conditional.md) | `if…else`, `case`, and `select` |
| 23 | [Loops](docs/23_loop.md) | `for`, `while`, `until`, `break`, and `continue` |
| 24 | [Arrays](docs/24_arrays.md) | Indexed arrays, associative arrays, and `mapfile` |
| 25 | [Functions](docs/25_function.md) | Defining functions, local variables, return values |
| 26 | [Alias](docs/26_alias.md) | Creating and managing command aliases |

## Commands & Redirection

| # | Topic | Description |
|---|-------|-------------|
| 27 | [Exit Status](docs/27_exit_status.md) | Return codes, `$?`, and error handling |
| 28 | [Command Execution](docs/28_command_execution.md) | How Bash finds and runs commands |
| 29 | [Command Substitution](docs/29_command_substitution.md) | `$(…)` and backtick syntax |
| 30 | [Command Chaining](docs/30_command_chaining.md) | `&&`, `||`, `;`, and pipelines |
| 31 | [Redirection](docs/31_redirection.md) | `>`, `>>`, `2>`, `&>`, here-docs, here-strings |

## Processes & Job Control

| # | Topic | Description |
|---|-------|-------------|
| 32 | [Background Processes](docs/32_background.md) | `&`, `jobs`, `fg`, `bg` |
| 33 | [SIGHUP](docs/33_background_sighup.md) | Handling hangup signals, `nohup`, `disown` |
| 34 | [Daemon Processes](docs/34_dameon_process.md) | Running long-lived background services |
| 35 | [Sub-Shells](docs/35_subshell.md) | Parenthesized commands and subshell scope |

## Advanced Topics

| # | Topic | Description |
|---|-------|-------------|
| 36 | [Process Substitution](docs/36_process_substition.md) | `<(…)` and `>(…)` syntax |
| 37 | [Regex in Bash](docs/37_reg_exp.md) | `=~` operator, `grep`, `sed`, `awk` |
| 38 | [`trap`](docs/38_trap.md) | Signal handling and cleanup routines |
| 39 | [Shell Options](docs/39_shell_options.md) | `set`, `shopt`, and common options |

## Program Arguments & Options

| # | Topic | Description |
|---|-------|-------------|
| 40 | [Command-line Arguments](docs/40_program_args.md) | Positional parameters and `shift` |
| 41 | [Command-line Options](docs/41_program_options.md) | `getopts` and option parsing |
| 42 | [Processing Options](docs/42_process_options.md) | Advanced option processing patterns |

## Debugging

| # | Topic | Description |
|---|-------|-------------|
| 43 | [Debugging Bash Scripts](docs/43_debugging.md) | `set -x`, `set -e`, `trap DEBUG`, and more |

---

## Project Structure

```
#primer-bash/
├── docs/          ← Markdown notes (one per topic)
├── pics/          ← Diagrams and images
├── codes/         ← Example scripts and supporting files
└── README.md      ← This file
```
