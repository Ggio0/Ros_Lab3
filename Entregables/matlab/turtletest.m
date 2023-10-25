%% Conexion con nodo maestro
rosinit; 
%% creacion del publisher a las vel
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creacion publicador
velMsg = rosmessage(velPub); %Creacion de mensaje
%% Creacion del cliente para tp abs
tpclint=rossvcclient('/turtle1/teleport_absolute');
tpreq= rosmessage(tpclint);
%% Valores de las velocidades
velMsg.Linear.X =1; %Valor del mensaje
velMsg.Linear.Y =3;
velMsg.Angular.Z=-2;
%% Valores de las pos abs
tpreq.X=cast(5.544445,'single');
tpreq.Y=cast(5.544445,'single');
tpreq.Theta=cast(0,'single');
%% Envio de la pose abs
call(tpclint,tpreq,"Timeout",3)
%% Envio de las vel
send(velPub,velMsg);
%% Creacion del subscriber al pose
pose = rossubscriber('/turtle1/pose', 'turtlesim/Pose');
pause(1)
%% Ultimo msg del pose
lastPose=pose.LatestMessage;
%% Finaliza el nodo maestro en Matlab
rosshutdown