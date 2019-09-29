import os
import wmi
from ftplib import *
import ftplib
import winrm


from ReplaceAgent.Common.RemoteMachine import RemoteMachine

class RemoteMachine_Windows(RemoteMachine):
    global count
    count = 0

    def __init__(self, ip, username, password, port = "21", timeout = 30):
        RemoteMachine.__init__(self, ip, username, password, port, timeout = 30)
        self.ftp = None

    #create ftp connection #Pass
    def FTPConnection(self):
        try:
            print("start ftp connection to specific server ", str(self.ip) + "." )
            self.ftp = FTP(self.ip)
            self.ftp.login(self.username,self.password)
            print("Ftp Connection establish successfully!")
        except ftplib.all_errors as e:
            print("FTP error:",e)

    #def FTP connection close #Pass
    def FTPDisconnection(self):
        try:
            print("start to close ftp connection on ip ", str(self.ip) + ".")
            self.ftp.quit()
            print("Ftp Close succefully!")
        except ftplib.all_errors as e:
            print("FTP error:",e)

    #Check File exits or not #Pass
    def WinFileCheckFTP(self, File):
        try:
            FileExist = False
            FilePathExist = False
            filepath, filename = self.SwitchToPathName(File)
            if(filepath !=""):
                self.ftp.cwd(filepath)
                FilePathExist = True
            FileList = self.ftp.nlst()
            for index in range(len(FileList)):
                if FileList[index] == filename:
                    FileExist = True
                    break
            if(FileExist):
                print("File ", filename + " Found Exist")
            else:
                print("File ", filename + " is not Found")
            return FilePathExist,FileExist
        except ftplib.all_errors as e:
            print("FTP error:",e)
            return FilePathExist,FileExist

    #Get Files from win machine #pass
    def WinGetFilesFTP(self, file_remote, file_local):
        print("start to get file from ftp server ", self.ip)
        Remotefilepath, Remotefilename = self.SwitchToPathName(file_remote)
        Savefilepath, Savefilename = self.SwitchToPathName(file_local)
        os.chdir(Savefilepath)
        if(Remotefilepath != ""):
            self.ftp.cwd(Remotefilepath)
        file = open(Remotefilename,"wb")
        self.ftp.retrbinary("RETR " + Remotefilename, file.write)
        file.close()
        os.rename(Remotefilename, Savefilename)
        if(os.path.isfile(file_local)):
            print("file download successfully!")
        else:
            print("file download failed!")

    #Upload Files to Remote win machine # Pass
    def WinFileUploadFTP(self, file_local, file_remote):
        print("Start to upload files " +  file_local + " to server: "+ self.ip)
        Remotefilepath, Remotefilename = self.SwitchToPathName(file_remote)
        filelocalpath, filelocalname = self.SwitchToPathName(file_local)
        if(Remotefilepath != ""):
            self.ftp.cwd(Remotefilepath)
        os.chdir(filelocalpath)
        file = open(filelocalname,"rb")
        self.ftp.storbinary("STOR " + filelocalname, file)
        file.close()
        if(filelocalname!=Remotefilename):
            self.ftp.rename(filelocalname, Remotefilename)
        if(self.WinFileCheckFTP(file_remote)):
            print("file upload successfully!")
        else:
            print("did not find file, upload fail!")

    #Upload From Local to Remote win machines
    #def winFilesUpload(self, file_local, file_remote):

    #Delete Files includ folders from Remote win machine # Pass
    def WinFileDeleteFTP(self, file_remote):
        print("start to delete file ", file_remote)
        RemoteFilePath, RemoteFileName = self.SwitchToPathName(file_remote)
        if (RemoteFilePath !="" and RemoteFileName !=""):
            self.ftp.cwd(RemoteFilePath)
            filepathExist, fileExist = self.WinFileCheckFTP(file_remote)
            if(filepathExist and fileExist):
                self.ftp.delete(RemoteFileName)
                print("File Delete Successfully!")
        elif (RemoteFilePath !="" and RemoteFileName == ""):
            print("this is folder trying to delete everything under this folder!")
            self.ftp.rmd(RemoteFilePath)
        else:
            print("File or folder is not exist, no need to delete!")

    #get file switch to path and name #Passed
    def SwitchToPathName(self,path):
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

    # Create session for winrm #Pass
    def WinSessionCreate(self):
        try:
            print("start create winrm session on remote server: "+ self.ip)
            self.client = winrm.Session(self.ip, auth=(self.username, self.password),transport='ntlm', server_cert_validation='ignore')
            print("session create successfully!")
        except Exception as error:
            print('Caught this error: ' + repr(error) + " ,this may cause by winrm not enable on target server!")

    # Execute wincommand #pass
    def WinBatchCommandExecute(self, cmd, args=()):
        try:
            r = self.client.run_cmd(cmd, args=())
            return_code = r.status_code
            output = r.std_out.decode("utf-8")
            print(output)
            error = r.std_err
            return output
        except Exception as error:
            print('Caught this error: ' + repr(error) + " ,command execute failed!")
            return False

    # Send win shell command to win vm
    def winPowserShellExecute(self,cmd):
        try:
            r = self.client.run_ps(cmd)
            return_code = r.status_code
            output = r.std_out.decode("utf-8")
            print(type(output))
            error = r.std_err
            print(return_code)
            print(output)
            print(error)
            return output
        except Exception as error:
            print('Caught this error: ' + repr(error) + " ,command execute failed!")
            return False

    # Create path and folder on ftp server
    def WinCreateFolderFTP(self, path):
        try:
            if(os.path.dirname (path)):
                print("this is the path!, start to create folder on ftp server")
                self.ftp.mkd(path)
            else:
                print("input: " + path + " is not path!")
        except Exception as error:
            print('Caught this error: ' + repr(error) + " ,this may cause by file already exist, cannot create!")

    # Clean the file under folder on ftp server
    def WinFolderDelete(self,path,temp = "" ):
        global count
        if(count >0 and (len(path)>len(temp))):
            self.ftp.rmd(path)
            print("Target Folder deleted successfully!")
            return True
        filepathExist, filenameExist = self.WinFileCheckFTP(path)
        if(filepathExist and filenameExist == False and temp !="/" and path !="/"):
            folderlist = []
            NonEmptyFolder = []
            if (count ==0):
                temp = path
            count = count + 1
            print(" trying to delete all files under current folder!")
            filepathExist, filenameExist = self.WinFileCheckFTP(temp)
            if(filepathExist and filenameExist==False):
                print("this is folder, proceed!")
                #get formal path
                filepath, filename = self.SwitchToPathName(temp)
                self.ftp.cwd(filepath)
                #delete all file in current folder
                for fname in self.ftp.nlst():
                    try:
                        self.ftp.delete(fname)
                    except ftplib.error_perm:
                        print(fname is "a folder")
                        folderlist.append(fname)
                print("all files under "+ filepath + " should be deleted")
                #start to delete void folder
                for foldern in folderlist:
                    try:
                        self.ftp.rmd(foldern)
                    except ftplib.error_perm:
                        NonEmptyFolder.append(foldern)
                if(len(self.ftp.nlst())==0):
                    try:
                        self.ftp.cwd("..")
                        temp = self.ftp.pwd()
                        print(temp)
                    except ftplib:
                        print("something wrong cannot delete void folder!")
                        return False
                elif(len(NonEmptyFolder)==0):
                    print("file is not being delete successfully, failed!")
                    return False
                else:
                    temp = filepath + NonEmptyFolder[0]
                self.WinFolderDelete(path,temp)
            else:
                print("the path you provide is not valid, terminate the proccess")
                return False

        #Delete remote win machine file
        def winFileDelete(self,path, TargetServer):
            cmd = "rm -r "+ path + " \n"
            TargetServer.winPowserShellExecute(cmd)


