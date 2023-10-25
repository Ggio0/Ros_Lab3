import rospy
from geometry_msgs.msg import Twist
#from keyControl import getkey, pubVel
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
from numpy import pi

TERMIOS = termios

'''
 Esta función publica comandos de velocidad para controlar el movimiento de la tortuga.
 Recibe los siguientes argumentos: 
 vel_x: Velocidad lineal en la dirección x.
 vel_y: Velocidad lineal en la dirección y.
 ang_z: Velocidad angular alrededor del eje z.
 t:  Duración durante la cual se deben aplicar los comandos de velocidad en segundos.
 nt: Duración durante la cual se deben aplicar los comandos de velocidad en nanosegundos.
'''
def pubVel(vel_x, vel_y, ang_z, t, nt):
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('velPub', anonymous=False)
    vel = Twist()
    vel.linear.x = vel_x
    vel.linear.y = vel_y
    vel.angular.z = ang_z
    #rospy.loginfo(vel)
    endTime = rospy.Time.now() + rospy.Duration(t,nt)
    while rospy.Time.now() < endTime:
        pub.publish(vel)




'''
Esta función lee una entrada de un solo carácter.

'''
def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)

    return c


'''
Esta función teleporta la tortuga a una posición absoluta con una orientación específica 
en coordenadas absolutas.
 Recibe los siguientes argumentos: 
 x: Posición en coordenadas absolutas en x.
 y: Posición en coordenadas absolutas en y.
 ang: Posición angular en coordenadas absolutas en z.
 '''
def teleport(x, y, ang):
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        resp1 = teleportA(x, y, ang)
        print('Teleported to x: {}, y: {}, ang: {}'.format(str(x),str(y),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))


'''
Entra en un bucle que escucha las pulsaciones de teclas del usuario donde  
dependiendo de la tecla presionada, realiza la accion correspondiente.
'''
def run():
    keypres='m'
    while(keypres!=b'\x1b'):
        keypres=(getkey())
    
        if(keypres==b'w'):
            pubVel(1,0,0,0.0001,0)
        if(keypres==b's'):
            pubVel(-1,0,0,0.0001,0)
        if(keypres==b'a'):
            pubVel(0,0,1,0.0001,0)
        if(keypres==b'd'):
            pubVel(0,0,-1,0.0001,0)
        if(keypres==b'r'):
            teleport(5.544445, 5.544445, 0)
        if(keypres==b' '):
            pubVel(0,0,pi/2,1,0)
        print(keypres)
    print('out')
if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass