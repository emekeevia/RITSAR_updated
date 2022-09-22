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
            s += "(" + str(mas[i,j].real) + "," + str(mas[i,j].real) + ")"
            if j == len(mas[0]) - 1 and i != len(mas) - 1:
                s += "\n"
            elif j != len(mas[0]) - 1 and i != len(mas) - 1:
                s += " "
        f.write(s)
        s = ""
    f.close()

#Include Dictionaries
from SARplatformUHF import plat_dict

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
x = img_plane['u']; y = img_plane['v']
points = []
for i in range(10):
    for j in range(20):
        points.append([i, j, 0])
amplitudes = [10 for _ in range(200)]
phs = phsTools.simulate_phs(platform, points, amplitudes)
write_in_file(phs, "../../CLionProjects/Omega-K/Example_with_rectangle.txt")


##############################################################################

#Apply RVP correction
phs_corr = phsTools.RVP_correct(phs, platform)
write_in_file(phs_corr, "../../CLionProjects/Omega-K/Example_with_rectangle_RVP_correct.txt")

#Demodulate phase history with constant reference, if needed 
phs_fixed = phsTools.phs_to_const_ref(phs_corr, platform, upchirp = 1)
write_in_file(phs_fixed, "../../CLionProjects/Omega-K/Example_with_rectangle_constant_ref.txt")

#Apply algorithm of choice to phase history data
#img_pf = imgTools.polar_format(phs_corr, platform, img_plane, taylor = 17)
img_wk = imgTools.omega_k(phs_fixed, platform, taylor = 17, upsample = 2)
write_in_file(phs_fixed, "../../CLionProjects/Omega-K/Example_with_rectangle_finished.txt")
#img_bp = imgTools.backprojection(phs_corr, platform, img_plane, taylor = 17, upsample = 2)

#Output image
imgTools.imshow(img_wk, dB_scale = [-25,0])