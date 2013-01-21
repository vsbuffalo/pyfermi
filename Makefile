CC = clang
LIBS = -lpthread -lm -lz
OBJS =	utils.o seq.o ksa.o ksa64.o rld.o exact.o merge.o sub.o correct.o \
	build.o smem.o unitig.o seqsort.o cmp.o cmd.o example.o \
	ksw.o mag.o bubble.o scaf.o bcr.o bprope6.o ropebwt.o ext.o kstring.o

all: fermi/*.c
	$(CC) -fpic -c ext.c -o fermi/ext.o
	$(CC) -fpic -Ifermi -c kstring.c -o fermi/kstring.o
	make -C fermi/ CFLAGS='-fpic'
	(cd fermi; $(CC) $(LIBS) -shared -o ../libfermi.so $(OBJS))

clean:
	( cd fermi; make clean )
