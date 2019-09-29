import threading

class ThreadHandler():

    def FlowTrigger(self,Target):
        print("start to binding thead on function " + Target._name_)
        added_thread = threading.Thread(target = Target)
        added_thread.start()
        print(Target._name_ + " execution finished")




