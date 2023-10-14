def stringify_season(season):
    return f"{season}-{season + 1}"


def slugify_item(*args, **kwargs):
    first = "-".join(str(i).strip(". ") for i in args)
    second = "-".join(str(kwargs[i]).strip(". ") for i in kwargs)
    return "-".join([first, second])
