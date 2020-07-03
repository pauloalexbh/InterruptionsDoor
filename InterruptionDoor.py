#! /usr/bin/python
# -*- coding: utf-8 -*-
 
import Rpi.GPIO as gpio
from datetime import datetime, timedelta
import time

 
 
""" Global """
Porta=23
PortaEvento = datetime.now()
string PortaEstado = "ND"

Tranca=24
TrancaEvento = datetime.now()
string TrancaEstado = "ND"
 
""" Funcoes """
 def action_event_registrar(gpio_pin):{
  if gpio_pin == Porta:{
   if gpio.input(gpio_pin) == 0:
    PortaEstado = "aberta";
   else:
    PortaEstado = "fechada";
   # if datetime.now()>PortaEvento:#esta aqui so para lembrar de como é a comparacao de datetime
   # if PortaEvento<(datetime.now()+timedelta(seconds=1)):#nao se pode comparar datetime com timedelta, mas pode-se somar.
   PortaEvento = datetime.now()
   #datahora = datetime.now()
   print "Houve um evento na porta (pino %d) e agora ela está %s \n" % gpio_pin, %PortaEstado
   print (PortaEvento)
  }
   
  if gpio_pin == Tranca:{
   if gpio.input(gpio_pin) == 0:
    TrancaEstado = "aberta";
   else:
    TrancaEstado = "fechada";
   # if datetime.now()>PortaEvento:#esta aqui so para lembrar de como é a comparacao de datetime
   # if PortaEvento<(datetime.now()+timedelta(seconds=1)):#nao se pode comparar datetime com timedelta, mas pode-se somar.
   TrancaEvento = datetime.now()
   #datahora = datetime.now()
   print "Houve um evento na tranca (pino %d) e agora ela está %s \n" % gpio_pin, %PortaEstado
   print (TrancaEvento)
  } 
 }
 
 def action_event_button(gpio_pin):{
  if TrancaEstado == "fechada":{
   if PortaEstado == "fechada":{
    if (PortaEvento+timedelta(seconds=1))>TrancaEvento:{
     #Aciona desliga tudo.
     print "\nTranca fechada enquanto a porta está recém fechada. Acionar Desligar tudo."
    }
    else {
     #Aciona Boa Noite.
     print "\nTranca fechada enquanto a porta está fechada a tempos. Acionar Boa Noite."
    }
   }
   #Não há fechamento da tranca com porta aberta, entao nao necessita de else.
  }
  if TrancaEstado == "aberta":{
   if PortaEstado == "fechada":{
    if ((datetime.now()-timedelta(milliseconds=900))>PortaEvento)and((datetime.now()-timedelta(milliseconds=900))>TrancaEvento):{
    #A porta foi fechada sem ser trancada depois de meio segundo. Não fazer nada.
     print "\nA porta foi fechada sem ser trancada depois de meio segundo. Não fazer nada."
    }
    #E necessario esperar para saber se a porta sera trancada. Entao nao deve ter else
   }
   if PortaEstado == "aberta":{
    if ((datetime.now()-timedelta(milliseconds=500))<TrancaEvento):{
     #A tranca estava aberta a tempo e a porta foi aberta. Não fazer nada.
     print "\nA tranca estava aberta a tempo e a porta foi aberta. Não fazer nada."
    }
    else {
     #A tranca foi aberta e logo depois a porta foi aberta. Acionar bom dia.
     print "\nA tranca foi aberta e logo depois a porta foi aberta. Acionar bom dia."
    }
    #A porta foi aberta 
   }
  }
 }
 
""" Configurando GPIO """
# Configurando o modo do GPIO como BCM
gpio.setmode(gpio.BCM)
 
# Configurando PIN's como INPUT e modo pull-down interno
gpio.setup(Porta, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(Tranca, gpio.IN, pull_up_down = gpio.PUD_DOWN)
 
# Adicionando um evento ao GPIO 23 na mudança RISING 0V[LOW] -> 3.3V[HIGH]
gpio.add_event_detect(Porta, gpio.BOTH, callback=action_event_registrar)
gpio.add_event_detect(Tranca, gpio.BOTH, callback=action_event_registrar) 
 
while True:
    try:
        if gpio.event_detected(Porta):
            action_event_button(Porta)
            #gpio.remove_event_detect(PIN)
        
        else:
                    print("Botão Desligado")
        if gpio.event_detected(Tranca):
            action_event_button(Tranca)
            #gpio.remove_event_detect(PIN)
        
        else:
                    print("Botão Desligado")
 
        time.sleep(1)
    except (KeyboardInterrupt):
        print("Saindo...")
        gpio.cleanup()
        exit()
