from pyboy.plugins.base_plugin cimport PyBoyPlugin

cdef class VramAccessLog(PyBoyPlugin):
    cdef object log_array
    cdef object log_file