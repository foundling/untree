# untree: the inverse of tree

## Installation


`pip install untree`

## Usage

```

untree [options] -s schema_file -o output_dir
tree -F --noreport . | untree.py [options]
```

`untree` is meant to work with `tree` output, so it uses a slightly specific invocation of `tree` as its specification:

`tree -F --noreport <directory name>'
