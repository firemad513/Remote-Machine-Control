import os
import re
from ReplaceAgent.Common.ToolPathManagement import ToolPathManagement

class ConfigFile:
 
    def StartReadFile(self, filePath):
        f = open(filePath, "r", encoding="utf-8")
        return f
     
    #Check file type if the file type is not support return ""
    def CheckFileType(self, filePath):
        try:
            filepath = ""
            type =""
            if(os.path.isfile(filepath)):
                if(filePath.endwith('.txt')):
                    print("file type txt detected.")
                    type = "txt"
                    return type
                elif(filePath.endwith('.json')):
                    print("file type json detected.")
                    type = "json"
                    return type
                elif(filePath.endwith('.xlsx')):
                    print("file type xlsx detected.")
                    type = "xlsx"
                    return type
                else:
                    print("current file type is not supported, please check!")
                    return type
            else:
                print("File is not Exist")
        except ValueError:
            print("The Input is not a valid file, please check!")
            
    #ReadFile get the key value and return
    def GetKeyValueFromFile(self, keyName, filePath):
        try:
            value = ""
            filePath = ToolPathManagement.ConfigFileBasePath + filePath
            print (filePath)
            File = self.StartReadFile(filePath).read()
            if(re.search(keyName+" = \""+"(.+?)"+"\"",File)):
                value = re.search(keyName+" = \""+"(.*)"+"\"",File).group(1)
            elif(re.search(keyName+" = \["+"(.+?)"+"\]",File)):
                value = re.search(keyName+" = \["+"(.*)"+"\]", File).group(1)
            else:
                print("The key is not found in the file, or the keyvalue format is not correct,please check!")
            if(value!=""):
                if("'" in value):
                    print("This should be list")
                    print(value)
                    
                    value = re.sub('[\'\s]','', value )
                    print(value)
                    list = value.split(',')
                    #split(",")
                    print(list)
                    return list
                else:
                    print("This should be string")
                    print(value)
                    return value
            else:
                print("the value is not valid, please check the config file!")
            File.closed()
        except ValueError:
            print("Error found, please check the input!")
        

    
        
            
            
