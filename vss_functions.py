# -*- coding:utf-8 -*-
import os
from re import search
import win32com.client

def WMIDateStringToDate(dtmDate):
    # Преобразует время из WMI формата в нормальный человеческий
    strDateTime = ""
    if (dtmDate[4] == 0):
        strDateTime = dtmDate[5] + '/'
    else:
        strDateTime = dtmDate[4] + dtmDate[5] + '/'
    if (dtmDate[6] == 0):
        strDateTime = strDateTime + dtmDate[7] + '/'
    else:
        strDateTime = strDateTime + dtmDate[6] + dtmDate[7] + '/'
        strDateTime = strDateTime + dtmDate[0] + dtmDate[1] + dtmDate[2] + dtmDate[3] + " " + dtmDate[8] + dtmDate[9] + ":" + dtmDate[10] + dtmDate[11] +':' + dtmDate[12] + dtmDate[13]
    return strDateTime


def List_shadows():
    # Выводит параметры всех существующих объектов теневых копий в консоль
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_ShadowCopy")
    for objItem in colItems:
        if objItem.Caption is not None:
          print("Caption:" + objItem.Caption)
        if objItem.ClientAccessible is not None:
          print('objItem.ClientAccessible: {}'.format(objItem.ClientAccessible))
        if objItem.Count is not None:
          print("Count:{}".format(objItem.Count))
        if objItem.Description is not None:
          print("Description: {}".format(objItem.Description))
        if objItem.DeviceObject is not None:
            print("DeviceObject: {}".format(objItem.DeviceObject))
        if objItem.Differential is not None:
            print("Differential: {}".format(objItem.Differential))
        if objItem.ExposedLocally is not None:
            print("ExposedLocally: {}".format(objItem.ExposedLocally))
        if objItem.ExposedName is not None:
            print("ExposedName: {}".format(objItem.ExposedName))
        if objItem.ExposedPath is not None:
            print("ExposedPath: {}".format(objItem.ExposedPath))
        if objItem.ExposedRemotely is not None:
            print("ExposedRemotely: {}".format(objItem.ExposedRemotely))
        if objItem.HardwareAssisted is not None:
            print("HardwareAssisted: {}".format(objItem.HardwareAssisted))
        if objItem.ID is not None:
            print("ID: {}".format(objItem.ID))
        if objItem.Imported is not None:
            print("Imported: {}".format(objItem.Imported))
        if objItem.InstallDate is not None:
            print("InstallDate: {}".format(WMIDateStringToDate(objItem.InstallDate)))
        if objItem.Name is not None:
            print("Name: {}".format(objItem.Name))
        if objItem.NoAutoRelease is not None:
            print("NoAutoRelease: {}".format(objItem.NoAutoRelease))
        if objItem.NotSurfaced is not None:
            print("NotSurfaced: {}".format(objItem.NotSurfaced))
        if objItem.NoWriters is not None:
            print("NoWriters: {}".format(objItem.NoWriters))
        if objItem.OriginatingMachine is not None:
            print("OriginatingMachine: {}".format(objItem.OriginatingMachine))
        if objItem.Persistent is not None:
            print("Persistent: {}".format(objItem.Persistent))
        if objItem.Plex is not None:
            print("Plex: {}".format(objItem.Plex))
        if objItem.ProviderID is not None:
            print("ProviderID: {}".format(objItem.ProviderID))
        if objItem.ServiceMachine is not None:
            print("ServiceMachine: {}".format(objItem.ServiceMachine))
        if objItem.SetID is not None:
            print("SetID: {}".format(objItem.SetID))
        if objItem.State is not None:
            print("State: {}".format(objItem.State))
        if objItem.Status is not None:
            print("Status: {}".format(objItem.Status))
        if objItem.Transportable is not None:
            print("Transportable: {}".format(objItem.Transportable))
        if objItem.VolumeName is not None:
            print("VolumeName: {}\n".format(objItem.VolumeName))


def get_shadows_objects():
    # Получает теневые объекты
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_ShadowCopy")
    ListObj = []
    for objItem in colItems:
        if objItem.DeviceObject is not None:
            ListObj.append(objItem)
    return ListObj


def get_shadow_paths(filepath):
    # Получает обычный путь к файлу и превращет в эквивалентный теневой путь к файлу
    drive_letter = search('\w:', filepath).group(0)
    ListObj = get_shadows_objects()
    shadow_paths = []
    for Obj in ListObj:
        try:
            if os.lstat(filepath.replace(drive_letter, Obj.DeviceObject)).st_dev == os.lstat(drive_letter).st_dev:
                shadow_paths.append(filepath.replace(drive_letter, Obj.DeviceObject))
        except FileNotFoundError:
            pass
    return shadow_paths


def unshadow_path(drive_letter, filepath):
    # Превращает теневой путь в обычный
    ListObj = search('.*HarddiskVolumeShadowCopy\d+', filepath).group(0)
    return filepath.replace(ListObj, drive_letter)


def get_last_shadow_path(shadow_paths):
    return max(shadow_paths, key=lambda x: int(search('HarddiskVolumeShadowCopy(\d+)', x).group(1)))


def open_shadow(shadow_path):
    # Открывает теневой файл
    with open(shadow_path, 'rb') as file_handler:
        data = file_handler.read()
        return data


def copy_shadow_as_file(shadow_path, output):
    # Копирует теневой файл как обычный
    with open(shadow_path, 'rb') as file_handler:
        data = file_handler.read()
    with open(output, 'wb') as file_handler:
        file_handler.write(data)



def vss_create(drive_letter):
    # Позволяет создать теневую копию диска
    wmi = win32com.client.GetObject("winmgmts:{impersonationLevel=impersonate}!\\\\.\\root\\cimv2:Win32_ShadowCopy")
    createmethod = wmi.Methods_("Create")
    createparams = createmethod.InParameters
    createparams.Properties_[1].value = "{0}:\\".format(drive_letter)
    results = wmi.ExecMethod_("Create", createparams)
    return results.Properties_[1].value


def vss_delete(shadow_id):
    wcd = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    wmi = wcd.ConnectServer(".", "root\cimv2")
    obj = wmi.ExecQuery(
        "SELECT * FROM Win32_ShadowCopy WHERE ID=\"{0}\"".format(
            shadow_id))
    obj[0].Delete_()

