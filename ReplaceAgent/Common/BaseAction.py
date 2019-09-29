import os.path
from os import listdir
import time
from ReplaceAgent.Common.RemoteMachine import RemoteMachine
from ReplaceAgent.Common.ConfigFile import  ConfigFile
from ReplaceAgent.Common.RemoteMachine_Windows import RemoteMachine_Windows
import shutil
import datetime

class BaseAction:
    File = ConfigFile()
    #Methods for Local machine
    1.#Get All files path from a folder
    def getLocalFilesPath(self,folder):
        files = []
        if  os.path.isdir(folder):
            print("start to get all files path...")
            for index in range(len(listdir(folder))):
                if os.path.isfile(os.path.join(folder,listdir(folder)[index])):
                    files.append(os.path.join(folder,listdir(folder)[index]))
            if len(files)!= 0:
                print("files get...")
                print (files)
            else:
                print("Cannot find any files in current folder！")
        else:
            print("Its not a path, please check!")
        return files

    2.#Get All files name from a folder
    def getLocalFilesName(selfs,folder):
        filename = []
        if os.path.isdir(folder):
            print("start to get all files name...")
            if len(os.listdir(folder))!= 0:
                filename = os.listdir(folder)
                print(filename)
            else:
                print("No files found under current folder")
        else:
            print("Its not a path, please check!")
        return filename

    3.#Create foler if the folder is not found
    def createLocalFolder(self,folder):
        if(os.path.isdir(folder)):
            print("Folder " + folder + " already exist!")
        else:
            print("folder " + folder + " not exist, start to create")
            os.mkdir(folder)

    4.#Generate target path by name
    def replaceFilesPath_ByName(self,folder,filename):
        targetfilepath = []
        print("start to replace the files path...")
        for index in range(len(filename)):
            targetfilepath.append(os.path.join(folder, filename[index]))
        print("replace files path done...")
        print(targetfilepath)
        return targetfilepath

    5.#Delete Local Folder
    def deleteLocalFolder(self,folder):
        print("Trying to delete local folder")
        if os.path.exists(folder):
            print("folder already exist!")
            shutil.rmtree(folder,ignore_errors=True)
        else:
            print("folder is not found!")

    6.#Copy folders to folders
    def CopyFolderTreesToFolders(self,sourcefolder,TargetFolder):
        print("trying to copy files or directory from "+ sourcefolder + " to " + TargetFolder)
        shutil.copytree(sourcefolder,TargetFolder)

    7.#copy file to file
    def CopyFile(self, filepath, targetfilepath):
        print("start to copy file "+filepath+ " to " + targetfilepath)
        shutil.copy(filepath,targetfilepath)

    #Bussiness Call
    1.#Agent Signing on Mac
    def AgentSigning(self,TargetServer,tmp_folder_name):
        self.getRemoteFilePath(tmp_folder_name, TargetServer)
    # Copy the hpmc enabler from mac to foler in order to perform codesign
        cmd = "cp -f "+ TargetServer.ip +"HPMCEnabler " + tmp_folder_name + "HPMCEnabler"
        self.executeCommand(TargetServer, cmd)
        cmd = "cd " + tmp_folder_name +"\n chmod +x HPMCEnabler"
        self.executeCommand(TargetServer, cmd)
        self.appCodesign_instrument(0, tmp_folder_name, TargetServer)

    2.#Silent Install MC server on Target Machine

    3.#File upload to remote win/linux/mac server

    4.#CreateRemoteTempFolder both linux-windows

    5.#DownloadFilesFromFTP both linux-windows

    6.#RemoteFileDelete both linux-windows

    7.#RemoteConfiglFileTransfer both linux-windows linux transfer thtrough sftp windows generate on local

    #Common Base Methods
    1.#Generate scenario.no for each user
    def generateScenarioNo(self):
        scenarioNo = "No" + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        return scenarioNo

    2.#ConfigFile
    def ConfigFile(self):
        f = ConfigFile()
        return f

    3.#spilt specific path to filepath and filename
    def switchToPathAndName(self,path):
        filename = ""
        filepath = ""
        if(path.count("\\")>=1):
            path = path.replace("\\","/")
        if(path != "./"):
            if(path.count("/")==1):
                filepath = os.path.dirname(path)
                filename = path.replace(filepath,"")
                if(filename.count(".")==0 and filename!="" and filepath != "./"):
                    filepath = filepath + filename + "/"
                    filename = ""
            elif(path.count("/")>=2):
                filepath = os.path.dirname(path) + "/"
                filename = path.replace(filepath,"")
                if(filename.count(".")==0 and filename!=""):
                    filepath = filepath + filename + "/"
                    filename = ""
            else:
                print("this is not path!")
        else:
            filepath = "./"
            filename = ""
        print (filepath + "\n")
        print (filename)
        return filepath, filename

    #Linux Methods
    1.# Transport files from local folder to remote folder or upload local files to remote files
    def fileUpload(self,folder_local,folder_remote,Target_server):
        #if both are folder perform file transfer folder to folder
        file_local = []
        file_remote= []
        if(isinstance(folder_local, str) and isinstance(folder_remote, str)):
            print("Both are folder")
            self.createLocalFolder(folder_local)
            file_local = self.getLocalFilesPath(folder_local)
            file_remote = self.replaceFilesPath_ByName(folder_remote,self.getLocalFilesName(folder_local))
            # check remote folder exist or not, if not create one
            self.remoteFolderCreate(folder_remote,Target_server)
        #if both are file list peform files to files
        elif(len(folder_local)!=0 and len(folder_local)==len(folder_remote)):
            print("Both are valid file lists")
            file_local = folder_local
            file_remote = folder_remote
        else:
            print("Input have some issue, please check!")
            return
        Target_server.uploadFiles(file_local,file_remote)
        print("File transfer successfully!")

    2.#Create remote folder if the folder is not found
    def remoteFolderCreate(self,folder,Target_server):
        print("start to check whether the folder is exsit or not")
        if Target_server.fileCheck(folder):
            print("folder exist")
        else:
            print("folder is not exist start to create...")
            cmd = "mkdir " + folder
            Target_server.CommandExecute(cmd)

    3.#Remote Machine create instance Linux
    def remoteServer(self, ip, username, password,port):
        return RemoteMachine(ip, username, password,port)

    4.# Transport file from remote folder to local folder
    def fileDownload(self,folder_remote,folder_local,Target_server):
        #if both are folder perform file transfer folder to folder
        file_local = []
        file_remote= []
        if(isinstance(folder_local, str) and isinstance(folder_remote, str)):
            print("Both are folder")
            file_remote = self.getRemoteFilePath(folder_remote,Target_server)
            tmp = self.getRemoteFileName(folder_remote, Target_server)
            for index in range(len(tmp)):
                file_local.append(folder_local + tmp[index])
         #if both are file list peform files to files
        elif(len(folder_local)!=0 and len(folder_local)==len(folder_remote)):
            print("Both are valid file lists")
            file_local = folder_local
            file_remote = folder_remote
        else:
            print("Input have some issue, please check!")
            return
        Target_server.getFiles(file_remote, file_local)
        print("File transfer successfully!")

    5.#Get Remote File path
    def getRemoteFilePath(self,folder,Target_server):
        if Target_server.fileCheck(folder):
           print("folder exist start to get file path...")
           line = Target_server.CommandExecute('cd %s \n ls | sed \"s:^:`pwd`/:\"'%(folder))
        else:
           print("folder is not exist fail to get file path.")
           line = []
        return line

    6.#Perform code sign action for apps
    def appCodesign_instrument(self,mode,remote_folder,Target_server):
         if mode == 0:
             print("Mode 0 detected Only code sign apps")
             tmp = self.getRemoteFilePath(remote_folder,Target_server)
             if len(tmp)!= 0:
                 print("detect files start to codesign files...")
                 for index in range(len(tmp)):
                     cmd = "cd " + remote_folder + " \n security unlock-keychain -p "+ Target_server.password+ "\n./HPMCEnabler " + tmp[index] + " -c \"iPhone Developer: Arnaud Clement (TCX7NF2V9B)\" -p /Users/qamcteam/Desktop/MC_QA_Devices.mobileprovision"
                     print("command run: "+cmd)
                     Target_server.CommandExecute(cmd)
         elif mode == 1:
             print("Mode 1 detected manul instrument apps")
         else:
             print("Invalid mode number")

    7.#Get Remote File Name
    def getRemoteFileName(self,folder,Target_server):
        line = Target_server.CommandExecute('cd %s \n ls ' % (folder))
        return line

    8.#Remote folder delete
    def remoteFolderDelete(self,folder,Target_server):
        print("start to check whether the folder is exsit or not")
        if Target_server.fileCheck(folder):
            print("folder exist")
            cmd = "rm -rf " + folder
            Target_server.CommandExecute(cmd)
        else:
            print("folder is not exist")

    9.#Execute command
    def executeCommand(self,Target_server,cmd):
        print("trying to perform a command with paramiko...")
        Result = Target_server.CommandExecute(cmd)
        return Result

    10.#Create remote folder if the folder is not found
    def remoteFolderCreate(self,folder,Target_server):
        print("start to check whether the folder is exsit or not")
        if Target_server.fileCheck(folder):
            print("folder exist")
        else:
            print("folder is not exist start to create...")
            cmd = "mkdir " + folder
            Target_server.CommandExecute(cmd)




    #Windows Methods
    1.#reate Remote File upload windows
    def fileUploadFTP_win(self,folder_local,folder_remote,Target_server):
        if(isinstance(folder_local, str) and isinstance(folder_remote, str)):
            print("Both are folder")
            self.createLocalFolder(folder_local)
            file_local = self.getLocalFilesPath(folder_local)
            file_remote = self.replaceFilesPath_ByName(folder_remote,self.getLocalFilesName(folder_local))
            # check remote folder exist or not, if not create one
            self.remoteFolderCreateFTP_win(folder_remote,Target_server)


        #if both are file list peform files to files
        elif(len(folder_local)!=0 and len(folder_local)==len(folder_remote)):
            print("Both are valid file lists")
            file_local = folder_local
            file_remote = folder_remote
        else:
            print("Input have some issue, please check!")
        for index in range(len(file_local)):
            Target_server.WinFileUploadFTP(file_local[index],file_remote[index])
        print("File transfer successfully!")


    2.#Execute command windows #wait
    def executeCommand_win(self,Target_server,cmd, type = "ps"):
        print("trying to perform a command with pywinrm...")
        if(type == "ps"):
            print("calling win powershell。。。。")
            return Target_server.winPowserShellExecute(cmd)
        elif(type == "Batch"):
            print("calling win batch file。。。")
            return Target_server.WinBatchCommandExecute(cmd)

    3. #Remote folder delete windows
    def remoteFolderDeleteFTP_win(self,folder,Target_server):
        print("start to delete folder on remote ftp")
        Target_server.WinFolderDelete(folder)

    4. #Remote folder create windows
    def remoteFolderCreateFTP_win(self,folder,Target_server):
        print("start to check whether the folder is exsit or not")
        filepathExist, fileExist = Target_server.WinFileCheckFTP(folder)
        if filepathExist:
            print("folder exist")
        else:
            print("folder is not exist start to create...")
            Target_server.WinCreateFolderFTP(folder)
            for i in range(5):
                time.sleep(1)
                if(self.remoteFileCheckFTP_Win(Target_server,folder)):
                    print("folder create successfully!")
                    break


    5.#Remote machine create instance windwos
    def remoteServer_win(self, ip, username, password,port="21",type = ""):
        RemoteWin = RemoteMachine_Windows(ip, username, password,port)
        if(type == "FTP"):
            RemoteWin.FTPConnection()
        else:
            RemoteWin.WinSessionCreate()
        return RemoteWin

    6.#remote batch file generate windows giving the list of ftppath add them into the batch file folder
    def remoteBatchFileGenerate_win(self, Remote_folder, ftp_filepathlist, Target_server, FTP_Server, type = "get", Target_Folder_path = ""):
        print("start to generate bat file on " + Target_server.ip + " under folder "+ Remote_folder)
        gotoftpfoldercmd = ""
        if(self.remoteFileCheck_Win(Target_server,Remote_folder)):
            print("folder "+Remote_folder+ " is found")
        else:
            print("folder "+Remote_folder+" is not found, start create!")
            self.remoteCreateFolder_win(Target_server, Remote_folder)
        if(type == "put" and Target_Folder_path !="" ):
            gotoftpfoldercmd = "cd \"" + Target_Folder_path + "\""
        gotofoldercmd = "cd "+ Remote_folder +"\n"
        createfilecmd = "New-Item -Path . -Name 'download.bat' -ItemType 'file'\n"
        addContentcmd1 = "Add-Content download.bat '@echo off'\n"+\
                        "Add-Content download.bat 'echo open "+FTP_Server.ip+">ftp.txt'\n"+\
                        "Add-Content download.bat 'echo "+FTP_Server.username+">>ftp.txt'\n"+\
                        "Add-Content download.bat 'echo "+FTP_Server.password+">>ftp.txt'\n" +\
                        "Add-Content download.bat 'echo " + gotoftpfoldercmd+">>ftp.txt'\n"
        #add all files in the ftp_filepath list

        addContentcmd2 = ""
        for index in range(len(ftp_filepathlist)):
            addContentcmd2 = addContentcmd2 + "Add-Content download.bat 'echo "+type+" \""+ftp_filepathlist[index]+"\">>ftp.txt'\n"
        addContentcmd3 = "Add-Content download.bat 'echo bye>>ftp.txt'\n"+\
                         "Add-Content download.bat 'ftp -s:ftp.txt'\n"
        addContentcmd = addContentcmd1 + addContentcmd2 + addContentcmd3
        cmd = gotofoldercmd + createfilecmd + addContentcmd
        print("execute command: "+gotofoldercmd+createfilecmd+addContentcmd)
        return self.executeCommand_win(Target_server, cmd)


    7.#Create remote folder on windwos
    def remoteCreateFolder_win(self,Target_server, folder_path):
        print("start to create folder on remote windows server "+ Target_server.ip)
        return self.executeCommand_win(Target_server, "mkdir "+ folder_path +"\n")

    8.#Delete remote folder on winodws
    def remoteDeleteFile_win(self,Target_server,folder_path):
        print("start to delete current file on remote windows server "+ Target_server.ip)
        return self.executeCommand_win(Target_server, "rm -r "+folder_path+"\n")

    9.#Check file exist on current server windows
    def remoteFileCheck_Win(self,Target_server,folder_path):
        print("start to check the file is on current server or not! " + Target_server.ip)
        result = self.executeCommand_win(Target_server,"Test-Path -Path "+ "\""+folder_path+"\"")
        print("this result is " + result)
        if(result == "True\r\n"):
            print("File found!")
            print(result)
            return True
        else:
            print("File not found!")
            print(result)
            return False

    10.#unzip file on current server windows
    #def remoteFileUnzip_win(self,Target_server,folder_path,target_path, toolpath):
       #try:
           # print("start to unzip file " + folder_path)
            #gotofoldercmd = "cd "+ toolpath + "\n"
            #unzipfile = "./7z.exe e"
                        #+ " e " + folder_path + " \n"
            #cmd = gotofoldercmd + unzipfile
            #print(cmd)
            #self.executeCommand_win(Target_server, cmd)
        #except Exception as error:
            #print('Caught this error: ' + repr(error) + " ,unzip file failed!")
            #return False

    11.#check folder or file exist
    def remoteFileCheckFTP_Win(self,Target_server,folder_path):
        filepathexist, filenamexist = Target_server.WinFileCheckFTP(folder_path)
        if(os.path.isfile(folder_path)):
            print("string input is file")
            if(filepathexist and filenamexist):
                print("file exist")
                return True
            else:
                print("file not exist")
                return False
        else:
            print("string input is folder")
            if(filepathexist):
                print("folder exit")
                return True
            else:
                return False


    12.#file download from ftp server
    def fileDownloadFTP_win(self, folder_remote, folder_local, Target_server):
        file_local = []
        file_remote = []
        if(isinstance(folder_local, str) and isinstance(folder_remote, str)):
            print("Both are folder")
            self.createLocalFolder(folder_local)
            file_local = self.getLocalFilesPath(folder_local)
            file_remote = self.replaceFilesPath_ByName(folder_remote,self.getLocalFilesName(folder_local))
            # check remote folder exist or not, if not create one
            self.remoteFolderCreateFTP_win(folder_remote,Target_server)

        #if both are file list peform files to files
        elif(len(folder_local)!=0 and len(folder_local)==len(folder_remote)):
            print("Both are valid file lists")
            file_local = folder_local
            file_remote = folder_remote
        else:
            print("Input have some issue, please check!")
            return
        for index in range(len(file_local)):
            Target_server.WinGetFilesFTP(file_remote[index] ,file_local[index])
        print("File download successfully!")
    13.#Copy remote file from one position to another
    def fileCopy_win(self, file_currentposition, file_targetpostion, Target_server):
        try:
            if(self.remoteFileCheck_Win(Target_server, file_currentposition)):
                print("file exist trying to moving to "+ file_currentposition)
                cmd = "Copy-Item " + file_currentposition +" -Destination "+ "\"" + file_targetpostion + "\"" + " -Force"
                self.executeCommand_win(Target_server, cmd)
            else:
                print("file "+ file_currentposition +" is not exist please check again!")
        except Exception as error:
            print('Caught this error: ' + repr(error) + " ,file copy failed!")

    14.#Get Latest MC build path from ftp
    #def getmcLatestBuildPath(self,TargetFtpServer):
        #print("trying to get latest MC build path")
        #LatestBuildDate = datetime.now().strftime('%d-1.%m.%Y')





        #filepathExist, fileExist = TargetFtpServer.WinFileCheckFTP(folder)
        #TargetFtpServer.
