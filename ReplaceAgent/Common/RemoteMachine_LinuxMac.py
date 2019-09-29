import paramiko
import os.path
from ReplaceAgent.Common.RemoteMachine import RemoteMachine

class RemoteMachine_LinuxMac(RemoteMachine):

    #create ssh connection
    def _SSHConnect(self):
        print("Connecting to server on ip", str(self.ip) + ".")
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.load_system_host_keys()
            self.client.connect(self.ip, self.port, self.username, self.password)
            print("Connected!")
        except paramiko.ssh_exception:
            print("Connection Error")

    #create sftp connection
    def CreateSFTP(self):
        self._SSHConnect()
        print("start to create sftp connection on ip",str(self.ip) + ".")
        try:
            self.sftp = self.client.open_sftp()
            print("sftp connection established")
        except paramiko.ssh_exception:
            print("Connection Error")

    #ssh/sftp disconnected
    def _SSHClose(self):
        self.client.close()
        print("SSH Client Disconnected")
        self.sftp.close()
        print("SFTP Disconnected")

    #ssh command remote execute
    def SSHCommandExecute(self, cmd):
        Result = []
        self.CreateSFTP()
        print("command input:")
        print(cmd)
        (stdin, stdout, stderr) = self.client.exec_command(cmd)
        for line in stdout.read().splitlines():
             print(line.decode('utf-8').strip())
             Result.append(line.decode('utf-8').strip())
        self._SSHClose()
        return Result

    # Check Files Exist or not on remote machine (including folder linux)
    def SSHFileCheck(self, Files):
        FilesNotExist = []
        tmp = []
        try:
            self.CreateSFTP()
            if  isinstance(Files, str):
                tmp.append(Files)
            else:
                tmp = Files
            for index in range(len(tmp)):
                try:
                    self.sftp.stat(tmp[index])
                except IOError:
                    FilesNotExist.append(tmp[index])

            if len(FilesNotExist) == 0:
                print("Files all found")
                self._SSHConnect()
                return True
            else:
                print("Files")
                for index in range(len(FilesNotExist)):
                    print(FilesNotExist[index])
                    self._SSHConnect()
                print("not found")
                return False
        except paramiko.ssh_exception:
            print("Connection Error")

    # Get file from remote server Linux or Mac
    def SSHGetFiles(self, file_remote, file_local):
        try:
            print("Trying to get Files...")
            if self.SSHFileCheck(file_remote):
                self.CreateSFTP()
                for index in range(len(file_remote)):
                    if os.path.exists(os.path.abspath(os.path.join(file_local[0], os.pardir))):
                        print("path ", str(os.path.abspath(os.path.join(file_local[0], os.pardir))) + " exists")
                    else:
                        print("path ", str(os.path.abspath(os.path.join(file_local[0], os.pardir))) + " not exist, creating Path....")
                        os.mkdir(os.path.abspath(os.path.join(file_local[0], os.pardir)))
                    self.sftp.get(file_remote[index], file_local[index])
                    print("Get Files % successfully", file_remote[index])
            else:
                print("Fail to get Files")
            self._SSHClose()
        except paramiko.ssh_exception:
            print("Fail to get Files")
            self._SSHClose()

    # Upload file from local to remote server
    def SSHUploadFiles(self, file_local, file_remote):
        try:
            print("Trying to upload Files...")
            self.CreateSFTP()
            for index in range(len(file_local)):
                self.sftp.put(file_local[index], file_remote[index])
                print("Upload Files %s successfully" %(file_local[index]))
            if  self.SSHFileCheck(file_remote):
                print("Upload All Files successfully")
            else:
                print("Upload Files Failed")
            self._SSHClose()
        except ValueError:
            print("Fail to Upload Files")
            self._SSHClose()

    # Delete file from remote server
    def SSHDeleteFiles(self,file_remote):
        try:
            print("Trying to Delete Files...")
            if self.SSHGetFiles(file_remote):
                print("Target files exists, start to delete...")
                self.CreateSFTP()
                for index in range(len(file_remote)):
                    self.sftp.remove(file_remote[index])
                    print("removing file % successfully" %(file_remote[index]))

            if self.SSHGetFiles(file_remote):
                print("Files still exist, need to check")

            else:
                print("Target files are missing, deletefiles failed")
            self._SSHClose()
        except paramiko.ssh_exception:
            print("Target files missing, deletefiles failed")
            self._SSHClose()

