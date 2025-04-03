#-------------------------------------------------------------------------------
# Name:        Git Pipeline
# Purpose:     Helper script for detecting the changed files and start the process in GaiaBuilder
#
# Author:      Merkator B.V.
#
# Created:     02-04-2025
# Copyright:   Merkator B.V.
#-------------------------------------------------------------------------------
import sys, os, git, logging, subprocess, time
from logging import FileHandler

class GIT2Gaia(object):
    mapservices = []
    gpservices = []
    content = []

    def analyzeChangedFiles(self,files):
        workdir = os. getcwd()
        for file in files:
            #test if content.json
            dirname = os.path.dirname(file)
            basename = os.path.basename(file)
            logging.info("analyzing {} {}".format(dirname,basename))
            aprx_basename = None
            test_path_aprx_json = None
            if basename.endswith(".mapx.json"):
                aprx_basename = basename.replace('.mapx.','.aprx.')
                test_path_aprx_json = os.path.join(workdir,dirname,aprx_basename)
            test_path_content_json = os.path.join(workdir,dirname,'content.json')
            test_path_gp_json = os.path.join(workdir,dirname,'gpservice.json')
            
            if file.endswith("content.json"):
                logging.info("Found the content.json")
                self.addToContent(file)
            elif os.path.exists(test_path_content_json):
                logging.info("Found the content.json in the same directory")
                self.addToContent(os.path.join(dirname,'content.json')) #pass relative path by joining dirname and content.json
            elif file.endswith("gpservice.json"):
                logging.info("Found the gpservice.json")
                self.addToGP(file)
            elif os.path.exists(test_path_gp_json):
                logging.info("Found the gpservice.json in the same directory")
                self.addToGP(os.path.join(dirname,'gpservice.json')) #pass relative path by joining dirname and gpservice.json
            elif file.endswith("aprx.json"):
                logging.info("Found the aprx.json")
                self.addToMapservice(file)
            elif test_path_aprx_json is not None and os.path.exists(test_path_aprx_json):
                logging.info("Found the {} based on {} ".format(test_path_aprx_json,basename))
                self.addToMapservice(os.path.join(dirname,aprx_basename)) #pass relative path by joining dirname and aprx_basename
            else:
                dir_content =os.listdir(os.path.join(workdir,dirname) )
                if len([x for x in dir_content if x.endswith(".aprx.json")]) ==1:#test if only one aprx.json is present
                    n = [x for x in dir_content if x.endswith(".aprx.json")][0]
                    self.addToMapservice(os.path.join(dirname,n))
                    logging.info("Found 1 aprx.json file in this directory")
                elif len([x for x in dir_content if x.endswith(".aprx.json")])>1:
                    logging.info("Multiple aprx.json files found, but the changed file couldn't be mapped")
                else:
                    logging.info("{} couldn't be mapped on a .aprx.json, gpservice.json or content.json".format(file) )


    def addToContent(self,file):
        file = file.replace('\\','/')
        if file not in self.content:
            self.content.append(file)
            logging.info("{} appended to content".format(file))
        else:
            logging.info("{} already exists in content".format(file))

    def addToGP(self,file):
        file = file.replace('\\','/')
        if file not in self.gpservices:
            self.gpservices.append(file)
            logging.info("{} appended to gpservices".format(file))
        else:
            logging.info("{} already exists in gpservices".format(file))

    def addToMapservice(self,file):
        file = file.replace('\\','/')
        if file not in self.mapservices:
            self.mapservices.append(file)
            logging.info("{} appended to mapservices".format(file))
        else:
            logging.info("{} already exists in mapservices".format(file))


    def getChangedFiles(self):
        logging.info("Python GIT version: {}".format(git.__version__))
        git_repo = git.Git()
        changed_filepaths = git_repo.execute(['git', 'diff-tree', '--name-only', '-r', '--no-commit-id', 'HEAD']).split('\n')
        for changed_filepath in changed_filepaths:
            logging.info("Changed file: {}".format(changed_filepath))
        return changed_filepaths

    def runGaiaBuilderForMapservices(self,server):
        totalresult = 0
        for c in self.mapservices:
            arguments = [os.path.join(os.path.dirname(__file__),'InstallMapservice_lite.py'), '-f', c, '-s', server, '-r', 'false', '-q', 'true', '-c',  'true', '-d', 'false', '-h', 'true', '-i', 'true', '-a', 'true', '-z', 'true', '-m', 'true', '-t', 'false']
            result = self.runGaiaBuilder(arguments=arguments)
            totalresult = totalresult + result
        return totalresult

    def runGaiaBuilderForGPservices(self,server):
        totalresult = 0
        for c in self.gpservices:
            arguments = [os.path.join(os.path.dirname(__file__),'InstallGeoProcessor_lite.py'), '-f', c, '-s', server]
            result = self.runGaiaBuilder(arguments=arguments)
            totalresult = totalresult + result
        return totalresult

    def runGaiaBuilderForContent(self,server):
        totalresult = 0
        for c in self.content:
            arguments = [os.path.join(os.path.dirname(__file__),'InstallContent_lite.py'), '-f', c, '-s', server]
            result = self.runGaiaBuilder(arguments=arguments)
            totalresult = totalresult + result
        return totalresult

    def runGaiaBuilder(self, arguments):
        python_location = sys.executable
        logging.info("Using Python from: {}".format(python_location))
        args = [python_location] + arguments
        logging.info("Arguments: {}".format(args))
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        for c in iter(lambda: process.stdout.read(1), b""):
            sys.stdout.buffer.write(c)
        while process.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)
        result = process.returncode
        logging.info(str(result))
        logging.info("*" *64)
        return result

    def execute(self):
        server = os.getenv('server')
        manual_build_list = os.getenv('manual_build_list')
        exitcode = 0
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logfile ='git2gaia.log'
        self.fileHandler = FileHandler(filename=logfile, mode='a', encoding=None, delay=False)
        logger.addHandler(self.fileHandler)
        if manual_build_list is not None and len(manual_build_list)>0:
            files = manual_build_list.split(",")
            self.analyzeChangedFiles([t.strip() for t in files])
        else:
            changed_filepaths = self.getChangedFiles()
            self.analyzeChangedFiles(changed_filepaths)
        mapserviceresult = self.runGaiaBuilderForMapservices(server)
        gpserviceresults = self.runGaiaBuilderForGPservices(server)
        contentresult = self.runGaiaBuilderForContent(server)
        exitcode = mapserviceresult + gpserviceresults + contentresult
        return exitcode

def main(argv):
    g2g = GIT2Gaia()

    exitcode = g2g.execute()    

    sys.exit(exitcode)



if __name__ == '__main__':
    main(sys.argv[1:])
#--------------------------------------------------------------------------------------------