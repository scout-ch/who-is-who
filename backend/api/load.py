import json
import os


def store(page, page_name, builddir="build"):
    filename = os.path.join(builddir, _filename(page_name, "html"))

    if not os.path.exists(builddir):
        os.makedirs(builddir)

    report = "replaced" if os.path.exists(filename) else "created"

    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(page)
        print(f"-- {report} {filename}")


def _filename(path, extension="html"):
    if path.split(".")[-1] != extension:
        path = ".".join([path, extension])
    return path


def store_to_json(data, filepath="transformed_data.json"):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
        )


def read_json(file="transformed_data.json"):
    with open(file, "r", encoding="utf-8") as file:
        return json.load(file)
