import requests

ENV_URL = "http://localhost:7860"


def reset(task: str = "easy"):
    r = requests.post(f"{ENV_URL}/reset", json={"task": task})
    r.raise_for_status()
    return r.json()


def step(action: str):
    r = requests.post(f"{ENV_URL}/step", json={"action": action})
    r.raise_for_status()
    return r.json()


def state():
    r = requests.get(f"{ENV_URL}/state")
    r.raise_for_status()
    return r.json()


def grade():
    r = requests.get(f"{ENV_URL}/grade")
    r.raise_for_status()
    return r.json()


def health():
    r = requests.get(f"{ENV_URL}/health")
    r.raise_for_status()
    return r.json()
