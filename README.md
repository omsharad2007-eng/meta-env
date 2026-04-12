---
title: Meta Env
emoji: 🗂
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# File Organizer Environment

An AI environment where an agent learns to sort files into correct folders.

## Real-World Task
File organization is a task humans do daily. This environment trains agents to correctly categorize files by type.

## Action Space
`filename -> folder`

Example: `image.png -> images`

## Observation Space
- `files`: list of remaining files to sort
- `message`: feedback on last action
- `reward`: 1.0 correct, 0.5 partial, -1.0 wrong
- `done`: true when all files are sorted

## Tasks
| Level | Files | Description |
|-------|-------|-------------|
| easy | 3 files | image, audio, document |
| medium | 5 files | adds video and text |
| hard | 8 files | adds csv, zip, photo |
| expert | 12 files | adds code, wav, xlsx, pptx |

## Reward Function
- `+1.0` correct folder
- `+0.5` partial credit (similar folder)
- `-0.25` file already moved
- `-0.5` invalid action format
- `-1.0` wrong folder

## Baseline Scores
| Task | Score |
|------|-------|
| easy | 1.0 |
| medium | 1.0 |
| hard | 1.0 |
| expert | 1.0 |

## API Endpoints
- `POST /reset` - start new task
- `POST /step` - perform action
- `GET /state` - get current state
- `GET /grade` - get score report
- `GET /health` - health check

## Run Locally
```bash
docker build -t meta-env .
docker run -p 7860:7860 meta-env
python inference.py
```
