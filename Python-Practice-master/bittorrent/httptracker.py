# -*- coding: utf-8 -*-

import httplib
import urllib
import bcodec
import re
import torrent_file
import get_ip_peerid

class TrackersInfo(object):
    '''
    TODO: http tracker support
    TODO: tracker polling support
    '''
	__info_hash = []
    
    __peer_id = None
    __host_ip = None
    __host_port = None
    
    __trackers = []             
    __tracker_check_timeout = 0 
    __tracker_get_timeout = 0
    __tracker_max_retrys = 0
    __peer_list = []

    def __init__(self, announce_list, host_info, info_hash):
        '''
        Constructor
        '''
        self.__info_hash = info_hash
        self.__peer_id, self.__host_ip, self.__host_port = host_info
        self.__tracker_check_timeout = 3 
        self.__tracker_get_timeout = 10
        self.__tracker_max_retrys = 2
        self.__peer_list = []
      
        for tier in announce_list:  
            for announce in tier:
                tracker_addr = self.__get_tracker_addr(announce)
                if tracker_addr == None:
                    continue
                tracker = {}
                tracker['addr'] = tracker_addr
                tracker['rsp'] = None
                tracker['retrys']  = 0
                tracker['error'] = ''
                self.__trackers.append(tracker)

        print '\n',self.__trackers
        pass

    def __get_tracker_addr(self, announce):
        tracker_addr = None
        m = re.match(r'(http://)([^/,:]*)(:(\d*))?(/.*)?',announce)
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
        
        tracker_addr = (web_addr,web_port, page_url)#ิชื้
        return tracker_addr

    def __generate_request(self, download_state):  
        downloaded = download_state['downloaded']
        uploaded = download_state['uploaded']
        left = download_state['left']
        event = download_state['event']
        
        request = {}
        request['info_hash'] = self.__info_hash
        request['peer_id'] = self.__peer_id
        request['ip'] = self.__host_ip
        request['port'] = self.__host_port
        request['uploaded'] = uploaded
        request['downloaded'] = downloaded
        request['left'] = left
        request['event'] = event
        request = urllib.urlencode(request)
        return request

    def refresh_trackers(self, download_state, refresh_intvl):
        rsp_msg = None
        for tracker in self.__trackers:
            rsp = tracker['rsp']
            if rsp != None:
                rsp['interval'] -= refresh_intvl
                if rsp['interval'] > 0:
                    continue
                if rsp['interval'] < 0:
                    rsp['interval'] = 0
            #self.__tracker_max_retrys = 2        
            if tracker['retrys'] < self.__tracker_max_retrys:
                self.__request_tracker(tracker, download_state)               
        passs

    def __request_tracker(self, tracker, download_state):
        print "\nrequest_tracker: ",tracker['addr']
        
        web_addr,web_port,page_url = tracker['addr']         
        tracker_con = httplib.HTTPConnection(web_addr, web_port,False,timeout=self.__tracker_get_timeout)
        piece_request = self.__generate_request(download_state)
        if not page_url:
            page_url = ''
        url = page_url + '?' + piece_request
        print 'http://'+web_addr+url
        try:
            tracker_con.request("GET", url)
            response = tracker_con.getresponse()
            print response.status,response.reason
            if response.status != 200:
                print 'Get tracker info error:%s! tracker:%s' %(response.reason, tracker['addr'])
                tracker_con.close()
                tracker['error'] = response.reason
                tracker['retrys'] += 1
                if response.status == 302:
                   print response.getheaders()
				   msg = response.msg['location']
                   self.workout302found(msg, download_state)
                return
            #200 OK
            msg_encoded = response.read()
            print msg_encoded
            tracker_con.close()
            rsp_msg, length = bcodec.bdecode(msg_encoded)
            print rsp_msg
            if rsp_msg == None:
                print 'Get tracker info error:%s! tracker:%s' %(msg_encoded, tracker['addr'])
                tracker['error'] = msg_encoded
                tracker['retrys'] += 1
                return
            
        except Exception,e:
            tracker_con.close()
            print 'Get tracker info error:%s! tracker:%s' %(e.message, tracker['addr'])
            tracker['error'] = e.message
            tracker['retrys'] += 1
            return
        
        if 'failure reason' in rsp_msg.keys():
            print 'Get tracker info error:%s! tracker:%s' %(rsp_msg['failure reason'], tracker['addr'])
            tracker['error'] = rsp_msg['failure reason']
            tracker['retrys'] += 1
            return

        if 'peers' in rsp_msg.keys():
            peers_msg = rsp_msg['peers']
        elif 'peers6' in rsp_msg.keys():
            peers_msg = rsp_msg['peers6']

        peer_list = []
        if type(peers_msg) == type(''):
            for i in range(0,len(peers_msg)-5,6):
                one_peer = peers_msg[i:i+6]
                #peer_id = ''
                ip = one_peer[0:4]
                port = one_peer[4:6]
                ip = '%d.%d.%d.%d' %(ord(ip[0]),ord(ip[1]),ord(ip[2]),ord(ip[3]))
                port = ord(port[0])*256+ord(port[1])
                peer_list.append((ip,port))
                self.__peer_list.append((ip,port))
        elif type(peers_msg) == type([]):
            for peer in peers_msg:
                peer_list.append((peer['ip'],peer['port']))
                self.__peer_list.append((peer['ip'],peer['port']))

        rsp_msg['peers'] = peer_list 
        print  peer_list
        tracker['rsp'] = rsp_msg
        tracker['retrys'] = 0
        
    def workout302found(self, msg, _302_download_state):
        comm_index = msg.find('?')
        _302_announce = msg[:comm_index]
        _302_piece = msg[comm_index+1:]
        _302_addrs = self.__get_tracker_addr(_302_announce)
        _302_tracker = {}
        _302_tracker['addr'] = _302_addrs
        _302_tracker['rsp'] = None
        _302_tracker['retrys']  = 0
        _302_tracker['error'] = ''
		print '_302GET.............start\n'
        self.__request_tracker(_302_tracker, _302_download_state)
        pass


    def get_peers(self):
    #    peers = []
    #    for tracker in self.__trackers:
    #        rsp = tracker['rsp']
    #        if rsp != None:
    #            for peer in rsp['peers']:
    #                if peer not in peers:
    #                    peers.append(peer)
        return self.__peer_list


if __name__ == '__main__':
    #torrent name here
    filename = 'xxxx.torrent'
    torrent = torrent_file.TorrentFile()
    torrent.read_file(filename)
    info_hash = torrent.get_info_hash()
    print "info_hash:\n", list(info_hash)
    announce_list = torrent.get_announces()
    print "\nannounce_list:\n",announce_list
    peer_id = get_ip_peerid.peer_id
    ip = get_ip_peerid.returnip()
    listening_addr = '6881'
    host_info = (peer_id, ip, listening_addr )
    print "\nhost_info:\n", host_info
    trackers = TrackersInfo(announce_list, host_info, info_hash)
    download_state = {}
    download_state['downloaded'] = 0
    download_state['uploaded']  = 0
    download_state['left'] = 364575
    download_state['event'] = 'started'
    trackers.refresh_trackers(download_state, 20)
    peers = trackers.get_peers()
    print peers
