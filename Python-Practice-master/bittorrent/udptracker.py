# -*- coding: utf-8 -*-

import socket
import struct
import bcodec
import torrent_file
import re

class UDPTracker(object):
    '''
    TODO: UDPTracker support
    '''
    _connid = 0
    _rsp_connid = 0
    _transid = 0
    
    _info_hash = None

    _tracker_max_retrys = 0

    _trackers = []
    _rsp_content = []
    _ip_port = []
    
    def __init__(self,info_hash,announce_list):
        self._connid = 0x41727101980
        self._rsp_connid = 0
        self._transid = 0x41727  #268071
        self._info_hash = info_hash
        self._tracker_max_retrys = 2
        self._rsp_content = []

        for tier in announce_list:
            for announce in tier:
                tracker_addr = self.get_tracker_addr(announce)
                if tracker_addr == None:
                    continue
                tracker = {}
                tracker['addr'] = tracker_addr
                tracker['rsp'] = None
                tracker['retrys'] = 0
                tracker['error'] = ''
                self._trackers.append(tracker)
                
        print '\n',self._trackers
        pass

    def get_tracker_addr(self, announce):
        tracker_addr = None
        m = re.match(r'(udp://)([^/,:]*)(:(\d*))?(/.*)?',announce)
        if m != None:
            web_addr = m.groups()[1]
            web_port = m.groups()[3]
            page_url = m.groups()[4]
        else:
            return None
        if web_port != None:
            web_port = int(web_port)
        else:
            web_port = 80
        
        tracker_addr = (web_addr,web_port, page_url)
        return tracker_addr

    def get_connpkt(self):
        connpkt = struct.pack(">QII",self._connid,0,self._transid) 
        return connpkt
    
    def analysisconnpkt(self,rsp_msg):
        if(len(rsp_msg) < 16):
            return False
        rsp_action,rsp_transid,rsp_connid = struct.unpack(">IIQ",rsp_msg)
        if(rsp_action != 0):
            return False
        if(self._transid != rsp_transid):
            return False
        self._rsp_connid = rsp_connid
        print 'rsp_connid = ',self._rsp_connid
        return True

    def get_announcepkt(self):
        peer_id = '-AZ2060-125987632568'
        downloaded = 0
        left = 12
        uploaded = 12
        event = 0
        ip = 0
        key = 0
        num_want = -1
        port = 80
        announcepkt = struct.pack(">QII20s20sQQQIIIiH",self._rsp_connid,1,self._transid,self._info_hash,peer_id,downloaded,left,uploaded,event,ip,key,num_want,port)
        return announcepkt

    def analysisannouncepkt(self,rsp_msg):
        pktcontent = {}
        if(len(rsp_msg) < 20):
            print '数据内容不匹配'
            return pktcontent
        try:
            rsp_action,rsp_transid,rsp_interval,rsp_leechers,rsp_seeders = struct.unpack(">iiiii",rsp_msg[0:20])
            i = 20
            while i < len(rsp_msg):
                rsp_ip = struct.unpack(">ssss",rsp_msg[i:i+4])
                rsp_ip = '%d.%d.%d.%d' % (ord(rsp_ip[0]),ord(rsp_ip[1]),ord(rsp_ip[2]),ord(rsp_ip[3])) 
                rsp_port = struct.unpack(">ss",rsp_msg[i+4:i+6])
                rsp_port = ord(rsp_port[0])*256 + ord(rsp_port[1])
                ip_port = (rsp_ip,rsp_port)
                i+=6
                self._ip_port.append(ip_port)
        except Exception,e:
            print 'error:',e.message
            
        pktcontent['action'] = rsp_action
        pktcontent['transid'] = rsp_transid
        pktcontent['interval'] = rsp_interval
        pktcontent['leechers'] = rsp_leechers
        pktcontent['seeders'] = rsp_seeders
        pktcontent['ip_port'] = self._ip_port
        return pktcontent


    def refresh_tracker(self):
        for tracker in self._trackers:
            if tracker['retrys'] < self._tracker_max_retrys:
                self.tracker_request(tracker)

        pass

    def connection(self,tracker):
        print "\nconnect_tracker: ",tracker['addr']
        host,port,url = tracker['addr']
        BUFSIZ=1024 
        addrs = (host,port)
        udpconnsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        data = self.get_connpkt()
        udpconnsock.settimeout(16)
        udpconnsock.sendto(data,addrs)
        try:
            rsp_msg,addrs = udpconnsock.recvfrom(BUFSIZ)
            print rsp_msg
            udpconnsock.close()
        except Exception,e:
            print 'connect error:',e.message
            udpconnsock.close()
            tracker['error'] = 'connect ' + e.message
            tracker['retrys'] += 1 
            return False
        flag = self.analysisconnpkt(rsp_msg)
        if not flag:
            tracker['error'] = 'analysis connect_rsp error!'
            tracker['retrys'] += 1
        return flag

    def tracker_request(self,tracker):
        if not self.connection(tracker):
            return 
        print "\nrequest_tracker: ",tracker['addr']

        host,port,url = tracker['addr']
        BUFSIZ=1024 
        addrs = (host,port)
        udpannouncesock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        data = self.get_announcepkt()
        udpannouncesock.settimeout(20)
        udpannouncesock.sendto(data,addrs)
        try:
            rsp_msg,addrs = udpannouncesock.recvfrom(BUFSIZ) 
            print 'request response ok here!'
            udpannouncesock.close()
        except Exception,e:
            print 'announce error:',e.message
            udpannouncesock.close()
            tracker['error'] = 'announce ' + e.message
            tracker['retrys'] += 1 
            return 
        rsp = self.analysisannouncepkt(rsp_msg)
        if rsp!={}:
            self._rsp_content.append(rsp)
        return

    def get_result(self):
        return self._ip_port
    
        
if __name__ == '__main__':
    filename = r'1.torrent'
    torrent = torrent_file.TorrentFile()
    torrent.read_file(filename)
    info_hash = torrent.get_info_hash()
    print "info_hash:\n", list(info_hash)
    announce_list = torrent.get_announces()
    print "\nannounce_list:\n",announce_list
    udp = UDPTracker(info_hash,announce_list)
    udp.refresh_tracker()
    result = udp.get_result()
    for ip_port in result:
        print ip_port


