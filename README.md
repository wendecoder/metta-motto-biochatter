# Metta Motto

This package provides integration of MeTTa and LLMs for prompt tamplates, guidance, and chaining as well as composition with other agents.

## Installation

The main requirement is [MeTTa](https://github.com/trueagi-io/hyperon-experimental/).

The project itself can be installed via
```bash
git clone git@github.com:zarqa-ai/metta-motto.git
cd metta-motto
```

## Usage

The package can be used both as a Python package
```python
import motto
```

and MeTTa extention
```
!(import! &self motto)
```

Please, refer to the [tutorial](tutorial) and [examples](examples). [Tests](tests) can also be considered in addition.

## Tests

The unit tests can be executed via

```bash
cd tests
pytest
```

## Biochatter with Metta-Motto setup

Navigate to the bio_ai folder

```bash
cd examples/bio_ai
```

Install required dependencies

```bash
pip install -r requirements.txt
```

set Openai Api Key

```bash
export OPENAI_API_KEY=<YOUR OPENAI API KEY>
```

## Running Bio_ai examples

Select the questions to run from the 'bio-ai.metta' file by uncomenting them. Then, run the below command

```bash
metta bio_ai.metta
```

## Note

The recommended environment for running this repository is the Docker environment within the hyperon-experimental repository.