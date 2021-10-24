---
title: Getting started
---

# Getting started

SatelliteDB is a database object extraction and versioning tool.
. If you're familiar with Python, you
can install SatelliteDB with [`pip`][1], the Python package manager.

## Prerequisites

-   Install [git](https://git-scm.com/)
-   Install [Python](https://www.python.org/)

## Installation

### with pip

SatelliteDB can be installed with `pip`:

```
pip install satellitedb
```

### with git

SatelliteDB can be directly used from [GitHub][3] by cloning the
repository into a subfolder of your project root which might be useful if you
want to use the very latest version:

1. Clone repository to your local

```
    $ git clone https://github.com/datadlog/satellitedb.git
```

1. Ensure [poetry](https://python-poetry.org/docs/) is installed, if not follow below.

```
    $ cd satellitedb
    $ python -m pip install --upgrade pip
    $ pip install poetry
```

1. Install dependencies and start your virtualenv:

```
    $ poetry install
```

[1]: #with-pip-recommended
[3]: https://github.com/datadlog/satellitedb
