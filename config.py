# Window screen configurations
WIDTH = 500
HEIGHT = 500

# Time configurations
FPS = 60

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# This part of the config file will be used for 
# access directories,mainly thought for the assets
# directory
from pathlib import Path

BASE_DIR = Path(__file__).parent

# This is for the asset's directory
ASSETS_DIR = Path = BASE_DIR / "Assets"
FONTS_DIR = Path = BASE_DIR / "Fonts"
