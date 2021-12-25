#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct
import argparse
import serial

from scapy.all import sendp, send, get_if_list, get_if_hwaddr, hexdump
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP
from myTunnel_header import MyTunnel

#establishing connection to arduino
try:
    arduino = serial.Serial("/dev/ttyACM0", timeout=1 ,baudrate=9600)
except:
    print("Please check the port")

#getting interface of ethernet
def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

#function to calculate mean, standard deviation and z-score of values
def caluclate_m_std(x):
    length=len(x)
    avg=0
    std=0
    z_score_alt=[0,0,0,0,0]
    z_score=list()
    if length>=1:
        avg=sum(x)/length
        std=0
        for i in range(length):
            std = std + (x[i]-avg)**2
        std = std / length
        std = std ** 0.5
        if std>0:
            for i in range(length):
                temp=abs(x[i]-avg)
                z_score.append(temp/std)
            if std<1.0:
                return True,z_score,avg
        elif std==0:
            return False,z_score_alt,avg
    else:
        return False,z_score_alt,avg

#function to populate arrays with 5 data points for each sensor
def get_data():
    temp_array=list()
    humid_array=list()
    press_array=list()
    counter=0
    while(True):
        data=arduino.readline()
        data=data.decode()
        if data:
            #return when the array gets populated with 5 elements
            if counter==5:
                return humid_array,temp_array,press_array
            words=data.split(",")
            #[u'Current humidity=55.70', u' temperature=18.10', u' pressure=94520\r\n']
            if len(words)==3:
                counter+=1
                humid_array.append(float(words[0].split("=")[-1]))
                temp_array.append(float(words[1].split("=")[-1]))
                press_array.append(float(words[2].split("=")[-1]))

def main():
    ip_addr="10.0.1.2"
    dst_id=2

    #variables to note the amount of data sent and the pkts that got aggregated
    pkt_amount=0
    aggregated_pkt=0

    addr = socket.gethostbyname(ip_addr)
    dst_id = dst_id
    iface = get_if()

    #humid_array=[69.0,69.3,69.7,69.7,69.4]
    #temp_array=[6.0,6.9,6.7,6.2,7.0]
    #press_array=[93472,93455,93432,93460,93460]
   
    new_value_humid=0
    prev_value_humid=0
    new_value_temp=0
    prev_value_temp=0
    new_value_press=0
    prev_value_press=0

    print "sending on interface {} to dst_id {}".format(iface, str(dst_id))
    
    #main loop
    for out_loop in range(5): 
        humid_array,temp_array,press_array=get_data()   
        print "humidity: ",humid_array
        
        op_humid,z_score_humid,avg_humid=caluclate_m_std(humid_array)
        print "mean humidity: ",avg_humid
        print "z-score humidity: ",z_score_humid

        op_temp,z_score_temp,avg_temp=caluclate_m_std(temp_array)
        print "temperature: ",temp_array

        print "pressure: ",press_array

        #this flag helps in not sending again the mean value again if it occurs
        flag_avg=0
        if op_humid==True:
            for i in range(len(humid_array)):
                z_sc=z_score_humid[i]
                if (z_sc<0.5):
                    new_value_humid=avg_humid
                    flag_avg +=1
                else:
                    new_value_humid=humid_array[i]
                if flag_avg <= 1:
                    #actually sending the pkt 
                    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
                    pkt = pkt / MyTunnel(dst_id=dst_id, prev_value=prev_value_humid, new_value=new_value_humid, op="h") / IP(dst=addr)  
                    #pkt.show2()
                    sendp(pkt, iface=iface, verbose=False)
                    aggregated_pkt+=1
                prev_value_humid=new_value_humid
                pkt_amount+=1
        #if the criteria for data aggregation doesnt meet we send the original data without processing it
        else:
            for i in range (len(humid_array)):
                new_value_humid=humid_array[i]
                pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
                pkt = pkt / MyTunnel(dst_id=dst_id, prev_value=prev_value_humid, new_value=new_value_humid, op="h") / IP(dst=addr)  
                #pkt.show2()
                sendp(pkt, iface=iface, verbose=False)
                prev_value_humid=new_value_humid
                pkt_amount+=1

        #checking the temp values with the same set of rules
        flag_avg=0
        if op_temp==True:
            for i in range(len(temp_array)):
                z_sc=z_score_temp[i]
                if (z_sc<0.5):
                    new_value_temp=avg_temp
                    flag_avg +=1
                else:
                    new_value_temp=temp_array[i]
                if flag_avg <= 1:
                    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
                    pkt = pkt / MyTunnel(dst_id=dst_id, prev_value=prev_value_temp, new_value=new_value_temp, op="t") / IP(dst=addr)  
                    #pkt.show2()
                    sendp(pkt, iface=iface, verbose=False)
                    aggregated_pkt+=1
                prev_value_temp=new_value_temp
                pkt_amount+=1

        else:
            for i in range (len(temp_array)):
                new_value_temp=temp_array[i]
                pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
                pkt = pkt / MyTunnel(dst_id=dst_id, prev_value=prev_value_temp, new_value=new_value_temp, op="t") / IP(dst=addr)  
                #pkt.show2()
                sendp(pkt, iface=iface, verbose=False)
                prev_value_temp=new_value_temp
                pkt_amount+=1

        #for pressure values
        for l in range (len(press_array)):
            new_value_press=press_array[l]
            pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
            pkt = pkt / MyTunnel(dst_id=dst_id, prev_value=prev_value_press, new_value=new_value_press, op="p") / IP(dst=addr)  
            #pkt.show2()
            sendp(pkt, iface=iface, verbose=False)
            prev_value_press=new_value_press
            pkt_amount+=1

    print "Number of pkts in total: ", pkt_amount
    print "aggregated pkts: ", pkt_amount-aggregated_pkt
    
if __name__ == '__main__':
    main()