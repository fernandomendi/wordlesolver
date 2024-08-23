class Language:
    ES: str = "es"
    EN: str = "en"

class Status:
    def __init__(self, code: str, color: str):
        self.code: str = code
        self.color: str = color

    def __repr__(self):
        return f"{self.code} : #{self.color}"

class Answer:
    CORRECT: Status = Status("0", "43a047")
    MISPLACED: Status = Status("1", "e4a81d")
    ABSENT: Status = Status("2", "757575")
