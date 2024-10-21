import serial.tools.list_ports
import usbcount_class as UC
import os
from labqrng import optical


portslist = list(serial.tools.list_ports.comports())
devicelist = []
addresslist = []
for port in portslist:
    devicelist.append(port.device + " " + port.description)
    addresslist.append(port.device)

print(list(zip(addresslist, devicelist)))
i = int(input("please input the correct address index:\n"))

deviceAddress = addresslist[i]
counter = UC.FPGA_counter()
counter.startport(deviceAddress)
counter.mode = 'timestamp'

ctr = 0
while True:
    bits, metrics= optical(10, counter)  # 100ms means 0.1 second
    if len(bits) > 1:
        bit = bits[-1]
        print(bit)
        with open('../webpage/streaming/word.txt', 'w') as file:  # It is saved in that folder for easier local tesing.
            file.write(bit + "*" + str(metrics[0]) + "*" + str(metrics[1]) + "*" + str(metrics[2]) + "*" + str(ctr))
        os.system("scp -i 'Keypair/NUSPC5287.pem' ../webpage/streaming/word.txt ubuntu@ec2-18-139-114-157.ap-southeast-1.compute.amazonaws.com:/var/www/html/streaming")

    elif len(bits) == 1:
        bit = bits[0]
        print(bit)
        with open('../webpage/streaming/word.txt', 'w') as file:
            file.write(bit + "*" + "None" + "*" + "None" + "*" + "None" + "*" + str(ctr))
        os.system("scp -i 'Keypair/NUSPC5287.pem' ../webpage/streaming/word.txt ubuntu@ec2-18-139-114-157.ap-southeast-1.compute.amazonaws.com:/var/www/html/streaming")
    else:
        print("not enough random bits")   
    # print(bits)
    # print(bit)

    # if os.path.exists("../remote/word.txt"):
    #     os.remove("../remote/word.txt")
    
    # For communicating with the server:
    
    #     Option1: Save it as a file
            # with open('../remote/word.txt', 'wb') as file:
            #     file.write(bits + "*" + str(ctr))
            #     # os.system("scp -i 'Keypair/NUSPC5287.pem' word.txt ubuntu@ec2-18-139-114-157.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/deployment/MDB")
    ctr += 1
    #     Option2: Set up the client and server connection by socket and secure socket layer.
    




# Option2: set up the client and server connection by socket and secure socket layer.

