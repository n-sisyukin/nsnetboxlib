#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# Name:        Inventory Tools
#
# Author:      Nikolay Sisyukin
# URL:         https://nikolay.sisyukin.ru/
#
# Created:     30.05.2025
# Copyright:   (c) Nikolay Sisyukin 2025
# Licence:     MIT License
#-------------------------------------------------------------------------------

import lib_nspylib as mylib
import requests as rq
import urllib3
import json
import re
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#-------------------------------------------------------------------------------

class NetboxAPI:
    
    #-------------------------------------------------------------------------------

    def __init__(self, config_file=None, input_data_file=None):
        if input_data_file is None and config_file is not None:
            config = mylib.readJSONfromFile(config_file)
            
            self.__url = config['url']
            self.__apikey = config['apikey']
            self.__api = {'custom_fields': {'url_part': 'extras/custom-fields',            'desc': 'Custom Fields'},
                          'vms':           {'url_part': 'virtualization/virtual-machines', 'desc': 'Virtual Machines'},
                          'cluster_types': {'url_part': 'virtualization/cluster-types',    'desc': 'Cluster Types'},
                          'clusters':      {'url_part': 'virtualization/clusters',         'desc': 'Clusters'},
                          'ip_addresses':  {'url_part': 'ipam/ip-addresses',               'desc': 'IP Addresses'},
                          'ip_ranges':     {'url_part': 'ipam/ip-ranges',                  'desc': 'IP Ranges'},
                          'ip_prefixes':   {'url_part': 'ipam/prefixes',                   'desc': 'IP Prefixes'},
                          'vlan_groups':   {'url_part': 'ipam/vlan-groups',                'desc': 'VLAN Groups'},
                          'vlans':         {'url_part': 'ipam/vlans',                      'desc': 'VLANs'},
                          'sites':         {'url_part': 'dcim/sites',                      'desc': 'Sites'},
                          'locations':     {'url_part': 'dcim/locations',                  'desc': 'Locations'},
                          'racks':         {'url_part': 'dcim/racks',                      'desc': 'Racks'},
                          'owners':        {'url_part': 'tenancy/contacts',                'desc': 'Owners'},
                          'manufacturers': {'url_part': 'dcim/manufacturers',              'desc': 'Manufacturers'},
                          'platforms':     {'url_part': 'dcim/platforms',                  'desc': 'Platforms'},
                          'device_roles':  {'url_part': 'dcim/device-roles',               'desc': 'Device Roles'},
                          'device_types':  {'url_part': 'dcim/device-types',               'desc': 'Device Types'},
                          'devices':       {'url_part': 'dcim/devices',                    'desc': 'Devices'}} 
            self.__cf = {}
            self.__headers = {'Authorization': f'Token {self.__apikey}', 'Content-Type': 'application/json','Accept': 'application/json'}

            print(f'{mylib.nowDateTime()} - NetboxAPI: Connecting to "{self.__url}" - ...')
            self.__netbox = rq.Session()
            self.__netbox.headers.update(self.__headers)
            try:
                self.__response_of_request = self.__netbox.get(f"{self.__url}", verify=False)
                if self.__response_of_request.status_code == 200: 
                    print(f'{mylib.nowDateTime()} - NetboxAPI: Connecting to "{self.__url}" - OK! (Code: {self.__response_of_request.status_code})\n')
                else:
                    print(f'{mylib.nowDateTime()} - NetboxAPI: Connecting to "{self.__url}" - Error!')
                    if not isinstance(self.__response_of_request, dict):
                        print(f'\nResponse Code: {self.__response_of_request.status_code}!')
                        print(f'\nResponse JSON:')
                        mylib.dumpJSONtoScreen(json.loads(self.__response_of_request.text))
                    else:
                        print(f'\nResponse:')
                        mylib.dumpJSONtoScreen(self.__response_of_request)
            except rq.exceptions.ConnectionError as e:
                self.__response_of_request = None
                print(f'{mylib.nowDateTime()} - NetboxAPI: Connecting to "{self.__url}" - Error!')
                print(f'\nText of Exception:\n{e}!')
                print(f'\nClose this program!')
                exit()
        elif input_data_file is not None:
            print(f'{mylib.nowDateTime()} - NetboxAPI: Work mode - Data from file "{input_data_file}"!\n')
            self.__input_data_file = input_data_file
            self.__netbox = None

    #-------------------------------------------------------------------------------

    def __del__(self):
        if self.__netbox is not None:
            self.__netbox.close()

    #-------------------------------------------------------------------------------

    def __load(self, part):
        print(f'{mylib.nowDateTime()} - NetBoxAPI: Get {self.__api[part]['desc']} from "{self.__url}" - ...')
        temp_response = self.__netbox.get(f"{self.__url}/{self.__api[part]['url_part']}/?limit=0", verify=False).json()
        data_to_return = temp_response.get('results', [])
        print(f'{mylib.nowDateTime()} - NetBoxAPI: Get {self.__api[part]['desc']} from "{self.__url}" - OK ({len(data_to_return)})\n')
        return data_to_return
    
    def loadCustomFields(self):
        temp = self.__load('custom_fields')
        result = temp
        return result

    def loadVMs(self):
        temp = self.__load('vms')
        result = temp
        return result
    
    def loadClusterTypes(self):
        temp = self.__load('cluster_types')
        result = temp
        return result

    def loadClusters(self):
        temp = self.__load('clusters')
        result = temp
        return result

    def loadIPAddresses(self):
        temp = self.__load('ip_addresses')
        result = temp
        return result        

    def loadIPRanges(self):
        temp = self.__load('ip_ranges')
        result = temp
        return result

    def loadIPPrefixes(self):
        temp = self.__load('ip_prefixes')
        result = temp
        return result
    
    def loadVlanGroups(self):
        temp = self.__load('vlan_groups')
        result = temp
        return result

    def loadVlans(self):
        temp = self.__load('vlans')
        result = temp
        return result
    
    def loadSites(self):
        temp = self.__load('sites')
        result = temp
        return result
    
    def loadLocations(self):
        temp = self.__load('locations')
        result = temp
        return result
    
    def loadRacks(self):
        temp = self.__load('racks')
        result = temp
        return result
    
    def loadOwners(self):
        temp = self.__load('owners')
        result = temp
        return result
    
    def loadManufacturers(self):
        temp = self.__load('manufacturers')
        result = temp
        return result
    
    def loadPlatforms(self):
        temp = self.__load('platforms')
        result = temp
        return result
    
    def loadDeviceRoles(self):
        temp = self.__load('device_roles')
        result = temp
        return result
    
    def loadDeviceTypes(self):
        temp = self.__load('device_types')
        result = temp
        return result
    
    def loadDevices(self):
        temp = self.__load('devices')
        result = temp
        return result
    
    #-------------------------------------------------------------------------------
    
    def __create(self, part, data_to_create):
        result = {'list_of_good': [],
                  'list_of_bad':  [],
                  'dict_of_bad'  :{}}
        
        if len(data_to_create) > 0:
            def __subcreate(data, item_index=1, len_of_data=1):
                if 'name' in data.keys():
                    object_name = data['name']
                elif 'address' in data.keys():
                    object_name = data['address']
                elif 'display' in data.keys():
                    object_name = data['display']
                elif 'model' in data.keys():
                    object_name = data['model']
                elif 'description' in data.keys():
                    object_name = data['description']                  
                elif 'id' in data.keys():
                    object_name = f'Object with ID {data['id']}'
                else:
                    object_name = 'Unknown Object'
                print(f'{mylib.nowDateTime()} - NetBoxAPI: Create {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - ...')
                temp_response = self.__netbox.post(f"{self.__url}/{self.__api[part]['url_part']}/", data=json.dumps(data), verify=False).json()
                if temp_response.get('created'):
                    print(f'{mylib.nowDateTime()} - NetBoxAPI: Create {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - OK ({item_index}/{len_of_data})!\n')
                    result['list_of_good'].append(object_name)
                else:
                    result['list_of_bad'].append(object_name)
                    
                    result['dict_of_bad'][object_name] = {}
                    result['dict_of_bad'][object_name]['request']  = data
                    
                    print(f'{mylib.nowDateTime()} - NetBoxAPI: Create {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - Error ({item_index}/{len_of_data})!')
                    
                    if not isinstance(temp_response, dict):
                        temp_response = {'status_code': temp_response.status_code,
                                        'text': temp_response.text,
                                        'json': json.loads(temp_response.text)}
                        
                        print(f'\nResponse Code: {temp_response['status_code']}!')
                        print(f'\nResponse JSON:')
                        mylib.dumpJSONtoScreen(temp_response['json'])
                    
                    else:
                        print(f'\nResponse:')
                        mylib.dumpJSONtoScreen(temp_response)

                    print()
                    print(f'\nData in request:')
                    mylib.dumpJSONtoScreen(data)
                    print()

                    result['dict_of_bad'][object_name]['response'] = temp_response

            if isinstance(data_to_create, dict):
                __subcreate(data_to_create)
            elif isinstance(data_to_create, list):
                for i, item_to_create in enumerate(data_to_create):
                    __subcreate(item_to_create, i+1, len(data_to_create)) 
        else:
            print(f'{mylib.nowDateTime()} - NetBoxAPI: No Data {self.__api[part]['desc']} to Create in "{self.__url}"!\n')
        
        result['list_of_good'] = sorted(set(result['list_of_good']))
        result['list_of_bad']  = sorted(set(result['list_of_bad']))
        result['dict_of_bad']  = mylib.sortDictByKey(result['dict_of_bad'])
        
        return result
    
    def createCustomFields(self, data_to_create):
        return(self.__create('custom_fields', data_to_create))

    def createVMs(self, data_to_create):
        return(self.__create('vms', data_to_create))
    
    def createClusterTypes(self, data_to_create):
        return(self.__create('cluster_types', data_to_create))

    def createClusters(self, data_to_create):
        return(self.__create('clusters', data_to_create))

    def createIPAddresses(self, data_to_create):
        res = self.__create('ip_addresses', data_to_create)
        res['list_of_good'] = mylib.sortedIPs(res['list_of_good'])
        res['list_of_bad'] = mylib.sortedIPs(res['list_of_bad'])
        res['dict_of_bad'] = {ip: res['dict_of_bad'][ip] for ip in res['list_of_bad']}
        return res

    def createIPRanges(self, data_to_create):
        return(self.__create('ip_ranges', data_to_create))

    def createIPPrefixes(self, data_to_create):
        return(self.__create('ip_prefixes', data_to_create))
    
    def createVlanGroups(self, data_to_create):
        return(self.__create('vlan_groups', data_to_create))

    def createVlans(self, data_to_create):
        return(self.__create('vlans', data_to_create))
    
    def createSites(self, data_to_create):
        return(self.__create('sites', data_to_create))
    
    def createLocations(self, data_to_create):
        return(self.__create('locations', data_to_create))
    
    def createRacks(self, data_to_create):
        return(self.__create('racks', data_to_create))
    
    def createOwners(self, data_to_create):
        return(self.__create('owners', data_to_create))
    
    def createManufacturers(self, data_to_create):
        return(self.__create('manufacturers', data_to_create))
    
    def createPlatforms(self, data_to_create):
        return(self.__create('platforms', data_to_create))

    def createDeviceRoles(self, data_to_create):
        return(self.__create('device_roles', data_to_create))

    def createDeviceTypes(self, data_to_create):
        return(self.__create('device_types', data_to_create))

    def createDevices(self, data_to_create):
        return(self.__create('devices', data_to_create))

    #-------------------------------------------------------------------------------

    def __update(self, part, data_to_update):
        result = {'list_of_good': [],
                  'list_of_bad':  [],
                  'dict_of_bad'  :{}}
        
        if len(data_to_update) > 0:
            def __subupdate(data, item_index=1, len_of_data=1):
                if 'name' in data.keys():
                    object_name = data['name']
                elif 'address' in data.keys():
                    object_name = data['address']
                elif 'display' in data.keys():
                    object_name = data['display']
                elif 'model' in data.keys():
                    object_name = data['model']
                elif 'description' in data.keys():
                    object_name = data['description']                  
                elif 'id' in data.keys():
                    object_name = f'Object with ID {data['id']}'
                else:
                    object_name = 'Unknown Object'
                print(f'{mylib.nowDateTime()} - NetBoxAPI: Update {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - ...')
                temp_response = self.__netbox.patch(f"{self.__url}/{self.__api[part]['url_part']}/{data['id']}/", data=json.dumps(data), verify=False)
                if temp_response.status_code == 200:
                    print(f'{mylib.nowDateTime()} - NetBoxAPI: Update {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - OK ({item_index}/{len_of_data})!\n')
                    result['list_of_good'].append(object_name)
                else:
                    result['list_of_bad'].append(object_name)
                    
                    result['dict_of_bad'][object_name] = {}
                    result['dict_of_bad'][object_name]['request']  = data
                    
                    print(f'{mylib.nowDateTime()} - NetBoxAPI: Update {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - Error ({item_index}/{len_of_data})!')
                    
                    if not isinstance(temp_response, dict):
                        temp_response = {'status_code': temp_response.status_code,
                                        'text': temp_response.text,
                                        'json': json.loads(temp_response.text)}
                        
                        print(f'\nResponse Code: {temp_response['status_code']}!')
                        print(f'\nResponse JSON:')
                        mylib.dumpJSONtoScreen(temp_response['json'])
                    
                    else:
                        print(f'\nResponse:')
                        mylib.dumpJSONtoScreen(temp_response)

                    print()
                    print(f'\nData in request:')
                    mylib.dumpJSONtoScreen(data)
                    print()

                    result['dict_of_bad'][object_name]['response'] = temp_response
                    
            if isinstance(data_to_update, dict):
                __subupdate(data_to_update)
            elif isinstance(data_to_update, list):
                for i, item_to_create in enumerate(data_to_update):
                    __subupdate(item_to_create, i+1, len(data_to_update))
        else:
            print(f'{mylib.nowDateTime()} - NetBoxAPI: No Data {self.__api[part]['desc']} to Update in "{self.__url}"!\n')
        
        result['list_of_good'] = sorted(set(result['list_of_good']))
        result['list_of_bad']  = sorted(set(result['list_of_bad']))
        result['dict_of_bad']  = mylib.sortDictByKey(result['dict_of_bad'])
        
        return result
    
    def updateCustomFields(self, data_to_update):
        return(self.__update('custom_fields', data_to_update))

    def updateVMs(self, data_to_update):
        return(self.__update('vms', data_to_update))
    
    def updateClusterTypes(self, data_to_update):
        return(self.__update('cluster_types', data_to_update))

    def updateClusters(self, data_to_update):
        return(self.__update('clusters', data_to_update))

    def updateIPAddresses(self, data_to_update):
        res = self.__update('ip_addresses', data_to_update)
        res['list_of_good'] = mylib.sortedIPs(res['list_of_good'])
        res['list_of_bad'] = mylib.sortedIPs(res['list_of_bad'])
        res['dict_of_bad'] = {ip: res['dict_of_bad'][ip] for ip in res['list_of_bad']}
        return res

    def updateIPRanges(self, data_to_update):
        return(self.__update('ip_ranges', data_to_update))

    def updateIPPrefixes(self, data_to_update):
        return(self.__update('ip_prefixes', data_to_update))
    
    def updateVlanGroups(self, data_to_update):
        return(self.__update('vlan_groups', data_to_update))

    def updateVlans(self, data_to_update):
        return(self.__update('vlans', data_to_update))
    
    def updateSites(self, data_to_update):
        return(self.__update('sites', data_to_update))
    
    def updateLocations(self, data_to_update):
        return(self.__update('locations', data_to_update))
    
    def updateRacks(self, data_to_update):
        return(self.__update('racks', data_to_update))
    
    def updateOwners(self, data_to_update):
        return(self.__update('owners', data_to_update))
    
    def updateManufacturers(self, data_to_update):
        return(self.__update('manufacturers', data_to_update))
    
    def updatePlatforms(self, data_to_update):
        return(self.__update('platforms', data_to_update))

    def updateDeviceRoles(self, data_to_update):
        return(self.__update('device_roles', data_to_update))

    def updateDeviceTypes(self, data_to_update):
        return(self.__update('device_types', data_to_update))

    def updateDevices(self, data_to_update):
        return(self.__update('devices', data_to_update))

    #-------------------------------------------------------------------------------

    def __delete(self, part, data_to_delete):
        result = {'list_of_good': [],
                  'list_of_bad':  [],
                  'dict_of_bad'  :{}}
        
        if len(data_to_delete) > 0:            
            def __subdelete(data, item_index=1, len_of_data=1):
                if 'name' in data.keys():
                    object_name = data['name']
                elif 'address' in data.keys():
                    object_name = data['address']
                elif 'display' in data.keys():
                    object_name = data['display']
                elif 'model' in data.keys():
                    object_name = data['model']
                elif 'description' in data.keys():
                    object_name = data['description']                  
                elif 'id' in data.keys():
                    object_name = f'Object with ID {data['id']}'
                else:
                    object_name = 'Unknown Object'
                print(f'{mylib.nowDateTime()} - NetBoxAPI: Delete {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - ...')
                temp_response = self.__netbox.delete(f"{self.__url}/{self.__api[part]['url_part']}/{data['id']}", verify=False)
                if temp_response.status_code == 204:  
                    print(f'{mylib.nowDateTime()} - NetBoxAPI: Delete {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - OK ({item_index}/{len_of_data})!\n')
                    result['list_of_good'].append(object_name)
                else:
                    result['list_of_bad'].append(object_name)

                    result['dict_of_bad'][object_name] = {}
                    result['dict_of_bad'][object_name]['request']  = data
                    
                    print(f'{mylib.nowDateTime()} - NetBoxAPI: Delete {self.__api[part]['desc']} object "{object_name}" in "{self.__url}" - Error ({item_index}/{len_of_data})!')
                    
                    if not isinstance(temp_response, dict):
                        temp_response = {'status_code': temp_response.status_code,
                                        'text': temp_response.text,
                                        'json': json.loads(temp_response.text)}
                        
                        print(f'\nResponse Code: {temp_response['status_code']}!')
                        print(f'\nResponse JSON:')
                        mylib.dumpJSONtoScreen(temp_response['json'])
                    
                    else:
                        print(f'\nResponse:')
                        mylib.dumpJSONtoScreen(temp_response)

                    print()
                    print(f'\nData in request:')
                    mylib.dumpJSONtoScreen(data)
                    print()

                    result['dict_of_bad'][object_name]['response'] = temp_response

            if isinstance(data_to_delete, dict):
                __subdelete(data_to_delete)
            elif isinstance(data_to_delete, list):
                for i, item_to_create in enumerate(data_to_delete):
                    __subdelete(item_to_create, i+1, len(data_to_delete))
        else:
            print(f'{mylib.nowDateTime()} - NetBoxAPI: No Data {self.__api[part]['desc']} to Delete in "{self.__url}"!\n')
        
        result['list_of_good'] = sorted(set(result['list_of_good']))
        result['list_of_bad']  = sorted(set(result['list_of_bad']))
        result['dict_of_bad']  = mylib.sortDictByKey(result['dict_of_bad'])

        return result

    def deleteCustomFields(self, data_to_delete):
        return(self.__delete('custom_fields', data_to_delete))

    def deleteVMs(self, data_to_delete):
        return(self.__delete('vms', data_to_delete))
    
    def deleteClusterTypes(self, data_to_delete):
        return(self.__delete('cluster_types', data_to_delete))

    def deleteClusters(self, data_to_delete):
        return(self.__delete('clusters', data_to_delete))

    def deleteIPAddresses(self, data_to_delete):    
        res = self.__delete('ip_addresses', data_to_delete)
        res['list_of_good'] = mylib.sortedIPs(res['list_of_good'])
        res['list_of_bad'] = mylib.sortedIPs(res['list_of_bad'])
        res['dict_of_bad'] = {ip: res['dict_of_bad'][ip] for ip in res['list_of_bad']}
        return res

    def deleteIPRanges(self, data_to_delete):
        return(self.__delete('ip_ranges', data_to_delete))

    def deleteIPPrefixes(self, data_to_delete):
        return(self.__delete('ip_prefixes', data_to_delete))
    
    def deleteVlanGroups(self, data_to_delete):
        return(self.__delete('vlan_groups', data_to_delete))

    def deleteVlans(self, data_to_delete):
        return(self.__delete('vlans', data_to_delete))
    
    def deleteSites(self, data_to_delete):
        return(self.__delete('sites', data_to_delete))
    
    def deleteLocations(self, data_to_delete):
        return(self.__delete('locations', data_to_delete))
    
    def deleteRacks(self, data_to_delete):
        return(self.__delete('racks', data_to_delete))
    
    def deleteOwners(self, data_to_delete):
        return(self.__delete('owners', data_to_delete))
    
    def deleteManufacturers(self, data_to_delete):
        return(self.__delete('manufacturers', data_to_delete))
    
    def deletePlatforms(self, data_to_delete):
        return(self.__delete('platforms', data_to_delete))

    def deleteDeviceRoles(self, data_to_delete):
        return(self.__delete('device_roles', data_to_delete))

    def deleteDeviceTypes(self, data_to_delete):
        return(self.__delete('device_types', data_to_delete))

    def deleteDevices(self, data_to_delete):
        return(self.__delete('devices', data_to_delete))

    #-------------------------------------------------------------------------------

    
    
    #-------------------------------------------------------------------------------

    def loadData(self):
        result = None
        if self.__netbox is not None:
            if self.__response_of_request is not None:
                if self.__response_of_request.status_code == 200:
                    result = {}
                    result['custom_fields'] = self.loadCustomFields()
                    result['vms'] =           self.loadVMs()
                    result['cluster_types'] = self.loadClusterTypes()
                    result['clusters'] =      self.loadClusters()
                    result['ip_addresses'] =  self.loadIPAddresses()
                    result['ip_ranges'] =     self.loadIPRanges()
                    result['ip_prefixes'] =   self.loadIPPrefixes()
                    result['vlan_groups'] =   self.loadVlanGroups()
                    result['vlans'] =         self.loadVlans()
                    result['sites'] =         self.loadSites()
                    result['locations'] =     self.loadLocations()
                    result['racks'] =         self.loadRacks()
                    result['owners'] =        self.loadOwners()
                    result['manufacturers'] = self.loadManufacturers()
                    result['platforms'] =     self.loadPlatforms()
                    result['device_roles'] =  self.loadDeviceRoles()
                    result['device_types'] =  self.loadDeviceTypes()
                    result['devices'] =       self.loadDevices()
                    return result
        else:
            print(f'{mylib.nowDateTime()} - NetBoxAPI: Reading data from file "{self.__input_data_file}" - ...')
            temp_data = mylib.readJSONfromFile(self.__input_data_file)
            result = temp_data.copy()
            print(f'{mylib.nowDateTime()} - NetBoxAPI: Reading data from file "{self.__input_data_file}" - OK!\n')
        return result
    
    #-------------------------------------------------------------------------------

    def uploadData(self, data_to_create, data_to_update, data_to_delete):
        pass

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This is a library module and should not be run directly.')