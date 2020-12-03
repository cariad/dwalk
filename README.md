# dwalk: walks directories, merges dictionaries

`dwalk` is a Python package and CLI tool for walking directories and merging dictionaries.

## Installation

`dwalk` requires Python 3.8 or later.

```bash
pip3 install dwalk
```

## CLI usage

```bash
dwalk --filenames FILENAME [FILENAME ...] [--directory DIRECTORY]
```

- `--directory VALUE`: Directory to walk to. The files in this directory will take priority over the files in its parent. Optional, and uses the current working directory by default.
- `--filenames LOWEST_PRECEDENCE ... HIGHEST_PRECEDENCE`: Files to look for and merge in each walked directory. Files at the end of the list take precedence over files at the beginning.
- `--include-meta`: Flag to indicate whether or not to include metadata on each merged property.

## Example

### Merging via file precedence

Say you have two configuration files:

- `example/foo.yml` describes the default configuration, and:
- `example/foo.user.yml` describes a user's personal configuration.

```yaml
# foo.yml
prompts:
  accessibility: not-asked
  notifications: not-asked
theme: default
```

```yaml
# foo.user.yml
accessibility:
  high-contrast: true
prompts:
  accessibility: user-enabled
theme: pink
```

To merge these two configurations **with precedence given to the user's configuration**:

```bash
dwalk --directory example --filenames foo.yml foo.user.yml
```

```json
{
  "accessibility": {
    "high-contrast": true
  },
  "prompts": {
    "accessibility": "user-enabled",
    "notifications": "not-asked"
  },
  "theme": "pink"
}
```

Pass the optional `--include-meta` flag to see where each value came from:

```json
{
  "__dwalk__": {
    "accessibility": {
      "src": "/Users/cariad/code/dwalk/example/foo.user.yml"
    },
    "prompts": {
      "src": "/Users/cariad/code/dwalk/example/foo.yml"
    },
    "theme": {
      "src": "/Users/cariad/code/dwalk/example/foo.user.yml"
    }
  },
  "accessibility": {
    "high-contrast": true
  },
  "prompts": {
    "__dwalk__": {
      "accessibility": {
        "src": "/Users/cariad/code/dwalk/example/foo.user.yml"
      }
    },
    "accessibility": "user-enabled",
    "notifications": "not-asked"
  },
  "theme": "pink"
}
```

### Merging via directory precedence

Say you have three configuration files:

- `example/foo.yml` describes the default configuration, and:
- `example/foo.user.yml` describes a user's personal configuration, and:
- `example/game/foo.yml` describes a sub-project's default configuration:

```yaml
# example/foo.yml
prompts:
  accessibility: not-asked
  notifications: not-asked
theme: default
```

```yaml
# example/foo.user.yml
accessibility:
  high-contrast: true
prompts:
  accessibility: user-enabled
theme: pink
```

```yaml
# game/foo.yml
theme: sci-fi
requires:
  - gamepad
```

To merge these three configurations **in the context of the game directory**:

```bash
dwalk --directory example/game --filenames foo.yml foo.user.yml
```

```json
{
  "accessibility": {
    "high-contrast": true
  },
  "prompts": {
    "accessibility": "user-enabled",
    "notifications": "not-asked"
  },
  "requires": [
    "gamepad"
  ],
  "theme": "sci-fi"
}
```

Pass the optional `--include-meta` flag to see where each value came from:

```json
{
  "__dwalk__": {
    "accessibility": {
      "src": "/Users/cariad/code/dwalk/example/foo.user.yml"
    },
    "prompts": {
      "src": "/Users/cariad/code/dwalk/example/foo.yml"
    },
    "requires": {
      "src": "/Users/cariad/code/dwalk/example/game/foo.yml"
    },
    "theme": {
      "src": "/Users/cariad/code/dwalk/example/game/foo.yml"
    }
  },
  "accessibility": {
    "high-contrast": true
  },
  "prompts": {
    "__dwalk__": {
      "accessibility": {
        "src": "/Users/cariad/code/dwalk/example/foo.user.yml"
      }
    },
    "accessibility": "user-enabled",
    "notifications": "not-asked"
  },
  "requires": [
    "gamepad"
  ],
  "theme": "sci-fi"
}
```

## Directory precedence

`dwalk` always starts in the current user's home directory, then walks down from the volume root to the specified directory (or the current working directory if one wasn't specified).

## Thanks!

My name is [Cariad Eccleston](https://cariad.me) and I'm a freelance DevOps engineer. I appreciate you checking out my projects! I'm available for interesing gigs -- let's talk!
