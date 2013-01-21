# pyfermi -- python interface to the Fermi assembler

**pyfermi** is an Python interface to Heng Li's [Fermi
  assembler](https://github.com/lh3/fermi). **Use it with caution, as
  it's experimental and in beta**.

## Example

    import fermi
    import random
    random.seed(0)
    def random_reads(seq, n, rlen=50):
        for i in range(n):
            pos = random.randint(0, len(seq)-rlen)
            yield seq[pos:(pos+rlen)]

    seq = """AACAAGATGGCCCTCTACGAGCAGTTCAGCGTCCCCTCCCAGCGCTTCGCCGCCAACGCCGCCAACACCGCCCCAGCCGCCGCCCCCCGCCCCGCCGCCAGCTACGCCGCCGTCTCCTCCGCCTCCGCCGGACAGATTGGTGGGATCGACAGACCTCTCTTTCCATCATTTTGCGTGCCTTCAAATGAACCTGTGCGTTTGCCCGAACACATCAAGACCAACTCGAGTGGGCGGGATGGCCAGGCTATATCTGGGAGGCTTTCCACCCAGCTTAAGAGCAAGGACGCCTATGCTGCAGGATCGACTGCTGAGTGTAGTAGTTCACAGCGTAGAGACAACAACAACAATAGCATGAAGAATTCTTCTGGGAAGAAGTTGACTAACGATGATGATTTTACGGTTCCTTCTGTCTTCTGCTCTGGAGCGCGCCCTCGTTCCAACCATGAGGAAGTGAGGATCCAAGAGAATGCCACACCCTTCCCAGCTACAAGTCCGTATAAGAGTGGGCCTACGGTGTCCAAACCAACTGCAAAATTTCCCAACACCGACAAGAGGTACCTGGAAGGAAGGAACGCGTCGGACACGAGATCAAGGGACTCTCCAAGTATTATCAGGGACAAAGCACCAGCAAACACAACGACAAACTTTTTGGAAACTGAAGAGAGGACTTCATCGTTCCAATTTTCTGCAGAGAAGACAATGGGTAAAAGAGATGACAAAGGTTCTTCGTATAGTAGGGTAAAAGAGACGAGCAGTATAAATGTTTCTGATAAGCAACATTCCCGAAACGAGGGGCATCAGGC"""
    fermi = Fermi()
    for read in random_reads(seq, 50, 70):
        fermi.addseq(read)
    fermi.correct()
    tigs = fermi.assemble(do_clean=True)

## Notes

`ext.c` contains some extra C functions needed to wrap fermi. These
are separate from fermi. In some cases, I need klib functions not
fermi, for example `ksprintf` from `kstring.c`. I try to keep things
seperate so fermi can be updated without breaking everything.