# Process Substitution

Process substitution lets you use the output (or input) of a command as if it were a file. This avoids creating and cleaning up temporary files manually.

| Type     | Purpose                | Direction       | Example                                                          |
|----------|------------------------|-----------------|------------------------------------------------------------------|
| `<(...)` | Process → file input   | Read (input)    | `diff <(sort file1.txt) <(sort file2.txt)`                       |
| `>(...)` | File output → process  | Write (output)  | `tee >(grep ERROR > errors.log) >(grep WARNING > warnings.log)`  |

> **Note:** Process substitution requires Bash or Zsh. It is not available in plain POSIX shells like `sh`.

Under the hood, Bash creates an anonymous pipe and exposes it as a file path (like `/dev/fd/63`), which it passes to the command that expects a filename. On systems without `/dev/fd` support, Bash falls back to creating a named pipe (FIFO) via `mkfifo` instead. Most modern Linux and macOS systems use the `/dev/fd` method.

## Input Process Substitution `<(...)`

`<(subcommand)` runs `subcommand` in a subshell and produces a filename whose contents are the subcommand's standard output. Any program that reads from a file can use this filename instead:

```bash
command < <(subcommand)
```

- `<(subcommand)` — runs the subcommand and exposes its output through a temporary file descriptor.
- `<` — redirects that file descriptor as standard input to `command`.

### Example — Comparing Sorted Output with `diff`

The `diff` command compares two **files** line by line. It cannot compare two command outputs directly. Without process substitution you would need temporary files:

```bash
sort file1.txt > sorted1.txt
sort file2.txt > sorted2.txt

diff sorted1.txt sorted2.txt

rm sorted1.txt sorted2.txt
```

With process substitution, the same task becomes a single line:

```bash
diff <(sort file1.txt) <(sort file2.txt)
```

`sort file1.txt` and `sort file2.txt` each run in their own subshell, and their outputs are presented to `diff` as two temporary file descriptors — no cleanup required.

## Output Process Substitution `>(...)`

`>(subcommand)` runs `subcommand` in a subshell and produces a filename that the caller **writes** to. Anything written to that filename becomes the standard input of `subcommand`:

```bash
command > >(subcommand)
```

- `>(subcommand)` — runs the subcommand and accepts input through a temporary file descriptor.
- `>` — redirects the output of `command` into that file descriptor.

### Example — Splitting Log Output with `tee`

Suppose you want to split a log file into separate files for errors and warnings. Without process substitution, you would need to read the file multiple times:

```bash
grep ERROR logfile.log > errors.log
grep WARNING logfile.log > warnings.log
```

This works, but the file is read twice. The `tee` command reads from standard input and writes the same data to one or more destinations simultaneously. Combined with process substitution, it can read the file once and send its input directly to filtering commands — no temporary files, no cleanup:

```bash
tee >(grep ERROR > errors.log) >(grep WARNING > warnings.log) < logfile.log
```

- `tee` reads from `logfile.log` once (via input redirection `<`).
- The first process substitution `>(grep ERROR > errors.log)` receives the full input and writes only lines containing "ERROR" to `errors.log`.
- The second process substitution `>(grep WARNING > warnings.log)` does the same for "WARNING" lines, writing them to `warnings.log`.

---

[← Previous: Subshell](35_subshell.md) | [Next: Regex →](37_reg_exp.md)
