# -*- coding: utf-8 -*-
# Auteur : Jean-Christophe HENRY 
# Mail   : jeanchristophe.henry@orange.com 
# Service: DTSI/DSI CCMD
# Script permettant d'intéragir directement avec les drones
# Pour ajouter des actions il faut aller dans la méthode
# if __name__ == '__main__':
# Puis ajouter une nouvelle ligne thread

# Import the built-in socket and time modules
import socket
import time
from threading import Thread, Event
 

#################################################################
#                   CONFIGURATION DU SOCKET                     #
#################################################################
# IP and port of Tello
tello_address = ('192.168.10.1', 8889)

# Event object used to send signals from one thread to another
stop_event = Event()

# Ajout du socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# On bind sur quel port on veut faire nos échanges
sock.bind(('', 9000))
# On ajoute un time out de 8 secondes
sock.settimeout(8)

#################################################################
#                   FONCTION POUR LES ACTIONS                   #
#################################################################
# Function to send messages to Tello
def send(message, sleep = 0):
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sock envoi message: " + message)
  except Exception as e:
    print("Sock erreur envoi: " + str(e))

    # Delay for a user-defined period of time
  time.sleep(sleep)

# Function that listens for messages from Tello and prints them to the screen
def receive():
  try:
    response, ip_address = sock.recvfrom(128)
    print("receive-message recu : " + response.decode(encoding='utf-8') + " from Tello with IP: " + str(ip_address))
  except Exception as e:
    print("receive-erreur de reception : " + str(e))


# do_actions permet d'automatiser les actions pour le drone
def do_actions(action, sleep):
    """
    Function that should timeout after 5 seconds.
    """
    # Ask Tello about battery status
    # send("battery?")

    # Receive battery response from Tello
    #receive()

    #time.sleep(3)

    # Close the UDP socket
    #sock.close()
    #print("---------------------------------")
    #print("Envoi de la commande : ")
    print(">do_action : " + action)
    send(action, sleep)

    # Receive response from Tello
    receive()

    # Here we make the check if the other thread sent a signal to stop execution.
    if stop_event.is_set():
        sock.close()
        print("Le socket est clos")
 

 ##########################################################################
 # On utilise la fonction do_actions et on éxécute le programme dans main #
 # Si on veut ajouter une action alors il faudra créer un autre thread    #
 ##########################################################################
if __name__ == '__main__':
    print("------------------Debut du programme------------------")

    # l'action command permet d'exécuter une commande sur le drone
    action1_thread = Thread(target=do_actions("command", 3))
    # Je demande le niveau de batterie du drone
    action2_thread = Thread(target=do_actions("battery?", 3))

    # Je demande que le drone de partir vers le haut
    action3_thread = Thread(target=do_actions("takeoff", 3))
 
    # Je demande que le drone avance
    action4_thread = Thread(target=do_actions("forward 200", 3))

    # Je demande que le drone de faire un flip à gauche
    action5_thread = Thread(target=do_actions("flip l", 3))

    # Je demande que le drone d'atterrir'
    action6_thread = Thread(target=do_actions("land", 3))

    # Here we start the thread and we wait 5 seconds before the code continues to execute.
    action1_thread.start()
    action2_thread.start()
    action3_thread.start()
    action4_thread.start()
    action5_thread.start()
    action6_thread.start()


    action1_thread.join(timeout=8)
    action2_thread.join(timeout=8)
    action3_thread.join(timeout=8)
    action4_thread.join(timeout=8)
    action5_thread.join(timeout=8)
    action6_thread.join(timeout=8)

    # We send a signal that the other thread should stop.
    stop_event.set()
 
    print("----------------Fin du programme-----------------")