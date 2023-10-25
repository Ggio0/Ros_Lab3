import rospy
from geometry_msgs.msg import Twist
#from keyControl import getkey, pubVel
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
from numpy import pi

TERMIOS = termios

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
def teleport(x, y, ang):
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        resp1 = teleportA(x, y, ang)
        print('Teleported to x: {}, y: {}, ang: {}'.format(str(x),str(y),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))


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