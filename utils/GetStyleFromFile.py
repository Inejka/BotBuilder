def get_style(path: str) -> str:
    with open(path, encoding="utf-8") as file:
        return file.read()
