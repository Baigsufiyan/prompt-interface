import streamlit as st
import os
import json
import shutil
from datetime import datetime
from utils.agent import prompt_to_spec

# Create folders if they don't exist
for folder in ["prompts", "logs", "specs", "actions/send_to_evaluator", "actions/send_to_unreal"]:
    os.makedirs(folder, exist_ok=True)

# Page setup
st.set_page_config(page_title="Prompt Interface", layout="wide")
st.title("Prompt Interface")
st.markdown("Easily generate specs, view logs, and forward them to agent")

# Dark mode styling
st.markdown("""
<style>
    body { background-color: #1E1E1E; color: white; }
    .stTextInput, .stTextArea { background-color: #2C2C2C; color: white; }
    .stButton button { background-color: #4CAF50; color: white; }
</style>
""", unsafe_allow_html=True)

# Sidebar log viewer
st.sidebar.header("Log Viewer")
log_path = "logs/prompt_logs.json"
logs = []

if os.path.exists(log_path):
    try:
        with open(log_path, "r") as file:
            logs = json.load(file)
    except json.JSONDecodeError:
        st.sidebar.error("Log file is corrupted!")

selected_prompt = None
selected_spec_path = None

if logs:
    options = [f"{log['timestamp']} - {log['prompt']}" for log in logs]
    selected = st.sidebar.selectbox("Select a past prompt:", options)
    selected_time = selected.split(" - ")[0]
    selected_prompt = next((l for l in logs if l["timestamp"] == selected_time), None)

    if selected_prompt:
        st.sidebar.write(f"**Prompt:** {selected_prompt['prompt']}")
        selected_spec_path = f"specs/{selected_prompt['timestamp']}.json"

        if os.path.exists(selected_spec_path):
            try:
                with open(selected_spec_path, "r") as f:
                    st.sidebar.json(json.load(f))
            except json.JSONDecodeError:
                st.sidebar.error("Spec file is corrupted!")
        else:
            st.sidebar.warning("Spec file not found.")

        # Delete log
        if st.sidebar.button("🗑 Delete This Log"):
            logs = [l for l in logs if l["timestamp"] != selected_time]
            with open(log_path, "w") as f:
                json.dump(logs, f, indent=4)

            prompt_file = f"prompts/{selected_time}.txt"
            if os.path.exists(prompt_file):
                os.remove(prompt_file)

            if os.path.exists(selected_spec_path):
                os.remove(selected_spec_path)

            st.sidebar.success("Log deleted successfully")
            st.rerun()
else:
    st.sidebar.info("No logs available")

# Main layout
left, right = st.columns([2, 1])

with left:
    st.subheader("Create New Prompt")
    prompt = st.text_area("Enter your prompt : ")

    if st.button("Generate Spec"):
        if not prompt.strip():
            st.warning("Please enter a prompt")
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")

            with open(f"prompts/{ts}.txt", "w") as f:
                f.write(prompt)

            if not os.path.exists(log_path):
                with open(log_path, "w") as f:
                    json.dump([], f)

            with open(log_path, "r") as f:
                logs = json.load(f)

            logs.append({"timestamp": ts, "prompt": prompt})
            with open(log_path, "w") as f:
                json.dump(logs, f, indent=4)

            spec = prompt_to_spec(prompt)
            with open(f"specs/{ts}.json", "w") as f:
                json.dump(spec, f, indent=4)

            st.success("Prompt saved and spec generated")
            st.json(spec)

with right:
    if selected_spec_path and os.path.exists(selected_spec_path):
        st.subheader("Send Spec to Agent")
        c1, c2 = st.columns(2)

        with c1:
            if st.button("Send to Evaluator"):
                shutil.copy(selected_spec_path, "actions/send_to_evaluator/")
                st.success(" Spec sent to Evaluator")

                act_log = "logs/action_logs.json"
                if not os.path.exists(act_log):
                    with open(act_log, "w") as f:
                        json.dump([], f)

                with open(act_log, "r") as f:
                    actions = json.load(f)
                actions.append({"action": "send_to_evaluator", "timestamp": selected_prompt["timestamp"]})
                with open(act_log, "w") as f:
                    json.dump(actions, f, indent=4)

        with c2:
            if st.button("Send to Unreal Engine"):
                shutil.copy(selected_spec_path, "actions/send_to_unreal/")
                st.success("Spec sent to Unreal Engine")

                act_log = "logs/action_logs.json"
                if not os.path.exists(act_log):
                    with open(act_log, "w") as f:
                        json.dump([], f)

                with open(act_log, "r") as f:
                    actions = json.load(f)
                actions.append({"action": "send_to_unreal", "timestamp": selected_prompt["timestamp"]})
                with open(act_log, "w") as f:
                    json.dump(actions, f, indent=4)
