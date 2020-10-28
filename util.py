from typing import Any

def log(debug: bool, *args: Any) -> None:
    if debug:
        print(*args)
