from core.models import Status


def feedback(secret: str, guess: str) -> str:
    result = [Status.ABSENT] * 5
    consumed = [False] * 5

    for i in range(5):
        if guess[i] == secret[i]:
            result[i] = Status.CORRECT
            consumed[i] = True

    for i in range(5):
        if result[i] == Status.ABSENT:
            for j in range(5):
                if not consumed[j] and guess[i] == secret[j]:
                    result[i] = Status.MISPLACED
                    consumed[j] = True
                    break

    return "".join(result)
