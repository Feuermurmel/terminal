# terminal

Small tool to change visual attributes of a tab in Terminal.app.

## Usage

```
usage: terminal [-h] [--cursor COLOR] [--background COLOR] [--text COLOR]
                [--bold-text COLOR]

Set visual attributes of the current Terminal.app tab. COLOR is either three
or six hex digits to specify an RGB color, in the same way as CSS uses
(without the leading "#").

options:
  -h, --help          show this help message and exit
  --cursor COLOR
  --background COLOR
  --text COLOR
  --bold-text COLOR
```

## Development Setup

```
pre-commit install
make venv
```
