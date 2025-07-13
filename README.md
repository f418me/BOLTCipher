# BOLTCipher

BOLTCipher is a small FastAPI service that sells encrypted content via the Lightning Network. The plaintext lives in `content.txt`, is encrypted with ChaCha20 and delivered along with a Lightning invoice.

## Installation

1. Install Python 3.9 or newer.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application reads its settings from environment variables (e.g. using an `.env` file). The most important ones are:

- `LOG_LEVEL` – log level to use
- `PAGE_TITLE` – page title shown in the browser
- `PAGE_INFO` – additional information displayed on the index page
- `CONTENT_PRICE` – price for the encrypted content in satoshis
- `LIGHTNING_RPC_FILE` – path to the RPC file of a Core Lightning node
- `INVOICE_LABEL_PREFIX` – prefix for generated invoice labels
- `INVOICE_DESCRIPTION` – description text for the created invoice

## Starting the Server

After installation and configuration the server can be started with Uvicorn:

```bash
uvicorn main:app --reload
```

The HTML view is available at `http://localhost:8000/` by default. A JSON API is served under `/json/`.

## Directory Structure

- `main.py` – entry point of the FastAPI server
- `templates/` – Jinja2 templates for the HTML output
- `static/` – static files such as CSS and images
- `sandbox/` – scripts to test encryption and the invoice flow
- `utils/` – helper functions (e.g. integration with Core Lightning)

## License

The code is released under the MIT License (see `LICENSE`).
