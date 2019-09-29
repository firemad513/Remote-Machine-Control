from ReplaceAgent.Common.BaseAction import BaseAction

class DefaultResources:

    BaseAction = BaseAction()
    File = BaseAction.ConfigFile()

    # Param for trigger
    ftp_server_ip = File.GetKeyValueFromFile("ftp_server_ip", "DefaultResourceFile.txt")
    ftp_server_username = File.GetKeyValueFromFile("ftp_server_username", "DefaultResourceFile.txt")
    ftp_server_password = File.GetKeyValueFromFile("ftp_server_password", "DefaultResourceFile.txt")
    ftp_server_port = File.GetKeyValueFromFile("ftp_server_port", "DefaultResourceFile.txt")
    ftp_install_path = File.GetKeyValueFromFile("ftp_install_path", "DefaultResourceFile.txt")
    target_server_ip = File.GetKeyValueFromFile("target_server_ip", "DefaultResourceFile.txt")
    target_server_username = File.GetKeyValueFromFile("target_server_username", "DefaultResourceFile.txt")
    target_server_password = File.GetKeyValueFromFile("target_server_password", "DefaultResourceFile.txt")
    target_server_port = File.GetKeyValueFromFile("target_server_port", "DefaultResourceFile.txt")
    target_server_type = File.GetKeyValueFromFile("target_server_type", "DefaultResourceFile.txt")
    instrument_server_ip = File.GetKeyValueFromFile("instrument_server_ip", "DefaultResourceFile.txt")
    instrument_server_username = File.GetKeyValueFromFile("instrument_server_username", "DefaultResourceFile.txt")
    instrument_server_password = File.GetKeyValueFromFile("instrument_server_password", "DefaultResourceFile.txt")
    instrument_server_port = File.GetKeyValueFromFile("instrument_server_port", "DefaultResourceFile.txt")
    instrument_server_type = File.GetKeyValueFromFile("instrument_server_type", "DefaultResourceFile.txt")
    ZiptoolPath = File.GetKeyValueFromFile("ZiptoolPath", "DefaultResourceFile.txt")
    DownLoadBatchFile = File.GetKeyValueFromFile("DownLoadBatchFile", "DefaultResourceFile.txt")
    AgentName = File.GetKeyValueFromFile("AgentName", "DefaultResourceFile.txt")
    SigneAgentName = File.GetKeyValueFromFile("SigneAgentName", "DefaultResourceFile.txt")
    RemoteAgentFolder = File.GetKeyValueFromFile("RemoteAgentFolder", "DefaultResourceFile.txt")
    mac_instrument_server_Enabler = File.GetKeyValueFromFile("mac_instrument_server_Enabler", "DefaultResourceFile.txt")
