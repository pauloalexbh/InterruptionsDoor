#! /usr/bin/python
# -*- coding: utf-8 -*-
 
import Rpi.GPIO as gpio
import time
 
 
""" Global """
PIN=23
 
""" Funcoes """
def action_press_button(gpio_pin):
    print "Você pressionou o botão do pino %d e agora ele sera desativado" % gpio_pin
 
 
""" Configurando GPIO """
# Configurando o modo do GPIO como BCM
gpio.setmode(gpio.BCM)
 
# Configurando PIN's como INPUT e modo pull-down interno
gpio.setup(PIN, gpio.IN, pull_up_down = gpio.PUD_DOWN)
 
# Adicionando um evento ao GPIO 23 na mudança RISING 0V[LOW] -> 3.3V[HIGH]
gpio.add_event_detect(PIN, gpio.RISING)
 
 
while True:
    try:
        if gpio.event_detected(PIN):
            action_press_button(PIN)
            gpio.remove_event_detect(PIN)
        
        else:
                    print("Botão Desligado")
 
        time.sleep(1)
    except (KeyboardInterrupt):
        print("Saindo...")
        gpio.cleanup()
        exit()
