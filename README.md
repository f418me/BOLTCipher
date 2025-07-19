# BOLTCipher

BOLTCipher is a small FastAPI service that sells encrypted content via the Lightning Network. The plaintext lives in `content.txt`, is encrypted with ChaCha20 and delivered along with a Lightning invoice.

## Demo

You can try a running instance at <https://boltcipher.f418.me/>. To verify or decrypt the encrypted content use the companion project [BOLTCipherVerifier](https://github.com/f418me/BOLTCipherVerifier) which is also available online at <https://boltcipherverifier.f418.me/>.

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

Copy `.env_example` to `.env` and adjust the values to your environment. The example file contains all available settings with explanatory comments.

## Starting the Server

After installation and configuration the server can be started with Uvicorn. When running behind a reverse proxy (e.g. Caddy), bind the application to `0.0.0.0` and enable proxy header support:

```bash
APP_HOST=0.0.0.0 \
APP_PORT=8000 \
PROXY_HEADERS=True \
FORWARDED_ALLOW_IPS='*' \
uvicorn main:app
```

The HTML view is available on the configured host and port. A JSON API is served under `/json/`.

## Directory Structure

- `main.py` – entry point of the FastAPI server
- `templates/` – Jinja2 templates for the HTML output
- `static/` – static files such as CSS and images
- `sandbox/` – scripts to test encryption and the invoice flow
- `utils/` – helper functions (e.g. integration with Core Lightning)

## License

The code is released under the MIT License (see `LICENSE`).
