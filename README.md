# Device Recording and Encoding Automation Tests

This repository contains automation tests written in Python using the `pytest` framework. The tests validate the functionality of a mock device API that simulates device recording and encoding processes.

## Prerequisites

To run these tests, you need to have the following installed:

- Python 3.x
- `pytest` (testing framework)
- `requests` (for sending HTTP requests)
- `paramiko` (for SSH connection simulation)
- `ffmpeg-python` (for validating video properties)

### Installation

Before running the tests, install the required dependencies:

```sh
$ brew install ffmpeg
$ virtualenv venv/python3 -m venv venv
$ source venv/bin/activate or  deactivate
$ pip install -r requirements.txt
$ 
```
