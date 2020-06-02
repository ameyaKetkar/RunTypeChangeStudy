import subprocess
import os



import os
projectPath = os.path.dirname(os.path.abspath(__file__))

from configparser import ConfigParser
config = ConfigParser()

config.read(os.path.join(projectPath,'config.ini'))

setupPath = config.get('main','path')

simpleTypechangeMiner = os.path.join(os.path.join(os.path.normpath(setupPath), 'TypeChangeStudy'), 'SimpleTypeChangeMiner')
os.chdir(simpleTypechangeMiner)

result = subprocess.run(['java', '-cp', '\"lib/*\"', 'Runner'], stdout=subprocess.PIPE)

result.stdout