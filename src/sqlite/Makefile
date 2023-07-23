INCDIR := ./inc/
SRCDIR := ./src/
OUTDIR := ./out/

vpath %.c $(SRCDIR)

CC := gcc
PATHFLAG := -I$(INCDIR)
CFLAGS := -std=c99 $(PATHFLAG) -fPIC
ADD_LIBS :=  -lsqlite3 -lpython3.10
PYTHON_PATH:= $(shell pkg-config --cflags --libs python3)
NUMPY_PATH := -I$(shell pip show numpy | grep -oP "(?<=Location: ).*"$\
			  | awk '{$$1=$$1};1')/numpy/core/include

SRCS := $(wildcard $(SRCDIR)*.c)
OBGS := $(patsubst $(SRCDIR)%.c,$(OUTDIR)%.o,$(SRCS))
DEPS := $(patsubst $(SRCDIR)%.c,$(OUTDIR)%.d,$(ALL_SRCS))

.PHONY : clean build

build: lindex.so

%.so : $(OBGS)
	@mkdir -p $(@D)
	$(CC) $(ADD_LIBS) -shared $^ -o $@

$(OUTDIR)%.o : %.c
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) $(PYTHON_PATH) $(NUMPY_PATH) -c $< -o $@

$(OUTDIR)%.d : %.c
	@mkdir -p $(@D)
	@$(CC) $(CFLAGS) $(PATHFLAG) -M $< | sed "s^$*.o^$(OUTDIR)$*.o^" > $@

include $(DEPS)

clean :
	rm -fr $(OUTDIR)
	rm -fr $(LIBSDIR)
	rm *.so *.db
