from ReplaceAgent.Common.BaseAction import BaseAction
import os.path
if __name__ == "__main__":

    # Param for trigger
    mac_server_ip = "10.5.33.10"
    mac_server_username = "qamcteam"
    mac_server_password = "123456"
    mac_server_port = "22"
    temp_folder_path = "/Users/qamcteam/Desktop/"
    local_folder = os.path.join(os.path.expanduser("~"), 'Desktop') + "/Ezio/"
    
    # Create ssh connection with Mac
    BaseAction = BaseAction()
    tmp_folder_name = temp_folder_path + BaseAction.generateScenarioNo() + "/"

    # Create mac remote Connection
    mac = BaseAction.remoteServer(mac_server_ip, mac_server_username, mac_server_password, mac_server_port)
    # Transfer Files from local folder to Mac temp folder
    BaseAction.fileUpload(local_folder, tmp_folder_name, mac)
    # Perform the code sign in remote mac
    BaseAction.getRemoteFilePath(tmp_folder_name, mac)
    # Copy the hpmc enabler from mac to foler in order to perform codesign
    cmd = "cp -f /opt/mac_instrument/Agent/MCEnabler/osx/HPMCEnabler " + tmp_folder_name + "HPMCEnabler"
    BaseAction.executeCommand(mac, cmd)
    cmd = "cd " + tmp_folder_name +"\n chmod +x HPMCEnabler"
    BaseAction.executeCommand(mac, cmd)
    # CodeSign Apps in remote folder
    BaseAction.appCodesign_instrument(0, tmp_folder_name, mac,mac_server_password)
    # Get the files
    BaseAction.fileDownload(tmp_folder_name, local_folder, mac)
    # Delete temp Folder
    BaseAction.remoteFolderDelete(tmp_folder_name, mac)







