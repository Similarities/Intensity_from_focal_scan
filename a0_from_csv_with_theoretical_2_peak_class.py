# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:15:52 2019

@author: sweedy


"""
import numpy as np
import math


import csv


import matplotlib.pyplot as plt


class Load_text_into_2D_array_and_calc:


    def __init__(self, filepath, how_many):


        self.file_name = str

        self.file_path = filepath

        self.loaded_array = np.empty([], dtype=np.float32)
        
        self.how_many = how_many
        
        self.length = int
        
        self.namelist = list()

        self.result_name = str()



    
    def header_names(self):
        
        with open(self.file_path) as csv_file:
            
            reader = csv.reader(csv_file, delimiter='\t')
            
            header_row = next(reader)
            
            
        for index, column_header in enumerate(header_row):
            
            xx = "column" + str(index) + ': ' +str(column_header) 
            
            self.namelist.append(xx)
            
            print( xx, index)
            
        return self.namelist





    def test_length(self):
        
        
        test = np.loadtxt(self.file_path, skiprows=(1), usecols=(0,))
        
        self.loaded_array = np.zeros(len(test))





    def loadarray(self):
        
        self.test_length()
        
        
        for x in range(0, self.how_many):
            
            liste1=np.loadtxt(self.file_path, skiprows=(1), usecols=(x,))
            
            matrix = np.array((liste1))
            
            self.loaded_array = np.column_stack((self.loaded_array, matrix))
            

        self.loaded_array = np.delete(self.loaded_array, 0, 1)


        return self.loaded_array
    
    

    
    def substract_a_column(self, column, value):
    
        self.loaded_array[::,column] = self.loaded_array[::, column]-value
    
        return self.loaded_array
    
    
    
    def multiply_a_column(self, column, value):
    
        self.loaded_array[::,column] = self.loaded_array[::, column]*value
    
        return self.loaded_array


    
    def avg_to_columns(self, column1, column2):
        
    
        new = (self.loaded_array[::,column1] + self.loaded_array[::, column2]) *  0.5
        #print(new, matrix[::,0])
    
        self.loaded_array = np.column_stack((self.loaded_array, new))
    
        new_name ='avg column '+  str(column1) +' column ' + str(column2)
        
        self.namelist.append(new_name)
        
        print(self.namelist[-1])

    
        return self.loaded_array, self.namelist
    
    
    
    def calc_A_from_two_columns(self, column1, column2):
        
    
        print(np.min(self.loaded_array[::, column1]), 'minimum focus diameter 1/e')
        
        print(np.min(self.loaded_array[::, column2]), 'minimum focus diameter 1/e')
    
        new = ((self.loaded_array[::,column1] *0.5) * (self.loaded_array[::, column2] *0.5)) *  math.pi *1E-8
        
        self.loaded_array= np.column_stack((self.loaded_array, new))
    
        new_name = 'Area column '+  str(column1) +' column' + str(column2)

        
        self.namelist.append(new_name)
        
        print(self.namelist[-1])
    
        return self.loaded_array, self.namelist



    def calc_I_from_A_with_values(self, column, value1, value2):
        
        #print(self.loaded_array[::,11], ' Q-value')
    
        new = value1 * self.loaded_array[::,11] / (self.loaded_array[::,column] *value2 )
        
        self.loaded_array = np.column_stack((self.loaded_array, new))
    
        new_name = 'Intensity'
        
        self.namelist.append(new_name)
        
        print(self.namelist[-1])
    
        return self.loaded_array, self.namelist
    
    
    def calc_I_in_a0(self, column):

    
        new = 0.855 *0.8 *((self.loaded_array[::, column] *1E-18) **(0.5))
        
        self.loaded_array = np.column_stack((self.loaded_array, new))
    
        new_name = 'a0(1/e) '

        self.namelist.append(new_name)
        
        print(self.namelist[-1])
    
        return self.loaded_array, self.namelist



    def calc_peak(self, sign):
    
        if sign == True: 
            
            new  = self.loaded_array[::,-1] * (2.7 **0.5)
            
            self.loaded_array = np.column_stack((self.loaded_array, new))
            
            new_name = 'a0_peak'

            
        
        else:
            
            new = self.loaded_array[::, -1] *2.7
            
            self.loaded_array = np.column_stack((self.loaded_array, new))
             
            new_name = 'IL_peak'
            
        self.namelist.append(new_name)
        
        print(self.namelist[-1])
        
        return self.loaded_array, self.namelist




def save_picture(picture_name):

        plt.savefig(picture_name+".png",  bbox_inches="tight", dpi = 1000)





# execute the experimental evaluation from .csv
first = Load_text_into_2D_array_and_calc('FokusScanAuswertung.csv', 12)

first.loadarray()

names = first.header_names()

#substract_a_column(column, value) -- in order to correct for relative motor position ('0')
first.substract_a_column(0,-20820)

#multiply_a_column(column, value) -- here stepsize of motor [um]
first.multiply_a_column(0,5)

#avg_to_columns(column1, column2)
x, names = first.avg_to_columns(5,6)

# plot w(z) beam waist of defocusing range
plt.figure(1)
plt.scatter(x[::,0], x[::,5], label = names[5] , color = 'b' )
plt.scatter(x[::,0], x[::,6], label = names[6], color = 'r' )
plt.scatter(x[::,0], x[::,-1], label = names[-1], color = 'c' )
plt.legend()


# now calculate to IL, a0 etc.

# calculates area from (column1, column2)
first.calc_A_from_two_columns( 5, 6)

#calculate from area to Intensity (last column, laser energy [J], laser pulse duration [s])
first.calc_I_from_A_with_values(-1, 2.3, 22*1E-15)

# calc_I_in_a0(column) - -1 is the last column appended which is IL
first.calc_I_in_a0( -1)

# calculates peak value by multiplying x 2.7 if evaluation was done in 1/e for intensity
# set false for intensity
# set true for a0 (multiplys by 2.7 ** 0.5)
x, names = first.calc_peak(True)



plt.figure(2)

fig, ax = plt.subplots()

ax.scatter(x[::,0], x[::,-1], label = names[-1], color = 'c')
ax.set_yscale('log')
ax.grid(True)
ax.legend()















       
        
        
class theoretical_conversion:
    
        # to be given in defocusing length [1E-4 m], focal length f in [cm], beam diameter D in [cm], 
        # laser energy EL in [J], laser pulse duration tauL in [s], normalization factor < 1 -- to adjust to experimental eval.
    def __init__ (self, defocusing_length, f, D, EL,tauL, normalization_factor):
        
        self.defocusing_length = defocusing_length
        
        self.f = f
        
        self.diameter = D
        
        self.energy = EL
        
        self.tauL = tauL
        
        self.normalization = normalization_factor
        
        self.array_z = []
        
        self.array_neg_z = []
        
        self.array_neg_IL = []
        
        self.array_IL = []
        
        self.array_neg_a0 = []
        
        self.array_a0 = []
        
        
        
    def calc_theoretical(self): 
    
        from theoretical_I_importable import Main
    
        aha = Main(self.defocusing_length, self.f, self.diameter , self.energy)
        
        aha.defocusin_w0()
        
        self.array_IL, self.array_z, self.array_a0 = aha.defocusing_I(self.tauL)
        
        #unfortunately does the external function return false form of array (list and not np)
        self.array_IL = np.array(self.array_IL)
        
        self.array_a0 = np.array(self.array_a0)
        
        self.array_z = np.array(self.array_z)
        
        self.array_IL[::] = self.array_IL* self.normalization
            
        self.array_a0[::]= self.array_a0[::]* (self.normalization ** 0.5)
            
            
        self.array_z[::] = self.array_z[::]*1E4 
            

    
        
        return self.array_z, self.array_IL, self.array_a0
        
        
        
        
        
        
        
    def calc_negative_values(self):
        
        self.array_neg_z[::] = -self.array_z[::-1]
            
        self.array_neg_IL [::]= self.array_IL[::-1] 
            
        self.array_neg_a0 [::]= self.array_a0[::-1]
            
        return self.array_neg_z, self.array_neg_IL, self.array_neg_a0
        
        





    def calc_a0_with_GDD(self, GDD):
        
        GDD = GDD*1E-30

    
        t_chirped =( (self.tauL **4 + 16*(0.7)*GDD **2) ** 0.5 ) /self.tauL
        print(t_chirped, 't_chirped')
        ratio = t_chirped/self.tauL
        print(ratio, 'ratio')
    

        self.array_IL[::] = self.array_IL[::] / ratio
        self.array_a0[::] = self.array_a0[::] / (ratio **0.5)


        return self.array_z, self.array_IL, self.array_a0
    
    
    def calc_to_peak(self):
    
        self.array_IL[::] = self.array_IL[::] * 2.7
            
        self.array_a0[::] = self.array_a0[::] * (2.7 **0.5)


        
        return self.array_z, self.array_IL, self.array_a0



        
    
  


theo = theoretical_conversion(55, 150, 6, 2.3, 22*1E-15, 0.5)

theo.calc_theoretical()

x, IL, a0 = theo.calc_to_peak()

xneg, ILneg, a0neg = theo.calc_negative_values()

ax.plot(x, a0, label = "theoretical a0_peak", color = "r" )

ax.plot(xneg, a0neg, color = "r" )


# now with GDD in [fs^2]
x, IL, a0 = theo.calc_a0_with_GDD(900)

xneg, ILneg, a0neg = theo.calc_negative_values()

ax.plot(x, a0, label = 'theo a0_peak + 900fs**2', color = "b")

ax.plot(xneg, a0neg, color = "b" )






ax.legend()

ax.set_xlim(-3000,6000)

save_picture('a0_of_z_from_2.moment_peak')

