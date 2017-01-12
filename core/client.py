#_*_coding:utf-8_*_
import time,sys
import urllib
from urllib import request,error
import json
sys.path.append("..")
from conf import settings
class ClientHandle(object):
    def __init__(self):
        self.monitored_services = {}
    def load_latest_configs(self):
        request_type = settings.configs['urls']['get_configs'][1]
        url = "%s/%s" % (settings.configs['urls']['get_configs'][0],settings.configs['HostID'])
        latest_config = self.url_request(request_type,url)
        latest_config = json.loads(latest_config.decode())
        self.monitored_services.update(latest_config)
    def forever_run(self):
        exit_flag = False
        config_last_update_time = 0
        while not exit_flag:
            if time.time() -config_last_update_time > settings.configs['ConfigUpdateInterval']:
                self.load_latest_configs()
                print("Loaded latest config:",self.monitored_services)
                config_last_update_time = time.time()
            #start to monitor services
            for service_name,val in self.monitored_services['services'].items():
                if len(val) == 2 :
                    self.monitored_services['services'][service_name].append(0)
                monitor_interval = val[1]
                last_invoke_time = val[2]
                if time.time() - last_invoke_time >monitor_interval:
                    print("\033[31;1mGoing to monitor [%s]\033[0m" % service_name)
                    #监控结束更改时间戳
                    self.monitored_services['services'][service_name][2] = time.time()
                else:
                    print("\033[31;1mGoing to monitor [%s] in [%s]secs\033[0m" % (service_name,(monitor_interval - (time.time() - last_invoke_time))))
            time.sleep(1)
    def url_request(self,action,url,**extra_data):
        '''
        cope with monitor server by url
        :param action: 'get' or ''post
        :param url: witch url you want to request from the moniter server
        :param extra_data:
        :return:
        '''
        abs_url = "http://%s:%s/%s" % (settings.configs['Server'],settings.configs['ServerPort'],url)
        if action in ('get','GET'):
            print(url,extra_data)
            try:
                req = urllib.request.Request(abs_url)
                req_data = urllib.request.urlopen(req,timeout=settings.configs['Request_Timeout'])
                callback = req_data.read()
                print("----->>server response:",callback)
                return callback
            except urllib.error.URLError as e:
                exit("\033[31;1m%s\033[0m"%e)