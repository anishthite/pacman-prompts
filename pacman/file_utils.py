from yaml import load, Loader


def load_yml(path):
    with open(path, "r") as f:
        return load(f, Loader=Loader)
