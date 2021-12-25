
from scapy.all import *
import sys, os

#defining protocol number for our custom header
TYPE_MYTUNNEL = 0x1212
#standard protocol fr ipv4
TYPE_IPV4 = 0x0800
#defining fields inside our header which will hold all the values
class MyTunnel(Packet):
    name = "MyTunnel"
    fields_desc = [
    ShortField("pid", 0),
    ShortField("dst_id", 0),
    #for holding a char which would tell us what kind of data point is in it
    #'h' = humidity
    #'t' = temperature
    #'p' = pressure
    StrFixedLenField("op", "a", length=1),
    #to hold the data values
    IEEEFloatField("prev_value", 0),
    IEEEFloatField("new_value", 0),
    ]
    def mysummary(self):
        return self.sprintf("pid=%pid%, dst_id=%dst_id%")

bind_layers(Ether, MyTunnel, type=TYPE_MYTUNNEL)
bind_layers(MyTunnel, IP, pid=TYPE_IPV4)