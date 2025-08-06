# Prompt Interface

A simple Streamlit app to enter prompts, generate JSON specs, view logs, and simulate sending specs to agents.

## 🚀 Live Demo
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://prompt-interface-qtfu5mdiauyayhak8fro3w.streamlit.app/)

## Features
- Enter prompts and save with timestamps
- Generate and view JSON specs
- Log viewer in the sidebar
- Send specs to Evaluator or Unreal Engine (simulated)
- Delete old logs
- Dark mode UI

## Tech Stack
- Python 3
- Streamlit
- JSON, OS, Shutil

## Project Structure
prompt_interface/
├── main.py
├── utils/agent.py
├── prompts/
├── specs/
├── logs/
├── actions/
│ ├── send_to_evaluator/
│ └── send_to_unreal/



## How to Run
```bash
pip install -r requirements.txt
streamlit run main.py
