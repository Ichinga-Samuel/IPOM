from pathlib import Path


base_dir = Path(__file__).resolve().parent.parent

assets = base_dir / 'assets'


def static(file, typ):
    """
    Creates a path to the assets folder containing images, icons and other types of static assets
    typ: a string that indicates the type of asset to look for eg. img stands image and ico stands for icon
    """
    types = {'img': 'images', 'ico': 'icons'}
    typ = types[typ]
    print(str(assets / typ / file))
    return str(assets / typ/file)


def homedir(typ='', initial=False):
    """
    Creates the home dir for storing app files and saved results
    :param initial: set to true during installation of app
    :param typ: the type of object to save. has two valid parameter 'i' for images or 'm' for the pdf manuals or '' for folders during
    :return: a Path object pointing to the home dir or None
    """
    folders = {'i': 'Images', 'm': 'Manuals', '': ''}
    folder = folders[typ]

    home_path = Path.home() / 'Documents/IPOM/'
    if not Path.exists(home_path) or initial:
        Path.mkdir(home_path / 'Manuals', parents=True)
        Path.mkdir(home_path / 'Images', parents=True)
        return home_path / folder

    if Path.exists(home_path / folder):
        return home_path / folder

    Path.mkdir(home_path / folder, parents=True)
    return home_path
