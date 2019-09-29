from ReplaceAgent.BussinessLevel.installSilent_win import *
from ReplaceAgent.BussinessLevel.ReplaceAgentWindows import *
from ReplaceAgent.Resources.Tools.DefaultResources import DefaultResources
from ReplaceAgent.Common.ThreadHandler import ThreadHandler

class MCWorkFlow:

    def __init__(self):
        self.Threadhandler = ThreadHandler()

    @staticmethod
    def FlowExecution(self,Target):
        self.ThreadHandler.FlowTrigger(Target)

    @staticmethod
    def silentInstallWindows(ftp_server_ip = DefaultResources.ftp_server_ip,
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
        SilentInstall_win().SilentInstall_win(
            ftp_server_ip, ftp_server_username, ftp_server_password,
            ftp_server_port, ftp_install_path, target_server_ip,
            target_server_username, target_server_password,target_server_port,target_server_type,
            instrument_server_ip, instrument_server_username, instrument_server_password,
            instrument_server_port, instrument_server_type, ZiptoolPath,
            DownLoadBatchFile
        )
        print("server "+ftp_server_ip+ " finish install process!")

    @staticmethod
    def ReplaceAgentWindows(ftp_server_ip = DefaultResources.ftp_server_ip,
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
        ReplaceAgentWindows().ReplaceAgentWindows(
            ftp_server_ip, ftp_server_username, ftp_server_password,
            ftp_server_port, ftp_install_path, target_server_ip,
            target_server_username, target_server_password,target_server_port,target_server_type,
            instrument_server_ip, instrument_server_username, instrument_server_password,
            instrument_server_port, instrument_server_type, ZiptoolPath,
            DownLoadBatchFile
        )
        print("server "+ftp_server_ip+ " finish Agent Replace process!")

