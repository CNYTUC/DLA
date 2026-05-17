import time
def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_current_date():
    return time.strftime("%Y-%m-%d", time.localtime())

def get_current_time_only():
    return time.strftime("%H:%M:%S", time.localtime())

def get_current_date_only():
    return time.strftime("%Y-%m-%d", time.localtime())

def get_current_date_and_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def wait(times):
    time.sleep(times)