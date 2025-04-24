# `untree`: turn tree output back into directories

![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 
![untree logo](untree-logo.png) 

## Motivation

`tree` is a widely-used and useful command-line tool.  We see it often in code tutorials and reference documents.

Here's a real-world example of `tree` output from [Real Python](realpython.com)'s article, [Python import: Advanced Techniques and Tips](https://realpython.com/python-import):

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

Wouldn't it be nice if we could copy this output and use it to generate the same file tree on our local machine? 

That's the point of `untree`.

## Installation
`untree` is a command-line utility.  To install it globally, run:

```bash
pip install untree
```

## Usage

```bash
untree [-s schema_file] -o output_dir
```

## Examples

### Paste text right into `untree`

Copy the tree output from a website, document or terminal and paste it right into `untree`.

```bash
# we don't pass a schema file flag here, so it waits for us to enter the schema directly.
# press CTRL-D to signal the end of the text.

$ untree -o /path/to/output/dir
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

### Read schema file into `untree` stdin

```bash
# pipe the output of tree directly into untree
$ untree -o /path/to/output/dir < schema.txt
```

### Pipe data into `untree` via stdin

```bash
# pipe the output of tree directly into untree
$ tree -F --noreport /path/to/src/dir | untree -o /path/to/output/dir
```

### Using a schema file

```bash
$ untree -o /path/to/output/dir -s schema.txt
```

## Input Specification

`untree` is designed specifically to accept `tree` output as its input. The standard invocation `tree <dir>`, however, produces output that is ambiguous (files and directories appear the same) and extranous (there is a summary at the end).

For these reasons, the `untree` spec requires a slightly specific invocation of `tree`: 

```bash
tree -F --noreport <directory name>'
```

- The `-F` flag adds a trailing slash after directory names to distinguish them from regular files.
- The `--noreport` flag suppresses the `tree` command's concluding summary.
