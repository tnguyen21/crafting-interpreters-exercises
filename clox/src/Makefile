.SUFFIXES : .c .o

OBJECTS = main.o chunk.o memory.o debug.o value.o vm.o

CC = gcc
CFLAGS = -c

TARGET = clox

$(TARGET) : $(OBJECTS)
	$(CC) -o $(TARGET) $(OBJECTS)

clean :
	rm $(TARGET) $(OBJECTS)

main.o : common.h memory.h main.c
chunk.o : chunk.h  chunk.c
debug.o : debug.h debug.c
memory.o : memory.h memory.c
value.o : value.h value.c
vm.o : vm.h vm.c
