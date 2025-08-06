def prompt_to_spec(prompt):
    return {
        "prompt": prompt,
        "spec": {
            "type": "UI Component",
            "status": "generated",
            "details": f"This is a demo spec for: {prompt}"
        }
    }
