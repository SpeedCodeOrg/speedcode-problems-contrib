import os
from pathlib import Path

ROOT_DIR = Path('.')
SOURCE_CODE_ROOT = Path('.')

if 'SPEEDCODE_SERVER' in os.environ and os.environ['SPEEDCODE_SERVER'] == '1':
    ROOT_DIR = Path('/box')
    SOURCE_CODE_ROOT = Path('/sandbox')
if 'SERVER_EXECUTION' in os.environ and os.environ['SERVER_EXECUTION'] == '1':
    ROOT_DIR = Path('/box')
    SOURCE_CODE_ROOT = Path('/sandbox')

