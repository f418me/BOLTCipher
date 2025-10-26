# BOLTCipher

BOLTCipher is a proof of concept FastAPI service that sells encrypted content via the Lightning Network. The plaintext lives in `content.txt`, is encrypted with ChaCha20 and delivered along with a Lightning invoice.

## Introduction

### The Concept

BOLTCipher demonstrates an innovative approach to selling digital content via the Lightning Network: encrypting content with the preimage of a Lightning invoice. The core idea is that the payment proof (the preimage) simultaneously serves as the decryption key.

**The Principle:**
- A Lightning invoice is created with a random preimage (32 bytes)
- This preimage is used as the encryption key for ChaCha20
- The content is encrypted and delivered along with the invoice
- Only by paying the invoice does the buyer receive the preimage
- With the preimage, the encrypted content can be decrypted

This cryptographically links payment and access rights – whoever has paid can decrypt.

### When to Use BOLTCipher vs L402

**L402 (Payment Required Before Service):**
When providing a service that incurs costs (e.g., calling external APIs, running computations, using resources), you need payment upfront. L402 is the right choice here – the client pays first, then receives the service.

**BOLTCipher (Content Delivery):**
When delivering static content or data that's already available, BOLTCipher offers a simpler alternative. The content is delivered immediately in encrypted form, and payment unlocks the decryption key. This approach:
- Eliminates the need for payment verification before delivery
- Reduces server-side complexity (no authentication, session management, or payment tracking)
- Allows instant content delivery with cryptographic payment enforcement
- Works well for information, documents, media files, or any pre-existing data

In essence: if your service costs you money to provide, use L402. If you're selling content or data, BOLTCipher provides a lightweight alternative.

### The Process

**1. Content Request**
- A user accesses the BOLTCipher instance (web interface or JSON API)
- The system reads the content to be sold from `content.txt`

**2. Encryption**
- A random 32-byte preimage is generated (this becomes the encryption key)
- A random 12-byte nonce is created for ChaCha20
- The content is encrypted with ChaCha20:
  - Key: the preimage (32 bytes)
  - Nonce: the generated nonce (12 bytes)
- The result is Base64-encoded

**3. Invoice Generation**
- A Lightning invoice (BOLT11) is created via Core Lightning
- The invoice uses the previously generated preimage
- Price and description are taken from the configuration

**4. Delivery**
- The user receives:
  - The encrypted content (Base64)
  - The nonce (hexadecimal)
  - The Lightning invoice (BOLT11)

**5. Payment & Decryption**
- The user pays the Lightning invoice
- As payment proof, they receive the preimage (32 bytes)
- With preimage + nonce, the content can be decrypted
- Decryption is performed via [BOLTCipherVerifier](https://github.com/f418me/BOLTCipherVerifier)

**Security Aspects:**
- The preimage only leaves the server through payment of the invoice
- Encryption uses ChaCha20, a modern symmetric algorithm
- Each content request generates a new preimage and nonce
- The server stores no association between buyer and content

### Use Case: AI Agents and llms.txt

A practical use case for BOLTCipher is providing information to AI agents via the [llms.txt](https://llmstxt.org/) standard, where premium content requires payment.

**Scenario:**
- A resource provides basic information freely accessible via `/llms.txt`
- The llms.txt file references additional premium content available through BOLTCipher
- AI agents can access the free information and discover paid content
- For premium information, the agent receives encrypted content and a Lightning invoice
- Upon payment, the agent obtains the preimage to decrypt the premium content
- This enables micropayments for AI-consumed information without traditional authentication

**Example llms.txt structure:**
```
# Basic Information
[Free content about the resource...]

# Premium Content
For detailed technical specifications, access:
https://example.com/premium-content
Price: 100 satoshis
```

This approach allows content creators to monetize specialized knowledge while keeping basic information freely accessible, creating a pay-per-use model for AI agent interactions.

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
