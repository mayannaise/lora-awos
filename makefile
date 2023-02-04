THIS_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(THIS_DIR)style.mk

.PHONY: all
all:
	@echo "$(RED)Please run 'make install_tx' or 'make install_rx'$(DEFAULT)"

.PHONY: setup
setup:
	@echo "$(YELLOW)Installing prereqs$(DEFAULT)"
	$(AT) sudo apt install -y python3-pip python3-rpi.gpio
	$(AT) pip3 install --user pyserial
	@echo "$(GREEN)Done$(DEFAULT)"

.PHONY: install_tx
install_tx:
	@echo "$(YELLOW)Installing transmitter service$(DEFAULT)"
	$(AT) sudo systemctl enable $(THIS_DIR)lora-transmitter.service
	$(AT) sudo systemctl start lora-transmitter.service
	@echo "$(GREEN)Done$(DEFAULT)"

.PHONY: install_rx
install_rx:
	@echo "$(YELLOW)Installing receiver service$(DEFAULT)"
	$(AT) sudo systemctl enable $(THIS_DIR)lora-receiver.service
	$(AT) sudo systemctl start lora-receiver.service
	@echo "$(GREEN)Done$(DEFAULT)"
