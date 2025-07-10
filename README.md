# Bot Template

A modern Telegram bot template with rapid project setup powered by [uv](https://github.com/astral-sh/uv) and [aiogram](https://github.com/aiogram/aiogram).

## 🧩 Using this repository as a project template
- On GitHub, click **"Use this template"** (green button) to create your own repository based on this template.

- Update `pyproject.toml`:
    - Change the `name`, `description`, `authors`, and any other relevant fields.

- Update `.env` as needed for your project.

- Follow the installation and usage steps below.

That's it — you're ready to build your own aiogram bot!

## 📦 Installation

**Requirements:** [uv](https://github.com/astral-sh/uv)


- Set up the environment and install dependencies:

    ```bash
    uv sync
    uv pip install -Ue .
    ```

- Create your `.env` file (see example in `.env.example`) and set all required environment variables.

## 🚀 Running the Bot

- After installation and environment setup, simply run:

   ```bash
   bot-run
   ```
