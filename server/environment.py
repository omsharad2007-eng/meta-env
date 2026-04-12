TASKS = {
    "easy": [
        "image.png", "song.mp3", "report.pdf"
    ],
    "medium": [
        "image.png", "song.mp3", "report.pdf", "video.mp4", "notes.txt"
    ],
    "hard": [
        "image.png", "song.mp3", "report.pdf", "video.mp4", "notes.txt",
        "data.csv", "archive.zip", "photo.jpg"
    ],
    "expert": [
        "image.png", "song.mp3", "report.pdf", "video.mp4", "notes.txt",
        "data.csv", "archive.zip", "photo.jpg", "script.py", "music.wav",
        "spreadsheet.xlsx", "presentation.pptx"
    ],
}

CORRECT_FOLDERS = {
    "image.png": "images",
    "song.mp3": "audio",
    "report.pdf": "documents",
    "video.mp4": "videos",
    "notes.txt": "documents",
    "data.csv": "data",
    "archive.zip": "archives",
    "photo.jpg": "images",
    "script.py": "code",
    "music.wav": "audio",
    "spreadsheet.xlsx": "data",
    "presentation.pptx": "documents",
}

PARTIAL_CREDIT = {
    ("image.png", "photos"): 0.5,
    ("photo.jpg", "photos"): 0.5,
    ("notes.txt", "text"): 0.5,
    ("report.pdf", "files"): 0.5,
    ("song.mp3", "music"): 0.5,
    ("music.wav", "music"): 0.5,
    ("video.mp4", "media"): 0.5,
    ("data.csv", "files"): 0.5,
    ("archive.zip", "files"): 0.5,
    ("script.py", "scripts"): 0.5,
    ("spreadsheet.xlsx", "files"): 0.5,
    ("presentation.pptx", "files"): 0.5,
}


class FileOrganizerEnv:
    def __init__(self):
        self.files = []
        self.moved = {}
        self.score = 0.0
        self.done = False
        self.task = "easy"

    def reset(self, task: str = "easy"):
        self.task = task
        self.files = list(TASKS.get(task, TASKS["easy"]))
        self.moved = {}
        self.score = 0.0
        self.done = False
        return {
            "files": self.files,
            "message": f"Sort these {len(self.files)} files into correct folders.",
            "done": False
        }

    def step(self, action: str):
        try:
            parts = action.split("->")
            filename = parts[0].strip()
            folder = parts[1].strip()
        except Exception:
            return {
                "files": self.remaining_files(),
                "message": "Invalid action format. Use: filename -> folder",
                "reward": -0.5,
                "done": False
            }

        if filename not in self.files:
            return {
                "files": self.remaining_files(),
                "message": f"{filename} is not in the file list.",
                "reward": -0.5,
                "done": False
            }

        if filename in self.moved:
            return {
                "files": self.remaining_files(),
                "message": f"{filename} already moved.",
                "reward": -0.25,
                "done": False
            }

        correct = CORRECT_FOLDERS.get(filename)

        if folder == correct:
            reward = 1.0
            self.score += reward
            self.moved[filename] = folder
            message = f"Correct! {filename} -> {folder}"
        elif (filename, folder) in PARTIAL_CREDIT:
            reward = PARTIAL_CREDIT[(filename, folder)]
            self.score += reward
            self.moved[filename] = folder
            message = f"Partial credit! {filename} -> {folder} (correct: {correct})"
        else:
            reward = -1.0
            self.score += reward
            self.moved[filename] = folder
            message = f"Wrong! {filename} should go to {correct}"

        remaining = self.remaining_files()
        if len(remaining) == 0:
            self.done = True

        return {
            "files": remaining,
            "message": message,
            "reward": reward,
            "done": self.done
        }

    def state(self):
        return {
            "files": self.remaining_files(),
            "moved": self.moved,
            "score": self.score,
            "done": self.done
        }

    def grade(self):
        total = len(self.files)
        correct = sum(
            1 for f, folder in self.moved.items()
            if CORRECT_FOLDERS.get(f) == folder
        )
        partial = sum(
            1 for f, folder in self.moved.items()
            if (f, folder) in PARTIAL_CREDIT
        )
        normalized_score = round(correct / total if total > 0 else 0, 4)
        return {
            "score": round(self.score, 4),
            "correct": correct,
            "partial": partial,
            "total": total,
            "percentage": round((correct / total * 100) if total > 0 else 0, 2),
            "normalized_score": normalized_score
        }

    def remaining_files(self):
        return [f for f in self.files if f not in self.moved]
