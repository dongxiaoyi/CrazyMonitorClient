#_*_coding:utf-8_*_
configs = {
    'HostID': 1,
    'Server':"localhost",
    'ServerPort':8001,
    'urls':{
        'get_configs':['api/client/config','get'],#acqurire all the services will be monitored
        'service_report':['api/client/service/report/','post']
    },
    'ConfigUpdateInterval':300,
    'Request_Timeout':30,
}