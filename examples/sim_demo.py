##############################################################################
#                                                                            #
#  This is a demonstration of the ritsar toolset using a simple point        #
#  simulator. Algorithms can be switched in and out by commenting/           #
#  uncommenting the lines of code below.                                     #
#                                                                            #
##############################################################################

#Add include directories to default path list
from numpy import *
from sys import path
import matplotlib.pylab as plt
import matplotlib.cm as cm


path.append('/home/ivan/RITSAR/examples/dictionaries')

def write_in_file(mas, file_path):
    f = open(file_path, 'w')
    s = ""
    for i in range(len(mas)):
        for j in range(len(mas[0])):
            s += "(" + str(mas[i,j].real) + "," + str(mas[i,j].imag) + ")"
            if j == len(mas[0]) - 1 and i != len(mas) - 1:
                s += "\n"
            elif j != len(mas[0]) - 1:
                s += " "
        f.write(s)
        s = ""
    f.close()

def imag(mas, name):
    fig_2 = plt.figure()
    ax = fig_2.add_subplot(111)
    cax = ax.imshow(abs(mas), aspect='equal', cmap=cm.gray)
    ax.set_title(name)
    ax.set_xlabel('Range pixels')
    ax.set_ylabel('Azimuth pixels')
    ax.set_xticks([])
    ax.set_yticks([])
    fig_2.show()

#Include Dictionaries
from SARplatform import plat_dict

#Include SARIT toolset
from ritsar import phsTools
from ritsar import imgTools

#Create platform dictionary
platform = plat_dict()

#Create image plane dictionary
img_plane = imgTools.img_plane_dict(platform, aspect = 1)

#Simulate phase history, if needed
##############################################################################
nsamples = platform['nsamples']
npulses = platform['npulses']
x = img_plane['u']
y = img_plane['v']
points = [[0,0,0]]
#for i in range(10):
#    for j in range(20):
#        points.append([i, j, 0])

amplitudes = [1]
phs = phsTools.simulate_phs(platform, points, amplitudes)
write_in_file(phs, "../../CLionProjects/Omega-K/Example_with_rectangle.txt")
##############################################################################
#print(input())
#print(phs)
#print(input())
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.imshow(abs(phs), aspect='equal', cmap=cm.gray)
ax.set_title('Unfocused model')
ax.set_xlabel('Range pixels')
ax.set_ylabel('Azimuth pixels')
ax.set_xticks([])
ax.set_yticks([])

#Apply RVP correction
#print(phs[0,100:300])
phs_corr = phsTools.RVP_correct(phs, platform)
write_in_file(phs_corr, "../../CLionProjects/Omega-K/Example_with_rectangle_after_RVP_correct.txt")

#Demodulate phase history with constant reference, if needed 
phs_fixed = phsTools.phs_to_const_ref(phs_corr, platform, upchirp = 1)
write_in_file(phs_fixed, "../../CLionProjects/Omega-K/Example_with_rectangle_after_RVP_and_constant_ref.txt")


#Apply algorithm of choice to phase history data
#img_pf = imgTools.polar_format(phs_corr, platform, img_plane, taylor = 17)
img_wk = imgTools.omega_k(phs_fixed, platform, taylor = 17, upsample = 2)
#img_bp = imgTools.backprojection(phs_corr, platform, img_plane, taylor = 17, upsample = 2)
#write_in_file(img_wk, "../../CLionProjects/Omega-K/Example_with_rectangle_finished.txt")

fig_2 = plt.figure()
ax = fig_2.add_subplot(111)
cax = ax.imshow(abs(img_wk), aspect='equal', cmap=cm.gray)
ax.set_title('Focused model')
ax.set_xlabel('Range pixels')
ax.set_ylabel('Azimuth pixels')
ax.set_xticks([])
ax.set_yticks([])
plt.show()
#Output image
#imgTools.imshow(img_wk, dB_scale = [-25,0])