# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:51:39 2024

@author: Florencia D. Choque
TODO: Use a config file with cam parameters
Build a class
Change this to get image
Watch out buffers!
ready: setup cam
"""
from datetime import datetime
from pylablib.devices import Andor
import numpy as np
import ctypes as ct
import time
# def setup_camera(andor): #OJO! Armar una clase
#     shape = (512, 512) # TO DO: change to 256 x 256
#     expTime = 0.300   # in sec
        
#     andor.set_exposure(expTime)
#     andor.set_roi(0, 512, 0, 512, 1, 1)
        
#     print(datetime.now(), '[xy_tracking] FOV size = {}'.format(self.shape))

#     # Temperature
#     andor.set_cooler(True)
#     andor_temperature= -20   # in °C
#     andor.set_temperature(andor_temperature)
#     print(f"Changed temperature setpoint to: {andor.get_temperature_setpoint} °C")
#     print("Andor temperature: status", andor.get_temperature_status())
        
#     # Frame transfer mode
#     andor.enable_frame_transfer_mode(True)
#     print(datetime.now(), 'Frame transfer mode ON? ', andor.is_frame_transfer_enabled())

#     # Horizontal Pixel Shift
#     channel = 0 #channel_bitdepth = 14
#     oamp = 0 #oamp_kind = 'Electron Multiplying' (output amplifier description)
#     hsspeed = 1 # hsspeed_MHz = 5.0 (horizontal scan frequency corresponding to the given hsspeed index)
#     preamp = 1 # preamp_gain=2.4000000953674316 #OJO: antes se usaba 4.7, con indice 2, chequear cómo se ve la imagen con un mayor preamp, puedo usar preamp = 2 y el cambio está en preamp_gain=5.099999904632568

#     andor.set_amp_mode(channel, oamp, hsspeed, preamp)
#     print("Current Amp mode: ", andor.get_amp_mode())

#     # EM GAIN
#     EM_gain = 1  # EM gain set to 100
#     andor.set_EMCCD_gain(EM_gain) #Check I'm not sure about units (indexes???)

#     print(datetime.now(), 'EM gain: ', andor.get_EMCCD_gain())
    
#     # Vertical shift speed
#     vert_shift_speed = 4 #µs
#     andor.set_vsspeed(vert_shift_speed)
#     print(datetime.now(), 'Current Vertical shift speed [µs]: ', andor.get_vsspeed())

#     return True

def open_shutter(andor,ttl_mode=0):
    andor.setup_shutter(ttl_mode)
    return
             

#Forma Larga de hacer lo mismo, sin tener en cuenta el __init__.py
# if __name__=="__main__":
#     AndorSDK2.restart_lib()
#     print(AndorSDK2.get_cameras_number())
#     camera = AndorSDK2.AndorSDK2Camera()
#     print(camera.get_device_info())

if __name__=="__main__":
    Andor.AndorSDK2.restart_lib() #restart_lib is not imported in __init__.py
    # print(Andor.get_cameras_number_SDK2()) #This is because of the __init__.py script of Andor file
    andor = Andor.AndorSDK2Camera(idx=0, temperature = -30, fan_mode = "full")
    print(datetime.now(),'[test_andor_using_pylablib] Device info:', andor.get_device_info())
    #setup_camera(andor)
    print("Andor is opened?", andor.is_opened())
    print("Andor cooler ON?", andor.is_cooler_on())
    print('status: ',andor.get_status(), "idle:no acquisition")
    print("Andor temperature:", andor.get_temperature())
    print("Andor temperature: status", andor.get_temperature_status())
    print("Temperature setpoint: ", andor.get_temperature_setpoint())
    print('px_size:', andor.get_pixel_size())
    print("andor channel: ", andor.get_channel())
    print("andor bitdepth: ", andor.get_channel_bitdepth())
    #print("Amp modes: ",andor.get_all_amp_modes())
    #Quiero: TAmpModeFull(channel=0, channel_bitdepth=14, oamp=0, oamp_kind='Electron Multiplying', hsspeed=1, hsspeed_MHz=5.0, preamp=1, preamp_gain=2.4000000953674316),
    #tengo: TAmpModeFull(channel=0, channel_bitdepth=14, oamp=0, oamp_kind='Electron Multiplying', hsspeed=0, hsspeed_MHz=10.0, preamp=0, preamp_gain=1.0)
    # print('hsspeed Hz: ',andor.get_hsspeed_frequency())
    # print('hspeed: ',andor.get_hsspeed())
    # print("All vsspeed: ", andor.get_all_vsspeeds())
    # print("max vsspeed: ", andor.get_max_vsspeed())
    print(datetime.now(), 'Current Vertical shift speed [µs]: ', andor.get_vsspeed())
    print("preampr_gain: ",andor.get_preamp())
    print("emCCD gain: ", andor.get_EMCCD_gain())
    print("get_roi: ", andor.get_roi()) #512*512
    #shutters
    print("shutter parameters: ", andor.get_shutter_parameters())
    print("shutter: ", andor.get_shutter())
    #Trigger
    #print("Trigger mode: ", andor.get_trigger_mode()) #Should be internal. Yes: int
    print("Acq mode: ", andor.get_acquisition_mode()) #should be kinetic, or use andor.setup_kinetic_mode()

    #Desde aquí modificar el script
    andor.setup_acquisition(mode="cont", nframes=10)
    print("Acq mode before change: ", andor.get_acquisition_mode())
    print("Tamaño del buffer: ", andor.get_buffer_size())
    open_shutter(andor,1)
    print("shutter: ", andor.get_shutter())
    andor.start_acquisition()
    print('status2: ',andor.get_status(), "idle: no acquisition")
    data = andor._read_frames((0, 10),False)
    print("FRames acquires: ", andor._get_acquired_frames())
    # print("data: ", data.shape)
    time.sleep(10.)
    print('status3: ',andor.get_status(), "idle:no acquisition")
    andor.clear_acquisition()
    print('status4: ',andor.get_status(), "idle:no acquisition")
    open_shutter(andor,0)
    print("shutter: ", andor.get_shutter())
    andor.stop_acquisition()
    print('status5: ',andor.get_status(), "idle:no acquisition")
    andor.close()
    print("Andor is opened?", andor.is_opened())


