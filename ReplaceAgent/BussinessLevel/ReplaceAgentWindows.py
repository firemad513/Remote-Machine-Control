from ReplaceAgent.Common.BaseAction import BaseAction
import os.path
from ReplaceAgent.Resources.Tools.DefaultResources import DefaultResources


class ReplaceAgentWindows:

    def __init__(self):
        self.BaseAction = BaseAction()

    #SilentInstall_win
    def ReplaceAgentWindows(self,ftp_server_ip = DefaultResources.ftp_server_ip,
                          ftp_server_username = DefaultResources.ftp_server_username,
                          ftp_server_password = DefaultResources.ftp_server_password,
                          ftp_server_port = DefaultResources.ftp_server_port,
                          ftp_install_path = DefaultResources.ftp_install_path,
                          target_server_ip = DefaultResources.target_server_ip,
                          target_server_username = DefaultResources.target_server_username,
                          target_server_password = DefaultResources.target_server_password,
                          target_server_port = DefaultResources.target_server_port,
                          target_server_type = DefaultResources.target_server_type,
                          instrument_server_ip = DefaultResources.instrument_server_ip,
                          instrument_server_username = DefaultResources.instrument_server_username,
                          instrument_server_password = DefaultResources.instrument_server_password,
                          instrument_server_port = DefaultResources.instrument_server_port,
                          instrument_server_type = DefaultResources.instrument_server_type,
                          ZiptoolPath = DefaultResources.ZiptoolPath,
                          DownLoadBatchFile = DefaultResources.DownLoadBatchFile,
                          ):

        TmpFolderName = self.BaseAction.generateScenarioNo()
        #TmpFolderName = "No20190822184246"
        LocalTempFolderPath = os.path.join(os.path.expanduser("~"), 'Desktop').replace("\\","/") + "/Ezio/"
        MacTempFolderPath = "/Users/qamcteam/Desktop/"+ TmpFolderName +"/"
        RemoteTmpFolderPath = "C:/Users/Administrator/Desktop/"+TmpFolderName + "/"
        RemoteFTPTmpFolderPath = "/Ezio/" + TmpFolderName + "/"
        #get  Agent path on linux server
        RemoteAgentPath = []
        for index in range(len(DefaultResources.AgentName)):
            RemoteAgentPath.append(DefaultResources.RemoteAgentFolder+DefaultResources.AgentName[index])
        print(RemoteAgentPath)

        # get Unsign agent path on local
        UnsignAgentPath = []
        for index in range(len(DefaultResources.AgentName)):
            UnsignAgentPath.append(LocalTempFolderPath + DefaultResources.AgentName[index])
        print(UnsignAgentPath)

        # get SignedAgent path on local
        SignedAgentPath = []
        for index in range (len(DefaultResources.SigneAgentName)):
            SignedAgentPath.append(LocalTempFolderPath+DefaultResources.SigneAgentName[index])
        print(SignedAgentPath)

        # get UNsign agent path on ftp
        ftpunsignAgentPath = []
        for index in range (len(DefaultResources.AgentName)):
            ftpunsignAgentPath.append(RemoteFTPTmpFolderPath+DefaultResources.AgentName[index])
        print(ftpunsignAgentPath)

        # get signed agent path on ftp
        ftpsignAgentPath = []
        for index in range (len(DefaultResources.SigneAgentName)):
            ftpsignAgentPath.append(RemoteFTPTmpFolderPath+DefaultResources.SigneAgentName[index])
        print(ftpsignAgentPath)

        # get signed agent path on remote server
        currentposition = []
        for index in range(len(DefaultResources.SigneAgentName)):
            currentposition.append(RemoteTmpFolderPath + DefaultResources.SigneAgentName[index])
        print(currentposition)

        #Remote server instance define
        FTPServer = self.BaseAction.remoteServer_win(ftp_server_ip, ftp_server_username, ftp_server_password, ftp_server_port, "FTP")
        TargetServer = self.BaseAction.remoteServer_win(target_server_ip, target_server_username, target_server_password, target_server_port, target_server_type)
        InstrumentServer = self.BaseAction.remoteServer(instrument_server_ip, instrument_server_username, instrument_server_password, instrument_server_port)

        #ResourceFile FTP path
        self.BaseAction.remoteFolderCreateFTP_win(RemoteFTPTmpFolderPath,FTPServer)
        self.BaseAction.remoteBatchFileGenerate_win(RemoteTmpFolderPath,RemoteAgentPath ,TargetServer, FTPServer, "put", RemoteFTPTmpFolderPath)
        #Trigger upload process

        cmd_gotofolder = "cd "+ RemoteTmpFolderPath+"\n"
        cmd_triggerdownload = "./download.bat\n"
        cmd = cmd_gotofolder +  cmd_triggerdownload
        self.BaseAction.executeCommand_win(TargetServer,cmd)
        self.BaseAction.createLocalFolder(LocalTempFolderPath)
        self.BaseAction.fileDownloadFTP_win(ftpunsignAgentPath,UnsignAgentPath,FTPServer)
        # Transfer Files from local folder to Mac temp folder
        self.BaseAction.fileUpload(LocalTempFolderPath, MacTempFolderPath, InstrumentServer)
        self.BaseAction.remoteDeleteFile_win(TargetServer,RemoteTmpFolderPath)
        # Perform the code sign in remote mac
        self.BaseAction.getRemoteFilePath(MacTempFolderPath, InstrumentServer)
        # Copy the hpmc enabler from mac to foler in order to perform codesign
        cmd = "cp -f "+ DefaultResources.mac_instrument_server_Enabler +"HPMCEnabler " + MacTempFolderPath + "HPMCEnabler"
        self.BaseAction.executeCommand(InstrumentServer, cmd)
        cmd = "cd " + MacTempFolderPath +"\n chmod +x HPMCEnabler"
        self.BaseAction.executeCommand(InstrumentServer, cmd)
        # CodeSign Apps in remote folder
        self.BaseAction.appCodesign_instrument(0, MacTempFolderPath, InstrumentServer)
        # Get the files
        self.BaseAction.fileDownload(MacTempFolderPath, LocalTempFolderPath, InstrumentServer)
        # Delete temp Folder
        #self.BaseAction.remoteFolderDelete(MacTempFolderPath, InstrumentServer)
        #Upload files which being codesigned to specific folder in Linux (Replace Agent)
        self.BaseAction.fileUploadFTP_win(SignedAgentPath, ftpsignAgentPath, FTPServer)
        self.BaseAction.remoteBatchFileGenerate_win(RemoteTmpFolderPath,ftpsignAgentPath ,TargetServer, FTPServer)

        #Trigger upload process
        cmd_gotofolder = "cd "+ RemoteTmpFolderPath+"\n"
        cmd_triggerdownload = "./download.bat\n"
        cmd = cmd_gotofolder +  cmd_triggerdownload
        self.BaseAction.executeCommand_win(TargetServer,cmd)

        #Copy rename file
        for index in range(len(currentposition)):
            self.BaseAction.fileCopy_win(currentposition[index], RemoteAgentPath[index], TargetServer)
        #Clean Env
        #self.BaseAction.remoteDeleteFile_win(TargetServer,RemoteTmpFolderPath)
        self.BaseAction.remoteFolderDeleteFTP_win(RemoteFTPTmpFolderPath,FTPServer)
        self.BaseAction.deleteLocalFolder(LocalTempFolderPath)






    #Need to get agent from Remote server to current server
    #BaseAction.remoteBatchFileGenerate_win()
    #remoteBatchFileGenerate_win(self, Remote_folder, ftp_filepathlist, Target_server, FTP_Server, type = "get"):
