from pathlib import Path
import os


sp = Path(__file__).resolve().parent    # The Styles Path
styles = {f[:-4]: sp/f for f in os.listdir(sp) if f.endswith('.qss')}     # A dict of style files


def style(sf):
    """
    Reads the style from the stylesheet files in the stylesheets directory
    :param sf: sf a string parameter representing the name of the style file without the .qss extension
    :return: The style as a string
    """
    file = styles[sf]
    with open(file) as f:
        style_string = f.read()
    return style_string
