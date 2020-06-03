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

def run_command(command, cwd = ''):
    if cwd == '' :
        p = subprocess.Popen(command,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')
    else:
        p = subproc ess.Popen(command,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     ced =cwd)
        return iter(p.stdout.readline, b'')



projectPath = os.path.dirname(os.path.abspath(__file__))

from configparser import ConfigParser
config = ConfigParser()

config.read(os.path.join(projectPath,'config.ini'))

setupPath = config.get('main','path')

simpleTypechangeMiner = os.path.join(os.path.join(os.path.normpath(setupPath), 'TypeChangeStudy'), 'SimpleTypeChangeMiner')
os.chdir(simpleTypechangeMiner)

cmd = ['java', '-cp', 'lib/*', 'Runner']

result = run_command(cmd, cwd = str(simpleTypechangeMiner))







