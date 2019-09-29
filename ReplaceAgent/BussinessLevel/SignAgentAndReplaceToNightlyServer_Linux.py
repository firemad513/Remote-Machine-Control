from ReplaceAgent.Common.BaseAction import BaseAction
import os.path

if __name__ == "__main__":
    #Initialize Test Componet 
    BaseAction = BaseAction()
    File = BaseAction.ConfigFile()
    # Param for trigger
    mac_server_ip = File.GetKeyValueFromFile("mac_server_ip", "ReplaceAgentconfig.txt")
    mac_server_username = File.GetKeyValueFromFile("mac_server_username", "ReplaceAgentconfig.txt")
    mac_server_password = File.GetKeyValueFromFile("mac_server_password", "ReplaceAgentconfig.txt")
    mac_server_port = File.GetKeyValueFromFile("mac_server_port", "ReplaceAgentconfig.txt")
    linux_server_ip = File.GetKeyValueFromFile("linux_server_ip", "ReplaceAgentconfig.txt")
    linux_server_username = File.GetKeyValueFromFile("linux_server_username", "ReplaceAgentconfig.txt")
    linux_server_password = File.GetKeyValueFromFile("linux_server_password", "ReplaceAgentconfig.txt")
    linux_server_port = File.GetKeyValueFromFile("linux_server_port", "ReplaceAgentconfig.txt")
    mac_instrument_server = File.GetKeyValueFromFile("mac_instrument_server", "ReplaceAgentconfig.txt")
    
    linuxAgentName = ['HP4M-Agent.ipa', 'HPMC-AgentLauncher.ipa', 'WebDriverAgentRunner-Runner.ipa', 'WebDriverAgentRunner-Runner_xcode9.ipa']
    SignedAgentName = ['HP4M-Agent-Codesigned.ipa', 'HPMC-AgentLauncher-Codesigned.ipa', 'WebDriverAgentRunner-Runner-Codesigned.ipa', 'WebDriverAgentRunner-Runner_xcode9-Codesigned.ipa']
    RemoteAgentFolder = "/opt/mc/server/Agent/"
    local_folder = os.path.join(os.path.expanduser("~"), 'Desktop') + "/Ezio/"
    temp_folder_path = "/Users/qamcteam/Desktop/"
    
    #get  Agent path on linux server
    linuxAgentPath = []
    for index in range(len(linuxAgentName)):
        linuxAgentPath.append(RemoteAgentFolder+linuxAgentName[index]) 

    # get Unsign agent path on local
    UnsignAgentPath = []
    for index in range(len(linuxAgentName)):
        UnsignAgentPath.append(local_folder + linuxAgentName[index])

    # get SignedAgent path on local
    SignedAgentPath = []
    for index in range (len(SignedAgentName)):
        SignedAgentPath.append(local_folder+SignedAgentName[index])
    
    tmp_folder_name = temp_folder_path + BaseAction.generateScenarioNo() + "/"
    #Create ssh connection with Linux
    Linux = BaseAction.remoteServer(linux_server_ip, linux_server_username, linux_server_password, linux_server_port)
    
    #Get Agent file from linux to Local Windows
    BaseAction.fileDownload(linuxAgentPath, UnsignAgentPath, Linux)
    
    # Create mac remote Connection
    mac = BaseAction.remoteServer(mac_server_ip, mac_server_username, mac_server_password, mac_server_port)
    # Transfer Files from local folder to Mac temp folder
    BaseAction.fileUpload(local_folder, tmp_folder_name, mac)
    # Perform the code sign in remote mac
    BaseAction.getRemoteFilePath(tmp_folder_name, mac)
    # Copy the hpmc enabler from mac to foler in order to perform codesign
    cmd = "cp -f "+ mac_instrument_server +"HPMCEnabler " + tmp_folder_name + "HPMCEnabler"
    BaseAction.executeCommand(mac, cmd)
    cmd = "cd " + tmp_folder_name +"\n chmod +x HPMCEnabler"
    BaseAction.executeCommand(mac, cmd)
    # CodeSign Apps in remote folder
    BaseAction.appCodesign_instrument(0, tmp_folder_name, mac)
    # Get the files
    BaseAction.fileDownload(tmp_folder_name, local_folder, mac)
    # Delete temp Folder
    BaseAction.remoteFolderDelete(tmp_folder_name, mac)
    #Upload files which being codesigned to specific folder in Linux (Replace Agent)
    BaseAction.fileUpload(SignedAgentPath, linuxAgentPath, Linux)
    # Delete Ezio Folder
    BaseAction.deleteLocalFolder(local_folder)

    
    






