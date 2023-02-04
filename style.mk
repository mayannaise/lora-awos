# common colour definitions
BOLD         := $(shell tput -Txterm bold)
BLACK        := $(BOLD)$(shell tput -Txterm setaf 0)
RED          := $(BOLD)$(shell tput -Txterm setaf 1)
GREEN        := $(BOLD)$(shell tput -Txterm setaf 2)
YELLOW       := $(BOLD)$(shell tput -Txterm setaf 3)
LIGHTPURPLE  := $(BOLD)$(shell tput -Txterm setaf 4)
PURPLE       := $(BOLD)$(shell tput -Txterm setaf 5)
BLUE         := $(BOLD)$(shell tput -Txterm setaf 6)
WHITE        := $(BOLD)$(shell tput -Txterm setaf 7)
DEFAULT      := $(shell tput sgr0)

# hide build commands unless specified by user when running make:
# cmdline$ AT= make app
AT?=@

# hide additonal make output
MAKE=make --no-print-directory
