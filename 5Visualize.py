import subprocess
import os
import os



def execute(cmd, cwd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, cwd=cwd)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)



projectPath = os.path.dirname(os.path.abspath(__file__))

from configparser import ConfigParser
config = ConfigParser()

config.read(os.path.join(projectPath,'config.ini'))

setupPath = config.get('main','path')

dataAnalysis = os.path.join(os.path.join(os.path.normpath(setupPath), 'TypeChangeStudy'), 'DataAnalysis')
os.chdir(dataAnalysis)

cmd = ['python ToHtml.py']

for result in execute(cmd, str(dataAnalysis)):
    print(result)