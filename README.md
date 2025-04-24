# untree: the inverse of tree

## Installation


`pip install untree`

## Usage

```bash
untree [options] -s schema_file -o output_dir
```

## Input Specification

`untree` is designed to accept `tree` output as its input, so it requires a `schema` file formatted in the following way using the `tree` command:

`tree -F --noreport <directory name>'

The `-F` flag adds a trailing slash after directory names to distinguish them from regular files. The `--noreport` flag suppresses the `tree` summary.

