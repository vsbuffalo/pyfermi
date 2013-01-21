"""
fermi.py is an experimental Python wrapper to the Fermi assembler
(from Heng Li).

"""
DEFAULT_QUAL = 20

import sys
from array import array
import pdb
from ctypes import *
from Bio import SeqIO

flib = cdll.LoadLibrary("libfermi.so")

class Fermi(object):
    def __init__(self):
        """
        Initialize a call to Fermi.
        """
        self.len = 0
        self.pseq = c_char_p()
        self.pqual = c_char_p()
        self._seq = ""
        self._qual = ""

    def readseq(self, file):
        """
        Use Fermi's readseq API function to read in a FASTA/FASTQ
        file.
        """
        self.len = flib.fm6_api_readseq(file, byref(self.pseq), byref(self.pqual))

    def correct(self, ec_k=c_int(-1)):
        """
        Error correct sequences; this changes the underlying
        sequences.
        """
        assert(self.len > 0)
        flib.fm6_api_correct(ec_k, c_int64(self.len), self.pseq, self.pqual)

    def writeseq(self):
        """
        Write sequences to stdout.
        """
        assert(self.len > 0)
        flib.fm6_api_writeseq(c_int64(self.len), self.pseq, self.pqual)

    def addseq(self, seq, qual=None):
        """
        Add a sequence and optional quality to Fermi; useful for
        directly interfacing with Fermi.
        """
        self._seq += seq + '\x00'
        if qual is not None:
            self._qual += qual + '\x00'
        else:
            self._qual += chr(DEFAULT_QUAL + 33)*len(seq) + '\x00'
        self.pseq = c_char_p(self._seq)
        self.pqual = c_char_p(self._qual)
        self.len += len(seq) + 1

    def exportseq(self):
        assert(self.len > 0)
        pseqs = c_char_p()
        flib.fm6_ext_exportseq(c_int64(self.len), self.pseq, self.pqual, byref(pseqs))
        seqs = pseqs.value
        flib.free_pchar(pseqs)
        return seqs

    def assemble(self, unitig_k=c_int(-1), do_clean=True):
        """
        Assembly sequences with call to fm6_api_unitig(). This outputs
        a FASTQ string.
        """
        assert(self.len > 0)
        do_clean = c_int(int(do_clean))
        tmp = c_void_p()
        punitigs = c_char_p()
        flib.fm6_ext_unitig(unitig_k, self.len, do_clean, self.pseq, self.pqual, byref(tmp))
        flib.fm6_ext_unitig_write(byref(tmp), byref(punitigs))
        unitigs = punitigs.value
        flib.free_pchar(punitigs)
        return unitigs

