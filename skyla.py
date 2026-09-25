"""Minimal terminal core for SKYLA."""

VERSION = "0.1.0"


def respond(command: str) -> str:
    """Return SKYLA's response for a terminal command."""
    normalized = command.strip().lower()

    if normalized == "hello skyla":
        return "Hello! I am SKYLA."
    if normalized == "exit":
        return "Goodbye!"
    return "I don't understand that command yet."


def run() -> None:
    """Start SKYLA and process terminal input until the user exits."""
    print(f"SKYLA started (version {VERSION})")
    print('Type "hello skyla" to test SKYLA or "exit" to quit.')

    while True:
        try:
            command = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        print(respond(command))
        if command.strip().lower() == "exit":
            break


if __name__ == "__main__":
    run()
