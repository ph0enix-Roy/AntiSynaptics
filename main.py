import ctypes
import ctypes.wintypes
from ctypes.wintypes import LPCWSTR

# 定义Windows API函数
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

LoadLibraryEx = kernel32.LoadLibraryExW
LoadLibraryEx.argtypes = [
    ctypes.wintypes.LPCWSTR,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
]
LoadLibraryEx.restype = ctypes.wintypes.HMODULE

FindResourceEx = kernel32.FindResourceExW
FindResourceEx.argtypes = [
    ctypes.wintypes.HMODULE,
    ctypes.wintypes.LPCWSTR,
    ctypes.wintypes.LPCWSTR,
    ctypes.wintypes.WORD,
]
FindResourceEx.restype = ctypes.wintypes.HRSRC

SizeofResource = kernel32.SizeofResource
SizeofResource.argtypes = [ctypes.wintypes.HMODULE, ctypes.wintypes.HRSRC]
SizeofResource.restype = ctypes.wintypes.DWORD

LoadResource = kernel32.LoadResource
LoadResource.argtypes = [ctypes.wintypes.HMODULE, ctypes.wintypes.HRSRC]
LoadResource.restype = ctypes.wintypes.HGLOBAL

LockResource = kernel32.LockResource
LockResource.argtypes = [ctypes.wintypes.HGLOBAL]
LockResource.restype = ctypes.wintypes.LPVOID

FreeLibrary = kernel32.FreeLibrary
FreeLibrary.argtypes = [ctypes.wintypes.HMODULE]
FreeLibrary.restype = ctypes.wintypes.BOOL


# 定义常量
LOAD_LIBRARY_AS_DATAFILE = 2
RT_RCDATA = 10


def read_resource(file_address, resource_type, resource_name):
    # 加载库
    module = LoadLibraryEx(file_address, None, LOAD_LIBRARY_AS_DATAFILE)
    if not module:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        # 查找资源
        resource_info = FindResourceEx(module, resource_type, resource_name, 0)
        if not resource_info:
            raise ctypes.WinError(ctypes.get_last_error())

        # 获取资源大小
        resource_length = SizeofResource(module, resource_info)
        if resource_length == 0:
            raise ctypes.WinError(ctypes.get_last_error())

        # 加载资源
        resource_data = LoadResource(module, resource_info)
        if not resource_data:
            raise ctypes.WinError(ctypes.get_last_error())

        # 锁定资源并获取指针
        resource_ptr = LockResource(resource_data)
        if not resource_ptr:
            raise ctypes.WinError(ctypes.get_last_error())

        resource_bytes = ctypes.string_at(resource_ptr, resource_length)
        resource_bytes = resource_bytes[:]  # 将数组转换为Python字节对象

    finally:
        FreeLibrary(module)

    return resource_bytes


if __name__ == "__main__":
    file_address = input("请输入感染文件地址：")
    resource_type = LPCWSTR(RT_RCDATA)
    resource_name = "EXERESX"
    resource_data = read_resource(file_address, resource_type, resource_name)

    # 将资源数据写入文件（如果需要）
    output_file = input("请输入输出文件地址：")
    with open(output_file, "wb") as f:
        f.write(resource_data)
