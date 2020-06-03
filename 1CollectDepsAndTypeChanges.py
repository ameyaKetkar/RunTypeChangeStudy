import subprocess
import os

def runLongCommand(s, cwd =''):
    if cwd == '':
        out = subprocess.Popen(s, stdout=subprocess.PIPE)
        out.stdout
        out.wait()
        o, e = out.communicate()
        return e, o
    else :
        out = subprocess.Popen(s, stdout=subprocess.PIPE, cwd = cwd)
        out.stdout
        out.wait()
        o, e = out.communicate()
        return e, o

projectPath = os.path.dirname(os.path.abspath(__file__))

from configparser import ConfigParser
config = ConfigParser()

config.read(os.path.join(projectPath,'config.ini'))

setupPath = config.get('main','path')

simpleTypechangeMiner = os.path.join(os.path.join(os.path.normpath(setupPath), 'TypeChangeStudy'), 'SimpleTypeChangeMiner')
os.chdir(simpleTypechangeMiner)

cmd = ['java', '-cp', 'lib/*', 'Runner']

result = runLongCommand(cmd, cwd = str(simpleTypechangeMiner))






