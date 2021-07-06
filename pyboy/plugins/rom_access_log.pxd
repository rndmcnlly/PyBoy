from pyboy.plugins.base_plugin cimport PyBoyPlugin

cdef class RomAccessLog(PyBoyPlugin):
    cdef object log_array
    cdef object log_file