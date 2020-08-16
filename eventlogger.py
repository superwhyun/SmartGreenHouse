from colorama import Fore
from colorama import Style

class EventLogger:

    EVENT_INFO=1000
    EVENT_WARN=2000
    EVENT_CRITICAL=3000
    EVENT_ERROR=4000

    def __init__(self):
        pass
    
    # def PrintEventLog(self, level, str):
    #     if(level == self.EVENT_INFO):
    #         print(f'{Fore.GREEN}%s{Fore.WHITE}' % (str))
    #     elif(level == self.EVENT_WARN):
    #         print(f'{Fore.YELLOW}%s{Fore.WHITE}' % (str))
    #     elif(level == self.EVENT_WARN):
    #         print(f'{Fore.BLUE}%s{Fore.WHITE}' % (str))
    #     elif(level == self.EVENT_ERROR):
    #         print(f'{Fore.RED}%s{Fore.WHITE}' % (str))

    def PrintEventLog(self, level, str):
        if(level == self.EVENT_INFO):
            print(Fore.GREEN + str + Fore.WHITE)
        elif(level == self.EVENT_WARN):
            print(Fore.YELLOW + str + Fore.WHITE)
        elif(level == self.EVENT_WARN):
            print(Fore.BLUE + str + Fore.WHITE)
        elif(level == self.EVENT_ERROR):
            print(Fore.RED + str + Fore.WHITE)