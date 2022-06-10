import re, winreg, json
import os


def parse_data(full_path):
    try:
        full_path = re.sub(r'/', r'\\', full_path)
        hive = re.sub(r'\\.*$', '', full_path)
        if not hive:
            raise ValueError('Invalid \'full_path\' param.')
        if len(hive) <= 4:
            if hive == 'HKLM':
                hive = 'HKEY_LOCAL_MACHINE'
            elif hive == 'HKCU':
                hive = 'HKEY_CURRENT_USER'
            elif hive == 'HKCR':
                hive = 'HKEY_CLASSES_ROOT'
            elif hive == 'HKU':
                hive = 'HKEY_USERS'
        reg_key = re.sub(r'^[A-Z_]*\\', '', full_path)
        reg_key = re.sub(r'\\[^\\]+$', '', reg_key)
        reg_value = re.sub(r'^.*\\', '', full_path)
        return hive, reg_key, reg_value
    except:
        return None, None, None

def query_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
        winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def get_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
        value_of_value, value_type = winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", value_of_value]
    except:
        return ["0", "0"]

def dec_value(c):
    c = c.upper()
    if ord('0') <= ord(c) and ord(c) <= ord('9'):
        return ord(c) - ord('0')
    if ord('A') <= ord(c) and ord(c) <= ord('F'):
        return ord(c) - ord('A') + 10
    return 0

def str_to_bin(s):
    res = b""
    for i in range(0, len(s), 2):
        a = dec_value(s[i])
        b = dec_value(s[i + 1])
        res += (a * 16 + b).to_bytes(1, byteorder='big')
    return res

def str_to_dec(s):
    s = s.upper()
    res = 0
    for i in range(0, len(s)):
        v = dec_value(s[i])
        res = res*16 + v
    return res


def set_value(full_path, value, value_type):
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        if 'REG_BINARY' in value_type:
            if len(value) % 2 == 1:
                value += '0'
            value = str_to_bin(value)
        if 'REG_DWORD' in value_type:
            if len(value) > 8:
                value = value[:8]
            value = str_to_dec(value)
        if 'REG_QWORD' in value_type:
            if len(value) > 16:
                value = value[:16]
            value = str_to_dec(value)                 
        
        winreg.SetValueEx(opened_key, value_list[2], 0, getattr(winreg, value_type), value)
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def delete_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        winreg.DeleteValue(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def query_key(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2], 0, winreg.KEY_READ)
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def create_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return ["1", "1"]
    except:
        return ["0", "0"]


def delete_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.DeleteKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return ["1", "1"]
    except:
        return ["0", "0"]

def Registry(ID, full_path, name_value, value, v_type):

    if ID == "GET VALUE":
        res = get_value(full_path + r'\\' + name_value)     

    elif ID == "SET VALUE":
        res = set_value(full_path + r'\\' + name_value, value, v_type)       

    elif ID == "CREATE KEY":
        res = create_key(full_path)

    elif ID == "DELETE KEY":
        res = delete_key(full_path + r'\\')
    if(ID == "GET VALUE"):
        if '0' in res[0]:
            return "Invalid operation!"
        else:
            return str(res[1])
    else:
        if '0' in res[0]:
            return "Invalid operation!"
        else: 
            return "Successful!"

