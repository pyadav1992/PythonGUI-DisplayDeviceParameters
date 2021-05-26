############################################################################################################################################################################################################################################
#Name: Pratik Yadav
#Project: GUI for REST API using python 2
#Description: XML files for particular devices are read in the program to replace parameter ids with appropriate names.
#             Json format data is read from source code of the URL provided.
#             Data is displayed to user according to user inputs on GUI
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  
#  If not, see <https://www.gnu.org/licenses/>
############################################################################################################################################################################################################################################

import  wx       #WXPython package for GUI development      
import urllib2   #package to access server from provided URL 
import json      #package to parse Json format data
import string    #package for string operations

############################################################################################################################################################################################################################################

# DATABASE:
# Enter a new XML file in XML_file to include a new device in database.Do not change the sequence of the files. Add new
# XML files after last XML file in the list.
XML_file = ["metercap_00080114_0002.xml","metercap_00080116_0005.xml","metercap_00080117_0008.xml","metercap_00080118_0003.xml",  
            "metercap_00080119_0005.xml","metercap_00080120_0008.xml","metercap_00080121_0005.xml","metercap_00080122_0001.xml",
            "metercap_00080127_0003.xml","metercap_00080128_0003.xml","metercap_00080129_0002.xml","metercap_00080130_0003.xml",
            "metercap_00080132_0003.xml","metercap_00080133_0003.xml","metercap_00080134_0003.xml","metercap_00080135_0003.xml",
            "metercap_00080136_0003.xml","metercap_00080137_0003.xml","metercap_00080138_0003.xml","metercap_00080139_0003.xml"]

data = range(len(XML_file))
device_ids = range(len(XML_file))
device_ids_temp1 = range(len(XML_file))
device_ids_temp2 = ""
                       
for xmls in range(len(XML_file)):
    with open(XML_file[xmls]) as file:
        data[xmls] = file.read().splitlines()
        device_ids_temp1[xmls] = filter(lambda x: 'device_model="' in x, data[xmls])
        device_ids_temp2+=str(device_ids_temp1[xmls])
        
device_ids_temp3 = device_ids_temp2.split(' ') 
device_ids_temp4 = filter(lambda x: 'device_model="' in x, device_ids_temp3)

device_ids_temp5 = ""
for i1 in range(len(XML_file)):
    device_ids_temp5+=str(device_ids_temp4[i1])
device_ids_temp6 = device_ids_temp5.split('"') 
device_ids_temp6.remove('')
temp_len = len(device_ids_temp6)

for i2 in range(temp_len/2):
    device_ids_temp6.remove('device_model=')

for i3 in range(temp_len/2):
    device_ids[i3] = int(device_ids_temp6[i3],16)
    
############################################################################################################################################################################################################################################
# Graphical User Interface Development 

