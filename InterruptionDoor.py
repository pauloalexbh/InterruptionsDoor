#! /usr/bin/python
# -*- coding: utf-8 -*-
 
import Rpi.GPIO as gpio
from datetime import datetime, timedelta
import time

 
 
""" Global """
Porta=23
PortaEvento = datetime.now()
string PortaEstado = "ND"
 
""" Funcoes """
def action_event_button(gpio_pin):{
 if gpio.input(Porta) == 0:
  PortaEstado = "aberta";
 else:
  PortaEstado = "fechada";
# if datetime.now()>PortaEvento:#esta aqui so para lembrar de como é a comparacao de datetime
# if PortaEvento<(datetime.now()+timedelta(seconds=1)):#nao se pode comparar datetime com timedelta, mas pode-se somar.
 PortaEvento = datetime.now()
 #datahora = datetime.now()
 print "Houve um evento na porta (pino %d) e agora ela está %s \n" % gpio_pin, %PortaEstado
 print (datahora)
 
}
 
""" Configurando GPIO """
# Configurando o modo do GPIO como BCM
gpio.setmode(gpio.BCM)
 
# Configurando PIN's como INPUT e modo pull-down interno
gpio.setup(Porta, gpio.IN, pull_up_down = gpio.PUD_DOWN)
 
# Adicionando um evento ao GPIO 23 na mudança RISING 0V[LOW] -> 3.3V[HIGH]
gpio.add_event_detect(Porta, gpio.BOTH)
 
 
while True:
    try:
        if gpio.event_detected(Porta):
            action_event_button(Porta)
            #gpio.remove_event_detect(PIN)
        
        else:
                    print("Botão Desligado")
 
        time.sleep(1)
    except (KeyboardInterrupt):
        print("Saindo...")
        gpio.cleanup()
        exit()
