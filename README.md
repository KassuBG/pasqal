# Pasqal Compiler

This is a barebone library for you to develop your coding exercise. There should be a clear goal to achieve as detailed in the exercise sheet, but during your solution you are welcome to improve the repo in any way you see fit.

## Install from source

You can use [`hatch`](https://hatch.pypa.io/latest/) environment manager to install from source:

```bash
python -m pip install hatch

# Automatically gets you into an environment with all dependencies
python -m hatch shell
```

To remake your environment you can run `exit`, `hatch env prune` to delete it, and re-run `hatch shell`.

Or just use your preferred environment manager and install from source with `pip`:

```bash
python -m pip install -e .
```

## Getting started

To check everything is working properly, try running

```bash
python pasqal_compiler/main.py
```

Get familiar with the code in this file, and then you are good to go!
