# ![untree logo](untree-logo.png) untree: turn `tree` output back into directories

## Motivation

The `tree` command is a widely-used and useful tool.  We see it often in code tutorials and reference documents.

Here's a real-world example from [Real Python](realpython.com)'s article, [Python import: Advanced Techniques and Tips](https://realpython.com/python-import):

```
world/
│
├── africa/
│   ├── __init__.py
│   └── zimbabwe.py
│
├── europe/
│   ├── __init__.py
│   ├── greece.py
│   ├── norway.py
│   └── spain.py
│
└── __init__.py
```


Wouldn't it be nice to copy this into a file and generate a local directory tree? 

## Installation
`untree` is a command-line utility.  To install it globally, run:

```bash
pip install untree
```

## Usage

```bash
untree [options] -s schema_file -o output_dir
```

## Examples

### Using a schema file

```bash
# run 'tree' on a directory and save as a schema file.
$ tree -F --noreport path/to/src/dir > schema.txt

# this is what it looks like
$ cat schema.txt
testdir
├── testdir/a
│   └── testdir/a/a.txt
└── testdir/b
    └── testdir/b/b.txt

# run 'untree' on the schema file
$ untree -o /path/to/output/dir -s schema.txt

# run 'tree' on your newly generated file tree
$ tree -F --noreport /path/to/new_dir
new_dir
├── testdir/a
│   └── testdir/a/a.txt
└── testdir/b
    └── testdir/b/b.txt
```

### Using stdin

```bash
# pipe the output of tree directly into untree
$ tree -F --noreport /path/to/src/dir | untree -o /path/to/output/dir

```




## Input Specification

`untree` is designed to accept `tree` output as its input, so it requires a `schema` file formatted in the following way using the `tree` command:

`tree -F --noreport <directory name>'

The `-F` flag adds a trailing slash after directory names to distinguish them from regular files. The `--noreport` flag suppresses the `tree` summary.