class REST_API_GUI(wx.Frame):
    
    #Initializing frame, panel and buttons for GUI
    def __init__(self,parent,id):
        # Every wx app must create one App object
        # before it does anything else using wx.
        self.app = wx.App()
        
        # Set up the main window
        wx.Frame.__init__(self,parent,id,'REST API GUI',size=(360, 600))
     
        panel=wx.Panel(self)
        self.quote = wx.StaticText(panel, label="P\nR\nO\nX\nI\nM\nE\nT\nR\nY\n", pos=(20, 30))
        self.Show()
        # menu buttons
        button1=wx.Button(panel,label="URL",pos=(130,10),size=(100,60))
        button2=wx.Button(panel,label="UUID",pos=(130,70),size=(100,60))
        button3=wx.Button(panel,label="Device List",pos=(130,130),size=(100,60))
        button4=wx.Button(panel,label="Device Parameters",pos=(130,190),size=(100,60))
        button5=wx.Button(panel,label="Device statistics",pos=(130,250),size=(100,60))
        button6=wx.Button(panel,label="Device Alarms",pos=(130,310),size=(100,60))
        button7=wx.Button(panel,label="Device status",pos=(130,370),size=(100,60))
        button8=wx.Button(panel,label="Device topology",pos=(130,430),size=(100,60))
        button9=wx.Button(panel,label="Exit",pos=(130,490),size=(100,60))
        
        # Bind buttons with particular functions
        self.Bind(wx.EVT_BUTTON,self.closewindow)
        self.Bind(wx.EVT_BUTTON,self.Enter_URL, button1)
        self.Bind(wx.EVT_BUTTON,self.Enter_UUID, button2)
        self.Bind(wx.EVT_BUTTON,self.get_devices,button3)
        self.Bind(wx.EVT_BUTTON,self.device_parameters,button4)
        self.Bind(wx.EVT_BUTTON,self.device_statistics,button5)
        self.Bind(wx.EVT_BUTTON,self.device_alarms,button6)
        self.Bind(wx.EVT_BUTTON,self.device_status,button7)
        self.Bind(wx.EVT_BUTTON,self.device_topology,button8)
        self.Bind(wx.EVT_BUTTON,self.closebutton, button9)

    #GUI will exit with by a red cross on right top corner 
    def closewindow(self,event):
        self.Destroy()
    
    #Button 9
    #GUI will exit with by Exit Button on GUI    
    def closebutton(self,event):
        self.Close(True)
    
    #Button 1
    #A window asking URL to user will appear.
    #If the user enters the URL and hits OK the the URL will be stored orelse not       
    def Enter_URL(self,event):
        global URL
        url = wx.TextEntryDialog(None,"Enter URL","URL","https://ftfserver.proximetry.com:20443/rest/1.0/devices/")
        if url.ShowModal()==wx.ID_OK:
            URL = url.GetValue()
    
    #Button 2
    #A window with list of all UUIDs will appear.
    #If the user selects an UUID and hits OK then UUID will be stored orelse not            
    def Enter_UUID(self,event):
        global uuid
        json_obj1 = urllib2.urlopen(URL)
        data1 = json.load(json_obj1)
        DS_device_ids = []
        DS_uuids = []
        for device in data1:
            DS_uuids.append(device['uuid'])
            DS_device_ids.append(device['device_model_id'])
        box = wx.SingleChoiceDialog(None,'Select UUID','UUID list',DS_uuids)        
        if box.ShowModal() == wx.ID_OK:
            uuid = box.GetStringSelection()
    
    #Button 3                
    #All devices registered on the server are displayed
    #total devices will be shown
    def get_devices(self,event):
        json_obj1 = urllib2.urlopen(URL)
        data1 = json.load(json_obj1)
        DS_device_ids = []
        DS_uuids = []
        for device in data1:
            DS_uuids.append(device['uuid'])
            DS_device_ids.append(device['device_model_id'])
        json_obj = urllib2.urlopen(URL)
        data = json.load(json_obj)
        print '\n'
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print 'Devices Summary:\n'
        for device in data:
            print 'uuid:\t\t\t' + device['uuid']
            print 'name:\t\t\t' + device['name']
            print 'device_model_id:\t\t' + device['device_model_id']
            print '\n'      
        print "Total number of device:", len(DS_uuids) 
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print "\n"

    #Button 4
    #with the UUID selected by the user paramters for that device will be displayed     
    def device_parameters(self,event):
        json_obj1 = urllib2.urlopen(URL)
        data1 = json.load(json_obj1)
        DS_device_ids = []
        DS_uuids = []
        for device in data1:
            DS_uuids.append(device['uuid'])
            DS_device_ids.append(device['device_model_id'])              
        for i4 in range(len(DS_uuids)):
            if str(uuid) == str(DS_uuids[i4]):
                device_id_user = DS_device_ids[i4] 
        for i5 in range(len(device_ids)):
            if device_id_user == str(device_ids[i5]): # and str(uuid) == str(DS_uuids[i5])
                DATA = data[i5]
                data_filter1 = filter(lambda x: 'paramid=' in x,DATA)
                data_filter2 = filter(lambda y: 'name='and 'paramid=' in y,DATA)
                param_ids_temp1 = ""
                name_temp1 = ""
                for i in range(len(data_filter1)):
                    param_ids_temp1+=str(data_filter1[i])
                    name_temp1+=str(data_filter2[i])
                param_ids_temp2 = param_ids_temp1.split()
                name_temp2 = name_temp1.split()
                param_ids_temp3 = filter(lambda x1: 'paramid=' in x1, param_ids_temp2)
                name_temp3 = filter(lambda y1: 'name=' in y1, name_temp2)
                name_temp4 = ""
                for i in range(len(name_temp3)):
                    name_temp4+=str(name_temp3[i])
                name_temp5 = name_temp4.replace('name="',' ')
                name_temp5 = name_temp5.replace('"',' ')
                name_temp5 = name_temp5.split(' ')
                name = []
                for i in range(len(name_temp5)):
                    if i%2 != 0:
                        name.append(name_temp5[i]) 
                param_ids = []
                a=string.maketrans('','')
                ch=a.translate(a, string.digits)
                for i in range(len(param_ids_temp3)):
                    param_ids.append(int(param_ids_temp3[i].translate(a, ch)))                                
        final_url = URL + uuid + "/parameters"    
        json_final_obj = urllib2.urlopen(final_url)
        final_data = json.load(json_final_obj)
        print '\n'
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print "Device Parameters:"
        print "UUID:",uuid
        print "Device ID:",device_id_user
        print "\n"
        param_ids_server = []
        value_server = []
        status = []
        for params in final_data:
            param_ids_server.append(params['param_id'])
            value_server.append(params['value'])
            status.append(params['status'])    
        for i6 in range(len(param_ids_server)):
            for i7 in range(len(param_ids)):
                if param_ids_server[i6] == str(param_ids[i7]):
                    print 'parameter_name:\t' + name[i7]
                    print 'value:\t\t' + value_server[i6]
                    print 'status:\t\t' + status[i6]
                    print '\n' 
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print "\n"

    #Button 5
    # Device Statistics will be displayed for that particular instant
    def device_statistics(self,event):
        json_obj1 = urllib2.urlopen(URL)
        data1 = json.load(json_obj1)
        DS_device_ids = []
        DS_uuids = []
        for device in data1:
            DS_uuids.append(device['uuid'])
            DS_device_ids.append(device['device_model_id'])            
        for i4 in range(len(DS_uuids)):
            if str(uuid) == str(DS_uuids[i4]):
                device_id_user = DS_device_ids[i4]         
        for i5 in range(len(device_ids)):
            if device_id_user == str(device_ids[i5]):
                DATA = data[i5]
                data_filter3 = filter(lambda z: 'object name=' in z, DATA)
                data_filter4 = filter(lambda a: 'stat name=' in a, DATA)
                object_name_temp1 = ""
                stat_id_temp1 = ""   
        for j in range(len(data_filter3)):
            object_name_temp1+=str(data_filter3[j])
            stat_id_temp1+=str(data_filter4[j])
        object_name_temp2 = object_name_temp1.split()
        stat_id_temp2 = stat_id_temp1.split()
        object_name_temp3 = filter(lambda z1: 'name=' in z1, object_name_temp2)
        stat_id_temp3 = filter(lambda a1: 'id=' in a1, stat_id_temp2)
        object_name_temp4 = ""
        for i in range(len(object_name_temp3)):
            object_name_temp4+=str(object_name_temp3[i])
        object_name_temp5 = object_name_temp4.replace('name="',' ')
        object_name_temp5 = object_name_temp5.replace('"',' ')
        object_name_temp5 = object_name_temp5.split(' ')
        stat_id_temp4 = ""
        for i in range(len(stat_id_temp3)):
            stat_id_temp4+=str(stat_id_temp3[i])
        stat_id_temp5 = stat_id_temp4.replace('id="',' ')
        stat_id_temp5 = stat_id_temp5.replace('"',' ')
        stat_id_temp5 = stat_id_temp5.split(' ')    
        object_name = []
        for i in range(len(object_name_temp5)):
            if i%2 != 0:
                object_name.append(object_name_temp5[i]) 
        stat_id= []
        for i in range(len(stat_id_temp5)):
            if i%2 != 0:
                stat_id.append(stat_id_temp5[i])                        
        final_url = URL + uuid + "/statistics/last-value"    
        json_final_obj = urllib2.urlopen(final_url)
        final_data = json.load(json_final_obj)
        print '\n'       
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print 'Device Statistics:'
        print "UUID:",uuid
        print "Device ID:",device_id_user
        print "\n"
        stat_id_server = []
        value_server = []
        timestamp_server = []
        for params in final_data:
            stat_id_server.append(params['stat_id'])
            value_server.append(params['value'])
            timestamp_server.append(params['timestamp'])
        for i6 in range(len(stat_id_server)):
            for i7 in range(len(stat_id)):
                if stat_id_server[i6] == str(stat_id[i7]):
                    print 'status id:\t\t' + str(object_name[i7])
                    print 'value:\t\t' + str(value_server[i6])
                    print 'time stamp:\t' + str(timestamp_server[i6])
                    print '\n'
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print "\n"
                     
    #Button 6
    #Device alarms will be shown with all information related
    def device_alarms(self,event):
        json_obj1 = urllib2.urlopen(URL)
        data1 = json.load(json_obj1)
        DS_device_ids = []
        DS_uuids = []
        for device in data1:
            DS_uuids.append(device['uuid'])
            DS_device_ids.append(device['device_model_id'])
        final_url = URL + uuid + "/alarms"    
        json_final_obj = urllib2.urlopen(final_url)
        final_data = json.load(json_final_obj)
        print '\n'
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print 'Device Alarms:'
        print "UUID:",uuid
        for params in final_data:
            print 'Alarm_id:\t\t' + str(params['alarm_id'])
            print 'State:\t\t' + str(params['state'])
            print 'Set ts:\t\t' + str(params['set_ts'])
            print 'Clear ts:\t\t' + str(params['clear_ts'])
            print 'Severity:\t\t' + str(params['severity'])
            print '\n'
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print "\n"
    
    #Button 7
    #Will let know if the device is unreachable or active      
    def device_status(self,event): 
        json_obj1 = urllib2.urlopen(URL)
        data1 = json.load(json_obj1)
        DS_device_ids = []
        DS_uuids = []
        for device in data1:
            DS_uuids.append(device['uuid'])
            DS_device_ids.append(device['device_model_id'])
        final_url = URL + uuid + "/status"    
        json_final_obj = urllib2.urlopen(final_url)
        final_data = json.load(json_final_obj)
        print '\n'
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print "UUID:",uuid
        print 'Device Status:' + str(final_data)
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print '\n'
    
    #Button 8
    #Device topology will be displayed 
    # parent id and child id
    def device_topology(self,event):
        json_obj1 = urllib2.urlopen(URL)
        data1 = json.load(json_obj1)
        DS_device_ids = []
        DS_uuids = []
        for device in data1:
            DS_uuids.append(device['uuid'])
            DS_device_ids.append(device['device_model_id'])
        final_url = URL + uuid + "/topology"    
        json_final_obj = urllib2.urlopen(final_url)
        final_data = json.load(json_final_obj)
        print '\n'
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------'
        print 'Device Topology:\n'
        print "UUID:",uuid
        for params in final_data:
            print 'Parent id:\t\t' + str(params['parent_id'])
            print 'Child id:\t\t' + str(params['child_id'])
            print 'attributes:\t\t' + str(params['attributes'])
            print '\n'  
        print '-------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------' 
        print '\n'
          
############################################################################################################################################################################################################################################
#Initializing GUI application
if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = REST_API_GUI(parent = None,id = -1)
    frame.Show()
    app.MainLoop()