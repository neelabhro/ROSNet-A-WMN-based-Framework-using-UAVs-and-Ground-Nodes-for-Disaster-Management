clear;
clc;
close all;

%a = [61 62.23905511 33;60 46.35567162 33;60 37.69618508 33;61 52.01258875 180.9;60 30.46412088 180.9;60 53.36407104 180.9; 7 3.578668071 180.9; 14 12.38943535 180.9;16 26.1126008 180.9]
file = [0.058;1;2;5;10;15;20;30]
speed = [19.5; 13.25;13.33;26.5597;25.49;22.57499;40.39;37.688]
figure;
%plot(a);
%A = a(1:8,1);
plot(file,speed);
title('Transfer from Laptop to Laptop');
xlabel('File size in Mb');
ylabel('Transfer speed in Mbps');
