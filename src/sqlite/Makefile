INCDIR := ./inc/
SRCDIR := ./src/
OUTDIR := ./out/

vpath %.c $(SRCDIR)

CC := gcc
PATHFLAG := -I$(INCDIR)
LIBSPATHFLAG := -L$(LIBSDIR)
CFLAGS := -std=c99 $(PATHFLAG) -Wall -Werror -Wpedantic -fPIC
CHECK_LIBS := -lcheck -lpthread -lrt

SRCS := $(wildcard $(SRCDIR)*.c)
LIBS_NAMES := $(patsubst $(SRCDIR)%.c,$(LIBSDIR)lib%.so,$(SRCS))
LIBS := $(patsubst $(SRCDIR)%.c,-l%,$(SRCS))

DEPS := $(patsubst $(SRCDIR)%.c,$(OUTDIR)%.d,$(ALL_SRCS))

.PHONY : clean build

build: lindex.so

%.so : $(OUTDIR)%.o
	@mkdir -p $(@D)
	$(CC) -shared $< -o $@

$(OUTDIR)%.o : %.c
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) -c $< -o $@

$(OUTDIR)%.d : %.c
	@mkdir -p $(@D)
	@$(CC) $(CFLAGS) $(PATHFLAG) -M $< | sed "s^$*.o^$(OUTDIR)$*.o^" > $@

include $(DEPS)

clean :
	rm -fr $(OUTDIR)
	rm -fr $(LIBSDIR)
