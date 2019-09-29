from ReplaceAgent.Common.BaseAction import BaseAction
from ReplaceAgent.Resources.Tools.DefaultResources import DefaultResources
import os

class SilentInstall_win:
    def __init__(self):
        self.BaseAction = BaseAction()

    #SilentInstall_win
    def SilentInstall_win(self,ftp_server_ip = DefaultResources.ftp_server_ip,
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
        #Remote server instance define
        FTPServer = self.BaseAction.remoteServer_win(ftp_server_ip, ftp_server_username, ftp_server_password, ftp_server_port, "FTP")
        TargetServer = self.BaseAction.remoteServer_win(target_server_ip, target_server_username, target_server_password, target_server_port, target_server_type)
        InstrumentServer = self.BaseAction.remoteServer_win(instrument_server_ip, instrument_server_username, instrument_server_password, instrument_server_port, instrument_server_type)

        #Needed param
        TmpFolderName = self.BaseAction.generateScenarioNo()
        #TmpFolderName = "No20190806144716"
        RemoteTmpFolderPath = "C:/Users/Administrator/Desktop/"+TmpFolderName
        RemoteFTPTmpFolderPath = "/Ezio/" + TmpFolderName
        LocalTempFolderPath = os.path.join(os.path.expanduser("~"), 'Desktop') + "/Ezio"

        #ResourceFile FTP path
        ZipFilepath,ZipFileName = self.BaseAction.switchToPathAndName(ZiptoolPath)
        ZipFtpPath = RemoteFTPTmpFolderPath + "/" + ZipFileName
        DownLoadBatchFilePath,DownLoadBatchFileName = self.BaseAction.switchToPathAndName(DownLoadBatchFile)
        DownLoadBatchFTPPath = RemoteFTPTmpFolderPath + "/" + DownLoadBatchFileName
        #add file into the list
        ftp_filepathlist = [ZipFtpPath, DownLoadBatchFTPPath, ftp_install_path]

        #Steps
        self.BaseAction.createLocalFolder(LocalTempFolderPath)
        self.BaseAction.CopyFile(ZiptoolPath, LocalTempFolderPath+"/"+ ZipFileName)
        self.BaseAction.CopyFile(DownLoadBatchFile, LocalTempFolderPath+"/"+ DownLoadBatchFileName)
        self.BaseAction.fileUploadFTP_win(LocalTempFolderPath,RemoteFTPTmpFolderPath,FTPServer)
        self.BaseAction.remoteBatchFileGenerate_win(RemoteTmpFolderPath,ftp_filepathlist ,TargetServer, FTPServer)
        #Trigger download process

        cmd_gotofolder = "cd "+ RemoteTmpFolderPath+"\n"
        cmd_triggerdownload = "./download.bat\n"
        cmd = cmd_gotofolder +  cmd_triggerdownload
        self.BaseAction.executeCommand_win(TargetServer,cmd)

        #Trigger 7zip silent install and mc server silent install
        cmd_gotofolder = "cd "+ RemoteTmpFolderPath+"\n"
        cmd_silentinstall = "./"+DownLoadBatchFileName+ " "+ target_server_ip+"\n"
        cmd = cmd_gotofolder + cmd_silentinstall
        print(cmd)
        self.BaseAction.executeCommand_win(TargetServer,cmd)

        #Clean Env
        self.BaseAction.remoteDeleteFile_win(TargetServer,RemoteTmpFolderPath)
        self.BaseAction.remoteFolderDeleteFTP_win(RemoteFTPTmpFolderPath,FTPServer)
        self.BaseAction.deleteLocalFolder(LocalTempFolderPath)






