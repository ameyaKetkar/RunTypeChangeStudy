import shutil as sh
import os

from configparser import ConfigParser
from os.path import dirname, abspath, join, normpath

config = ConfigParser()

projectPath = dirname(abspath(__file__))

config.read(join(projectPath, 'config.ini'))

setupPath = join(normpath(config.get('main', 'path')), "TypeChangeStudy")

stcm_output = join(join(setupPath, 'SimpleTypeChangeMiner'), "Output")

tcm_input = join(join(setupPath, 'TypeChangeMiner'), "Input")

tcm_output = join(join(setupPath, 'TypeChangeMiner'), "Output")

pr1 = join(join(join(join(setupPath, 'SimpleTypeChangeMiner'), "Output"), "ProtosOut"), "projects.txt")
pr2 = join(join(join(join(setupPath, 'SimpleTypeChangeMiner'), "Output"), "ProtosOut"), "projectsBinSize.txt")


sh.copytree(stcm_output, tcm_input)
sh.copy(pr1, tcm_output)
sh.copy(pr2, tcm_output)
