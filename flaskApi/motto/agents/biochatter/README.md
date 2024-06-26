## BioChatter MeTTa

This repo contains an implementation of **Natural Language Prompt** to **MeTTa Query** conversion.\
**Note:** *This implementation only works in a linux environment.*
- To run the examples, follow the steps below :

1. Install required dependencies
    - Using `poetry`
    ```bash
    poetry install
    ```
    - Using `pip`
    ```bash
    pip install -r requirements.txt
    ```
2. Activate Poetry virtual environment (if using `poetry`)
    ```bash
    poetry shell
    ```
3. Create `.env` file and add required environment variable
    ```bash
    touch .env && \
    echo OPENAI_API_KEY="<your_api_key>" > .env
    ```
4. Run `main.py`
    ```bash
    python3 main.py
    ```

### Repository structure:
- `bioatomspace_data_subset/` : Contains the sample MeTTa files from the Human BioAtomspace.
- `biochatter/` : Contains the [BioChatter](https://github.com/biocypher/biochatter) package for converting NL prompts to MeTTa queries.
- `biocypher_config/` : Contains the BioCypher schema configuration files.
- `main.py` : This is the main module that imports the BioChatter package.