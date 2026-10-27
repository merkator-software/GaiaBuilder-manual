#-------------------------------------------------------------------------------
# Name:        Git Pipeline
# Purpose:     Helper script for detecting the changed files and start the process in GaiaBuilder
#
# Author:      Merkator B.V.
#
# Created:     02-04-2025
# Copyright:   Merkator B.V.
#-------------------------------------------------------------------------------
import sys, os, git, logging, subprocess, time, glob, re
from logging import FileHandler

class GIT2Gaia(object):
    mapservices = []
    gpservices = []
    content = []
    portalconfig = []
    includecontent = '1'
    publish_sd_to_online = '1'
    rewrite_connection = '1'

    def getChangedFiles(self):
        logging.info("Python GIT version: {}".format(git.__version__))
        # Check whether we're running in a GitLab CI environment
        # CI_COMMIT_SHA is the current commit, CI_COMMIT_BEFORE_SHA is the one before it.
        before_sha = os.getenv('CI_COMMIT_BEFORE_SHA')
        current_sha = os.getenv('CI_COMMIT_SHA')
        git_repo = git.Git()
        if before_sha and before_sha != "0000000000000000000000000000000000000000":
            logging.info(f"GitLab CI detected. Comparing {before_sha} to {current_sha}")
            # Compare the state before the push to the current state
            changed_filepaths = git_repo.execute(['git', 'diff', '--name-only', before_sha, current_sha]).split('\n')
        else:
            # Default: diff the files changed in the current HEAD commit
            logging.info("No GitLab CI variables found, falling back to git diff-tree")
            changed_filepaths = git_repo.execute(['git', 'diff-tree', '--name-only', '-r', '--no-commit-id', 'HEAD']).split('\n')
        # Filter out empty lines
        changed_filepaths = [f for f in changed_filepaths if f.strip()]
        for changed_filepath in changed_filepaths:
            logging.info("Changed file: {}".format(changed_filepath))
        return changed_filepaths

    def expandBuildListEntry(self,entry):
        # "*" -> all .json files in the working directory (recursive)
        # "folder/*" -> all .json files under that folder (recursive, nesting allowed, e.g. "a/b/c/*")
        # anything else -> returned as-is (a specific file)
        e = entry.strip()
        if e == "":
            return []
        if e == "*":
            return glob.glob(os.path.join("**","*.json"), recursive=True)
        match = re.match(r'^(.+)[\\/]\*$', e)
        if match:
            folder = match.group(1)
            if not os.path.isdir(folder):
                logging.info("Folder '{}' does not exist, skipping entry '{}'".format(folder,e))
                return []
            logging.info("Scanning folder '{}' for json files".format(folder))
            return glob.glob(os.path.join(folder,"**","*.json"), recursive=True)
        return [e]

    def findConfigUpward(self,fulldir,filename):
        current = os.path.abspath(fulldir)
        while True:
            parent = os.path.dirname(current)
            if parent == current:
                return None
            current = parent
            candidate = os.path.join(current,filename)
            if os.path.exists(candidate):
                return candidate

    def analyzeChangedFiles(self,files):
        workdir = os. getcwd()
        for file in files:
            #test if content.json
            dirname = os.path.dirname(file)
            basename = os.path.basename(file)
            logging.info("analyzing {} {}".format(dirname,basename))
            fulldir = os.path.join(workdir,dirname)
            aprx_basename = None
            test_path_aprx_json = None
            if basename.endswith(".mapx.json"):
                aprx_basename = basename.replace('.mapx.','.aprx.')
                test_path_aprx_json = os.path.join(fulldir,aprx_basename)
            test_path_portalconfig_json = os.path.join(fulldir,'portalconfig.json')
            test_path_content_json = os.path.join(fulldir,'content.json')
            test_path_gp_json = os.path.join(fulldir,'gpservice.json')

            if file.endswith("aprx.json"):
                logging.info("Found the aprx.json")
                self.addToMapservice(file)
            elif test_path_aprx_json is not None and os.path.exists(test_path_aprx_json):
                logging.info("Found the {} based on {} ".format(test_path_aprx_json,basename))
                self.addToMapservice(os.path.join(dirname,aprx_basename)) #pass relative path by joining dirname and aprx_basename
            elif file.endswith("portalconfig.json"):
                logging.info("Found the portalconfig.json")
                self.addToPortalConfig(file)
            elif os.path.exists(test_path_portalconfig_json):
                logging.info("Found the portalconfig.json in the same directory")
                self.addToPortalConfig(os.path.join(dirname,'portalconfig.json')) #pass relative path by joining dirname and portalconfig.json
            elif self.findConfigUpward(fulldir,'portalconfig.json') is not None:
                logging.info("Found the portalconfig.json in a parent directory")
                self.addToPortalConfig(self.findConfigUpward(fulldir,'portalconfig.json'))
            elif file.endswith("content.json"):
                logging.info("Found the content.json")
                self.addToContent(file)
            elif os.path.exists(test_path_content_json):
                logging.info("Found the content.json in the same directory")
                self.addToContent(os.path.join(dirname,'content.json')) #pass relative path by joining dirname and content.json
            elif self.findConfigUpward(fulldir,'content.json') is not None:
                logging.info("Found the content.json in a parent directory")
                self.addToContent(self.findConfigUpward(fulldir,'content.json'))
            elif file.endswith("gpservice.json"):
                logging.info("Found the gpservice.json")
                self.addToGP(file)
            elif os.path.exists(test_path_gp_json):
                logging.info("Found the gpservice.json in the same directory")
                self.addToGP(os.path.join(dirname,'gpservice.json')) #pass relative path by joining dirname and gpservice.json
            elif self.findConfigUpward(fulldir,'gpservice.json') is not None:
                logging.info("Found the gpservice.json in a parent directory")
                self.addToGP(self.findConfigUpward(fulldir,'gpservice.json'))
            else:
                dir_content =os.listdir(fulldir)
                if len([x for x in dir_content if x.endswith(".aprx.json")]) ==1:#test if only one aprx.json is present
                    n = [x for x in dir_content if x.endswith(".aprx.json")][0]
                    self.addToMapservice(os.path.join(dirname,n))
                    logging.info("Found 1 aprx.json file in this directory")
                elif len([x for x in dir_content if x.endswith(".aprx.json")])>1:
                    logging.info("Multiple aprx.json files found, but the changed file couldn't be mapped")
                else:
                    logging.info("{} couldn't be mapped on a .aprx.json, gpservice.json, content.json or portalconfig.json".format(file) )


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

    def addToPortalConfig(self,file):
        file = file.replace('\\','/')
        if file not in self.portalconfig:
            self.portalconfig.append(file)
            logging.info("{} appended to portalconfig".format(file))
        else:
            logging.info("{} already exists in portalconfig".format(file))

    def addToMapservice(self,file):
        file = file.replace('\\','/')
        if file.endswith(".online.aprx.json") and self.publish_sd_to_online == "0":
            logging.info("Found ArcGIS Online configuration file, skipping {} because publishing to Online is blocked".format(file))
            return
        if file not in self.mapservices:
            self.mapservices.append(file)
            logging.info("{} appended to mapservices".format(file))
        else:
            logging.info("{} already exists in mapservices".format(file))


    def getServersForFile(self,buildfile,server):
        python_location = sys.executable
        script = os.path.join(os.path.dirname(__file__),'GaiaBuilder.py')
        args = [python_location, script, '-f', buildfile, '-a', 'listservers', '-q', server]
        logging.info("Resolving servers for {}: {}".format(buildfile,args))
        output = subprocess.check_output(args, universal_newlines=True)
        servers = [s.strip() for s in output.split(',') if s.strip()]
        logging.info("Resolved servers for {}: {}".format(buildfile,servers))
        return servers

    def runGaiaBuilderForPortalConfig(self,server):
        totalresult = 0
        for c in self.portalconfig:
            for s in self.getServersForFile(c,server):
                arguments = [os.path.join(os.path.dirname(__file__),'ConfigurePortal.py'), '-f', c, '-s', s, '-a', 'configure']
                result = self.runGaiaBuilder(arguments=arguments)
                totalresult = totalresult + result
        return totalresult

    def runGaiaBuilderForMapservices(self,server):
        totalresult = 0
        restore_args = ['-q','true'] if self.rewrite_connection == '1' else []
        for c in self.mapservices:
            for s in self.getServersForFile(c,server):
                arguments = [os.path.join(os.path.dirname(__file__),'InstallMapservice_lite.py'), '-f', c, '-s', s, '-r', 'false'] + restore_args + ['-c',  'true', '-d', 'false', '-h', 'true', '-i', 'true', '-a', 'true', '-z', 'true', '-m', 'true', '-t', 'false']
                result = self.runGaiaBuilder(arguments=arguments)
                totalresult = totalresult + result
        return totalresult

    def runGaiaBuilderForGPservices(self,server):
        totalresult = 0
        for c in self.gpservices:
            for s in self.getServersForFile(c,server):
                arguments = [os.path.join(os.path.dirname(__file__),'InstallGeoProcessor_lite.py'), '-f', c, '-s', s]
                result = self.runGaiaBuilder(arguments=arguments)
                totalresult = totalresult + result
        return totalresult

    def runGaiaBuilderForContent(self,server):
        totalresult = 0
        for c in self.content:
            for s in self.getServersForFile(c,server):
                arguments = [os.path.join(os.path.dirname(__file__),'InstallContent_lite.py'), '-f', c, '-s', s]
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
        self.includecontent = os.getenv('includecontent','1')
        self.publish_sd_to_online = os.getenv('publish_sd_to_online','1')
        self.rewrite_connection = os.getenv('rewrite_connection','1')
        fail_on_empty_manual_build_list = os.getenv('fail_on_empty_manual_build_list','1')
        exitcode = 0
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logfile ='git2gaia.log'
        self.fileHandler = FileHandler(filename=logfile, mode='a', encoding=None, delay=False)
        logger.addHandler(self.fileHandler)
        manual_build_used = manual_build_list is not None and len(manual_build_list)>0
        if manual_build_used:
            logging.info("Activating manual build from list")
            files = []
            for entry in manual_build_list.split(","):
                files = files + self.expandBuildListEntry(entry)
            self.analyzeChangedFiles(files)
        else:
            changed_filepaths = self.getChangedFiles()
            self.analyzeChangedFiles(changed_filepaths)

        total_queued = len(self.portalconfig) + len(self.mapservices) + len(self.gpservices) + len(self.content)
        if manual_build_used and total_queued == 0 and fail_on_empty_manual_build_list == '1':
            logging.error("manual_build_list was specified but no files could be resolved to a map service, geoprocessing service, content, or portal config item. Failing the build.")
            return 1

        portalconfigresult = self.runGaiaBuilderForPortalConfig(server)
        mapserviceresult = self.runGaiaBuilderForMapservices(server)
        gpserviceresults = self.runGaiaBuilderForGPservices(server)
        contentresult = 0
        if self.includecontent != "0":
            contentresult = self.runGaiaBuilderForContent(server)
        else:
            logging.info("includecontent is 0, skipping content publish")
        exitcode = portalconfigresult + mapserviceresult + gpserviceresults + contentresult
        return exitcode

def main(argv):
    g2g = GIT2Gaia()

    exitcode = g2g.execute()

    sys.exit(exitcode)



if __name__ == '__main__':
    main(sys.argv[1:])
#--------------------------------------------------------------------------------------------
