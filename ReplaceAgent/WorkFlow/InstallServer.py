from ReplaceAgent.WorkFlow.MCWorkFlow import MCWorkFlow
import threading

if __name__ == "__main__":

    def thread_job1():
        MCWorkFlow.silentInstallWindows(target_server_ip= "16.187.188.168")

    #def thread_job2():
        #MCWorkFlow.silentInstallWindows(target_server_ip= "16.187.190.223")


    thread1 = threading.Thread(target=thread_job1, name='T1')
    #thread2 = threading.Thread(target =thread_job2, name ='T2' )
    thread1.start()
    #thread2.start()

    #def thread_jobx():
        #MCWorkFlow.ReplaceAgentWindows(target_server_ip = "16.187.188.168")

    #threadx = threading.Thread(target=thread_jobx, name='T3')
    #threadx.start()
