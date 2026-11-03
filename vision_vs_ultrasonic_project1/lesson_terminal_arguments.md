# Lesson: passing arguments from the terminal to Python

In this lesson, we will learn how `parse_args()` in [01_measure_ultrasonic.py](01_measure_ultrasonic.py) reads settings from a terminal command. Write your own explanations in the spaces provided; we can discuss them together.

**Goal:** explain how a value such as `--count 5` becomes `args.count` in Python, and what happens when a value is invalid.

## 1. A terminal command has parts

Imagine this command is run on Buck:

```bash
python3 01_measure_ultrasonic.py --target-cm 30 --count 5 --interval 0.5
```

| Part | Meaning |
| --- | --- |
| `python3` | Starts Python. |
| `01_measure_ultrasonic.py` | Names the Python program to run. |
| `--target-cm 30` | Gives the program the target distance you measured with a ruler. |
| `--count 5` | Requests five sensor readings. |
| `--interval 0.5` | Requests a half-second pause between readings. |

The pieces after the program name are called **command-line arguments**. The names beginning with `--` are options; the words after these options are their values. The terminal passes those values as text, and our Python program decides how to interpret them.

**My notes:** What would I change in the command to request ten readings?

> [Write here]

## 2. Make a parser and describe its options

The file imports Python's `argparse` module. A module is a collection of code we can use in our program. The first two lines of the function are:

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
```

`def` defines a function named `parse_args`. The empty parentheses mean our function does not take an explicit Python argument. The `-> argparse.Namespace` part is a **type hint** describing what it returns; it does not itself check or convert the terminal input.

`ArgumentParser` creates an object that knows how to read and check command-line options. `description=__doc__` uses the file's opening description as the description shown by `--help`.

Next, `add_argument()` describes each option:

```python
parser.add_argument("--count", type=int, default=20)
```

This says: recognize `--count`, convert its value to an integer (`int`), and use `20` if the option was left out. The other options are:

| Terminal option | Python type | Required? | Value if omitted | Purpose |
| --- | --- | --- | --- | --- |
| `--target-cm` | `float` | Yes | No default | Ruler-measured distance in centimeters |
| `--count` | `int` | No | `20` | Number of readings |
| `--interval` | `float` | No | `0.25` | Seconds between readings |
| `--output` | `Path` | No | `None` | Optional location for a CSV file |

A `float` can represent a fractional number, such as `0.5`; an `int` represents a whole number, such as `5`. `Path` is a Python object representing a file path. Parsing `--output` creates the `Path` object; the file is written later in `main()`.

**My notes:** Why might `--interval` use a `float` instead of an `int`?

> [Write here]

## 3. Read the values into `args`

```python
args = parser.parse_args()
```

This line reads the command-line arguments, converts the values using the types above, and puts them into an `argparse.Namespace`. A namespace is a container whose values can be accessed by name using a dot.

For the command in section 1, the result is conceptually:

```python
args.target_cm  # 30.0, a float
args.count      # 5, an int
args.interval   # 0.5, a float
args.output     # None, because --output was omitted
```

Notice that the hyphen in `--target-cm` becomes an underscore in `args.target_cm`. If `--count` had been omitted, `args.count` would be `20`.

**My notes:** For `--target-cm 40` with no other options, what values would `args.count` and `args.interval` have?

> [Write here]

## 4. Check the values before using hardware

Some inputs can be converted to a number but still do not make sense for this experiment:

```python
if args.count <= 0:
    parser.error("--count must be positive")
```

If the count is zero or negative, `parser.error()` prints a usage message and the error, then stops the program. The checks for `target_cm` and `interval` also use `math.isfinite()` to reject special values such as infinity and `NaN` (not a number). The target distance must be greater than zero; the interval may be zero but cannot be negative.

If all checks pass, `return args` sends the settings back to `main()`:

```python
args = parse_args()
```

`main()` can then use values like `args.count`. In this script, the `robot_hat` import comes **after** `parse_args()`, so a help request or invalid input exits before the hardware library is imported.

**My notes:** What happens with `--target-cm 30 --count 0`? Why is that useful?

> [Write here]

## 5. Try it on the Mac without Buck

Run these from the `PIDOG_coding` workspace. Both commands exit during argument parsing, before the sensor is accessed.

First, show the help page:

```bash
python3 vision_vs_ultrasonic_project1/01_measure_ultrasonic.py --help
```

Next, try an invalid count:

```bash
python3 vision_vs_ultrasonic_project1/01_measure_ultrasonic.py --target-cm 30 --count 0
```

**What I saw in the help output:**

> [Write here]

**What error did the second command print?**

> [Write here]

### Try a valid parse in Python

To explore successful parsing without starting the robot program, open Python with `python3`, then enter the following. This small practice parser uses the same two option definitions as the sensor script:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--target-cm", type=float, required=True)
parser.add_argument("--count", type=int, default=20)
args = parser.parse_args(["--target-cm", "30", "--count", "5"])
print(args.target_cm, args.count)
```

The list supplies example argument text directly to this practice parser. In the real script, `parser.parse_args()` has no list, so it reads the terminal command instead. Try changing `"5"` to `"10"`, then call `parse_args()` and `print()` again. Type `exit()` to leave Python.

**What did I observe?**

> [Write here]

## 6. Check my understanding

1. What is the difference between the option name `--count` and its value `5`?
2. If `--count` is omitted, what value does the script use?
3. Why does `--target-cm` become `args.target_cm`?
4. What does `return args` let `main()` do?
5. What question do I still have about any line in `parse_args()`?

**My answers and questions:**

> [Write here]
