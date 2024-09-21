# Source Code : https://www.geeksforgeeks.org/how-to-terminate-a-running-process-on-windows-in-python/
# pip install wmi

# import wmi library
import wmi


def get_kill_process():
    # This variable ti would be used
    # as a parity and counter for the
    # terminating processes
    ti = 0

    # This variable stores the name
    # of the process we are terminating
    # The extension should also be
    # included in the name
    name = ['UiPath.Executor.exe', 'CustomInputForm.exe', 'UiPath.Studio.Analyzer.exe',
            'UiPath.Studio.DataBaseServer.exe', 'UiPath.Service.UserHost.exe']
    # 'UiPath.Studio.exe'
    # Initializing the wmi object
    f = wmi.WMI()

    # Iterating through all the
    # running processes
    for process in f.Win32_Process():

        # Checking whether the process
        # name matches our specified name
        print(process.name)
        if process.name in name:
            print("Terminating ", process.name)
            # If the name matches,
            # terminate the process
            process.Terminate()  # un check later

            # This increment would acknowledge
            # about the termination of the
            # Processes, and would serve as
            # a counter of the number of processes
            # terminated under the same name
            ti += 1

    # True only if the value of
    # ti didn't get incremented
    # Therefore implying the
    # process under the given
    # name is not found
    if ti == 0:
        # An output to inform the
        # user about the error
        print("Process not found!!!")


"""
Explanation: 

Firstly, we define a variable storing an integer value, which would serve to tell whether the process got terminated or not. 
This variable could also be used to determine how many processes under the same name have been terminated. 
Then, we specify the name of the process which we are willing to terminate. After which we initialize the WMI() class of wmi library.
This allows us to use the methods found inside it such as WMI.Win32_Service, WMI.Win32_Process etc which are designed to perform different tasks. 
We would be using the WMI.Win32_Process function to get the list of running processes as wmi objects.
Then we use the name attribute of the wmi object to the get name of the running process. 
After which we would be using primitive string matching to determine whether the name of the application matches the one specified before. 
If it does then we call the Terminate() method, to kill/terminate the process.
After which we increment the value of ti, where the incremented value (or any non 0 value) would signify that at least one process has been terminated.
After the end of the loop (when all the running processes names have been checked), we would check whether the value of variable ti is still 0 or not.
If it is then no process got terminated, and we inform the user about the same using an Error message.
"""
