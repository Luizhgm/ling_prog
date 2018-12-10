import machine
import pyb
import time

login_test=dict()
login_test["luiz"] = 0
login_test["micelli"] = 255
"""
Esse login_test, seria substituido por um querry de aprovados login = name e senha = user_id (ou quaisquer outra coisa)
existe o modelo de capitura dos logins e senhas no arquivo  'var/app_flask-instance/leitura de bd para porta', com o resutaldo um pickle exatamente do formato desejado
"""
y4 = machine.Pin('Y4')
adc = pyb.ADC(y4)
servo = pyb.Servo(1)
    
print("Enter name: ")
servo.angle(-90, 50)
while True:
    name=input()

    if name in login_test.keys() :

        if adc.read() == login_test[name]:
            print("Pode entrar")
            pyb.LED((1) + 1).on()
            servo.angle(90, 50)   
            time.sleep_ms(5000)
        else:
            print("'senha' invalida")
        
        print("Enter name: ")
        pyb.LED((1) + 1).off()
        servo.angle(-90, 50)

        
    elif name not in login_test.keys():
        
        print("'login' invalido")
        print("Enter name: ")
        pyb.LED((1) + 1).off()
        servo.angle(-90, 50)
