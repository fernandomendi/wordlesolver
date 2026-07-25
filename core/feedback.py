from core.models import Status


def feedback(secret: str, guess: str) -> str:
    """
    Evaluates a Wordle guess against a secret word.

    Returns a 5-character string where each character represents the status
    of the corresponding letter: '0' = correct position, '1' = misplaced, '2' = absent.
    """
    answer = [Status.ABSENT] * 5

    for i in range(5):
        if guess[i] == secret[i]:
            answer[i] = Status.CORRECT
            secret = secret[:i] + '_' + secret[i+1:]

    for i in range(5):
        if answer[i] == Status.ABSENT and guess[i] in secret:
            answer[i] = Status.MISPLACED
            secret = secret.replace(guess[i], "_", 1)

    return "".join(answer)
