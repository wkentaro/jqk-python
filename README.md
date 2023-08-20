### DISCLAIMER

[Jqk](https://github.com/wkentaro/jqk), which is written in Rust language is
much faster than this, so it is highly recommended over this Python version
unless there is legitimate reasons.

# jqk-python

## Installation

```
pip install git+https://github.com/wkentaro/jqk-python
```

## Usage

```
usage: jqk [-h] [--color-output]

jqk - Query key finder for jq [version 0.1]

Example:

    $ echo '{"japan": [{"name": "tokyo", "population": "14M"}, {"name": "osaka", "population": "2.7M"}]}' > data.json

    $ cat data.json | jqk
    {
      .japan: [
        {
          .japan[0].name: "tokyo",
          .japan[0].population: "14M"
        },
        {
          .japan[1].name: "osaka",
          .japan[1].population: "2.7M"
        }
      ]
    }

    $ cat data.json | jq .japan | jqk
    [
      {
        .[0].name: "tokyo",
        .[0].population: "14M"
      },
      {
        .[1].name: "osaka",
        .[1].population: "2.7M"
      }
    ]

    $ cat data.json | jq .japan[1].population -r
    2.7M
    

positional arguments:
  file                JSON file to parse (default: None)

options:
  -h, --help          show this help message and exit
  --version, -V       display version (default: None)
  --color-output, -C  force color output even with pipe (default: False)
  --list, -l          list all keys (default: False)
```


## Related projects

- `jq`: https://github.com/jqlang/jq
- `jqk`: https://github.com/wkentaro/jqk
