# No-IP DDNS Auto-Renew

An automated Python script utilizing Playwright to automatically renew free No-IP DDNS hostnames. It bypasses upsell prompts, solves reCAPTCHA challenges, and supports authenticated proxy routing to prevent captcha IP restrictions. Supports local and deployed usage.

## Features

- **Headless Browser Automation**: Uses Playwright to interact with the No-IP interface.
- **Automated reCAPTCHA Solving**: Leverages `playwright-recaptcha` (with audio-solving fallbacks).
- **Proxy Support**: Connects through an external proxy to bypass strict IP blocks often applied to CI/CD runners.
- **CLI Tool**: Packaged as a modern Python command-line utility (`ddns-renew`) for easy execution.
- **GitHub Actions Ready**: Includes a workflow file to run automatically on the 1st and 15th of every month.

## Prerequisites

- Python 3.13+
- FFmpeg (Required for audio-based reCAPTCHA solving)

## Local Setup

1. **Clone the repository and enter the directory**:

```bash
git clone <your-repo-url>
cd ddns-renew
```

2. **Install system dependencies**:

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y ffmpeg

# macOS
brew install ffmpeg
```

3. **Install the Python package and browser binaries**:
   Install the project in editable mode (which reads `pyproject.toml`) and fetch the Playwright Chromium binaries:

```bash
pip install -e .
playwright install --with-deps chromium
```

4. **Configure Environment Variables**:
   Copy the example environment file and add your details:

```bash
cp .env.example .env
```

Edit `.env` to include your No-IP Host ID (the `n=` parameter from the confirmation URL). You can also optionally provide a proxy URL and toggle headless mode:

```env
NOIP_HOST_ID=your_host_id_here
PROXY_URL=http(s)://username:password@proxy.example.com:port/
HEADLESS=True
```

_Note: Free webshare.io proxies will not work due to captcha IP address/rate limit restrictions._

## Usage

Once installed, the project exposes a global command. Run it locally:

```bash
ddns-renew
```

You can also pass arguments directly via the CLI, which will override the `.env` file settings:

```bash
ddns-renew <host_id> --proxy_url https://username:password@host:port/
```

## GitHub Actions Deployment

This project includes a `.github/workflows/renew.yml` file to fully automate the renewal process.

To enable it:

1. Go to your GitHub repository's **Settings** > **Secrets and variables** > **Actions**.
2. Add a new repository secret named `NOIP_HOST_ID` with your target host ID.
3. Add a new repository secret named `PROXY_URL` with your fully formatted proxy URL (e.g., `https://username:password@proxy.yourdomain.com:443`).

The workflow will now run automatically on the 1st and 15th of the month.
