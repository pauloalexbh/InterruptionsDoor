import RPi.GPIO as gpio
from datetime import datetime, timedelta
import time

"""Global"""
Porta=23
PortaEvento = datetime.now()
PortaEstado = "ND"

Tranca=24
TrancaEvento = datetime.now()
TrancaEstado = "ND"

"""Funcoes"""
def evento_registrar(gpio_pin):
    global PortaEvento, PortaEstado, TrancaEvento, TrancaEstado
    if gpio_pin == Porta:
        if gpio.input(gpio_pin) ==0:
            PortaEstado = "aberta"
        if gpio.input(gpio_pin) ==1:
            PortaEstado = "fechada"
        PortaEvento = datetime.now()
        
        print("Houve um evento na porta (pino %d) e agora ela esta %s" % (gpio_pin, PortaEstado))
        print(PortaEvento)
        
    
    if gpio_pin == Tranca:
        if gpio.input(gpio_pin) == 0:
            TrancaEstado = "aberta"
        else:
            TrancaEstado = "fechada"
        TrancaEvento = datetime.now()
        print("Houve um evento na tranca (pino %d) e agora ela esta  %s" % (gpio_pin,TrancaEstado))
        print(TrancaEvento)
    print("\n")

def evento_interacao(gpio_pin):
    if gpio_pin == Porta:
        if PortaEstado == "aberta":
            if PortaEvento < (TrancaEvento+timedelta(milliseconds=900)):
                #Alguem entrando ou saindo de casa - Acionar Bom Dia
                print("Alguem entrando ou saindo de casa - Acionar Bom Dia.")
            else:
                print("Porta aberta sem interação com a Tranca. Fazer nada.")
        if PortaEstado == "fechada":
            print("Porta fechada. Não fazer nada. Se houver interação da Tranca, ela chamará a ação.")
    if gpio_pin == Tranca:
        if TrancaEstado == "fechada":
            if TrancaEvento > PortaEvento+timedelta(seconds=5):
                print("Tranca fechada sem interação com a Porta. Acionar Boa Noite.")
            else:
                print("Tranca fechada com interação com a Porta. Acionar Desliga Tudo.")
        if TrancaEstado == "aberta":
            time.sleep(0.5)
            if TrancaEvento>PortaEvento:
                print("Tranca aberta sem interação com a Porta. Acionar Bom Dia.")
            else:
                print("Tranca aberta com interação com a Porta. A ação foi tomada pela Porta.")

"""Configurando GPIO"""
#Configurando o modo do GPIO como BCM
gpio.setmode(gpio.BCM)

#Configurando PINs como INPUT e modo PULL-DOWN interno
gpio.setup(Porta, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(Tranca, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# Adicionando evento aos pinos GPIO 23 e GPIO24
gpio.add_event_detect(Porta, gpio.BOTH, callback=evento_registrar, bouncetime=300)
gpio.add_event_detect(Tranca, gpio.BOTH, callback=evento_registrar, bouncetime=300)

while True:
    try:
        if gpio.event_detected(Porta):
            print("acionando interacao")
            evento_interacao(Porta)
        else:
            print ("Aguardando")
        if gpio.event_detected(Tranca):
            print("acionando interacao")
            evento_interacao(Tranca)
        else:
            print ("Aguardando")
            
        time.sleep(1)
        
    except (KeyboardInterrupt):
        print("Saindo")
        gpio.cleanup()
        exit()
            