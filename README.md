# 🧠 Copilot Agent (Gemini)

A lightweight, extensible **Python-based AI Copilot Agent** powered by **Google’s Gemini LLM**, designed to assist in automating workflows, reasoning over data, and integrating natural language intelligence into your local or cloud-based systems.

---

## 🚀 Features

* 🧩 **Gemini LLM Integration** — Connects seamlessly with Google Gemini via API.
* ⚙️ **Modular Agent Design** — Plug in custom tools.
* 💬 **Conversational Reasoning** — Natural language input with contextual memory.
* 🗃️ **Local Execution** — Run Python tasks, scripts, or system commands safely.
---

## 📦 Installation

```bash
git clone https://github.com/jepixo/copilot_agent.git
cd copilot_agent
pip install -r requirements.txt
```

If using a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # (on Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

---

## 🔑 Setup Environment Variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

---

## 🧰 Usage

Run the main agent locally:

```bash
uv run main.py "your-prompt"
```


---

## 🧠 Architecture Overview

```
copilot_agent/
├── main.py                  # Entry point
├── call_function.py         # Tool calling
├── config.py                # model configs
├── tests.py                 # Well, tests..
├── functions/
│   ├── get_file_info.py     # Fetch the list of dirs and files
│   ├── get_file_content.py  # Fetch the content of a file
│   ├── write_file.py        # Write to an existing file or create and write
│   ├── run_python_file.py   # Run a python file using python interpreter
```

---

## 🧩 Extending the Agent

Add a new tool under `functions/`:

```python
@tool("weather")
def get_weather(city: str):
    """Get live weather for a city."""
    return f"The weather in {city} is sunny ☀️"
```

Then register it in your `Agent` class — the agent will automatically learn how to call it when relevant.

---

## ⚙️ Requirements

* Python 3.9+
* `google-generativeai`
* `python-dotenv`

---

## 📄 License

MIT License © 2025 Jepixo™