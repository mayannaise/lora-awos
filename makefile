THIS_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(THIS_DIR)style.mk

.PHONY: all
all:
	@echo "$(RED)Please run 'make install_tx' or 'make install_rx'$(DEFAULT)"

.PHONY: setup
setup:
	@echo "$(YELLOW)Installing prereqs$(DEFAULT)"
	$(AT) sudo apt install -y python3-pip python3-rpi.gpio python3-serial
	$(AT) sudo pip3 install adafruit-circuitpython-ssd1306 adafruit-circuitpython-framebuf adafruit-circuitpython-rfm9x
	@echo "$(GREEN)Done$(DEFAULT)"

.PHONY: install_service
install_service:
	@echo "$(YELLOW)Installing service$(DEFAULT)"
	$(AT) sudo systemctl enable $(THIS_DIR)lora.service
	$(AT) sudo systemctl daemon-reload
	$(AT) sudo systemctl start lora.service
	@echo "$(GREEN)Done$(DEFAULT)"
