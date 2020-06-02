import os
import os.path as osp
import subprocess
import sys

import boto3

import javaproperties
from javaproperties import Properties
from botocore import UNSIGNED
from botocore.client import Config

import os
projectPath = os.path.dirname(os.path.abspath(__file__))

TypeChangeMiner = "TypeChangeMiner"
SimpleTypeChangeMiner = "SimpleTypeChangeMiner"
DataAnalysis = "DataAnalysis"
typeChangeMinerURL = "https://github.com/ameyaKetkar/TypeChangeMiner.git"
simpleTypeFactMinerURL = "https://github.com/ameyaKetkar/SimpleTypeChangeMiner.git"
dataAnalysisURL = 'https://github.com/ameyaKetkar/DataAnalysis.git'

systemArgs = sys.argv




def setupAt(path, mavenHome='/usr/local/Cellar/maven/3.6.3', project={'guice': 'https://github.com/google/guice.git'}):

    

    print('Setup started!!!')


    from configparser import ConfigParser
    config = ConfigParser()

    config.read('config.ini')
    config.add_section('main')


    inputProjects = {}
    if len(systemArgs) > 3 and (len(systemArgs) - 3) % 2 == 0:
        path = systemArgs[1]
        mavenHome = systemArgs[2]
        counter = 3
        while counter < len(systemArgs):
            inputProjects[systemArgs[counter]] = systemArgs[counter + 1]
            counter += 2
        if(len(inputProjects) > 0):
            project = inputProjects

    typechangestudy = osp.join(path, "TypeChangeStudy")
    config.set('main', 'path', path)
    config.set('main', 'mavenHome', mavenHome)


    os.chdir(osp.normpath(path))

    addDirectoryIfNotExists(typechangestudy)

    corpus = osp.join(typechangestudy, 'Corpus')

    projectsToanalyse = ''
    for k, v in project.items():
        projectsToanalyse += k + ',' + v + "\n"
    projectsToanalyse = projectsToanalyse[:len(projectsToanalyse) - 1]

    if not osp.isdir(corpus):
        os.mkdir(corpus)
        inputProjectsCsv = osp.join(corpus, 'mavenProjectsAll.csv')
        config.set('main', 'projectPath', str(inputProjectsCsv) )
        with open(inputProjectsCsv, 'w') as f:
            f.write(projectsToanalyse)
            f.close()



    type_change_miner = osp.join(typechangestudy, TypeChangeMiner)
    simple_typechange_miner = osp.join(typechangestudy, SimpleTypeChangeMiner)

    if not osp.isdir(simple_typechange_miner):
        print('Cloning ', simpleTypeFactMinerURL)
        import git
        git.Git(typechangestudy).clone(simpleTypeFactMinerURL)
        print('Cloning Complete!')
    os.chdir(simple_typechange_miner)

    output = osp.join(simple_typechange_miner, "Output")

    addDirectoryIfNotExists(output)
    addDirectoryIfNotExists(osp.join(output, "ProtosOut"))
    addDirectoryIfNotExists(osp.join(output, "tmp"))
    addDirectoryIfNotExists(osp.join(output, "dependencies"))

    if not osp.isdir(type_change_miner):
        print('Cloning ', typeChangeMinerURL)
        import git
        git.Git(typechangestudy).clone(typeChangeMinerURL)
        print('Cloning complete!!!')

    os.chdir(type_change_miner)

    output = osp.join(type_change_miner, "Output")

    addDirectoryIfNotExists(output)

    inp = osp.join(type_change_miner, "Input")

    addDirectoryIfNotExists(inp)

    updatePropertyFile(typechangestudy, simple_typechange_miner, mavenHome)
    updatePropertyFile(typechangestudy, type_change_miner)
    os.chdir(typechangestudy)
    downloadGremlinServer(typechangestudy)

    dataAnalysis = osp.join(typechangestudy, DataAnalysis)
    if not osp.isdir(dataAnalysis):
        print('Cloning ', dataAnalysisURL)
        import git
        from git import Repo
        Repo.clone_from(dataAnalysisURL, dataAnalysis, recursive=True)
        print('Cloning complete')


    with open(os.path.join(projectPath,'config.ini'), 'w') as f:
        config.write(f)
    print()


def addDirectoryIfNotExists(dir):
    if not osp.isdir(dir):
        os.mkdir(dir)
        print('Created the directory: ', str(dir))


def updatePropertyFile(path, stcm, mavenPath=''):
    jp = Properties()
    jp.load(open(osp.join(stcm, 'paths.properties')))

    newProperties = {}
    for k, v in jp.items():
        if k == 'mavenHome':
            if not mavenPath == '':
                newProperties[k] = mavenPath
        elif k == 'PathToSetup':
            newProperties[k] = path
        else:
            newProperties[k] = v

    with open(osp.join(stcm, 'paths.properties'), 'w') as f:
        javaproperties.dump(newProperties, f)


# https://changetype.s3.us-east-2.amazonaws.com/docs/apache-tinkerpop-gremlin-server-3.4.4.zip

def downloadGremlinServer(typechangestudy):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    if not osp.isfile(osp.join(typechangestudy, 'apache-tinkerpop-gremlin-server-3.4.4.zip')):
        print('Downloading ', 'apache-tinkerpop-gremlin-server-3.4.4.zip')
        s3.download_file('changetype', 'docs/apache-tinkerpop-gremlin-server-3.4.4.zip',
                         'apache-tinkerpop-gremlin-server-3.4.4.zip')
        print('Download complete!!!')
    if not osp.isdir(osp.join(typechangestudy, 'apache-tinkerpop-gremlin-server-3.4.4')):
        import zipfile
        print('Unzipping ', 'apache-tinkerpop-gremlin-server-3.4.4.zip')
        with zipfile.ZipFile(osp.join(typechangestudy, 'apache-tinkerpop-gremlin-server-3.4.4.zip'), 'r') as zip_ref:
            dir = os.mkdir(osp.join(typechangestudy, 'apache-tinkerpop-gremlin-server-3.4.4'))
            zip_ref.extractall(dir)
            print('Unzip complete')
    print()


def runLongCommand(s):
    out = subprocess.Popen(s, stdout=subprocess.PIPE)
    out.wait()
    o, e = out.communicate()
    return e, o


setupAt('/Users/ameya/Research/Test')
