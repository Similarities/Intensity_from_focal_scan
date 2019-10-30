# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:15:52 2019

@author: sweedy
"""
import numpy as np
import math


import csv


import matplotlib.pyplot as plt


class Load_text_into_2D_array:


    def __init__(self, filepath, how_many):




        self.file_name = str

        self.file_path = filepath

        self.loaded_array = np.empty([], dtype=np.float32)
        
        self.how_many = how_many
        
        self.length = int
        
        self.namelist = list()




    
    def header_names(self):
        with open(self.file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')
            header_row = next(reader)
            
            
        for index, column_header in enumerate(header_row):
            xx = str(column_header)
            self.namelist.append(xx)
            print( column_header, index)
            
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


    
def substract_a_column(matrix, column, value):
    
    matrix[::,column] = matrix[::, column]-value
    
    return matrix


def multiply_a_column(matrix, column, value):
    
    matrix[::,column] = matrix[::, column]*value
    
    return matrix


    
def avg_to_columns(matrix, column1, column2, name_list):
    
    new = (matrix[::,column1] + matrix[::, column2]) *  0.5
    print(new, matrix[::,0])
    
    matrix = np.column_stack((matrix, new))
    
    new_name = 'avg column '+  str(column1) +' column' + str(column2)
    name_list.append(new_name)
    
    return matrix, name_list
    
    
    
def calc_A_from_two_columns(matrix, column1, column2, name_list):
    
    new = ((matrix[::,column1]*0.5) * (matrix[::, column2]*0.5)) *  math.pi *1E-8
    matrix = np.column_stack((matrix, new))
    
    new_name = 'Area column '+  str(column1) +' column' + str(column2)
    name_list.append(new_name)
    
    return matrix, name_list



def calc_I_from_A_with_values(matrix, column, value1, value2,name_list):
    
    new = value1 *matrix[::,11] / (matrix[::,column]*value2*1E-15)
    matrix = np.column_stack((matrix, new))
    
    new_name = 'intensity '
    name_list.append(new_name)
    
    return matrix, name_list
    
    
def calc_I_in_a0(matrix, column, name_list):

    
    new = 0.855*0.8*((matrix[::,column]*1E-18)**(0.5))
    matrix = np.column_stack((matrix, new))
    
    new_name = 'a0 '
    name_list.append(new_name)
    
    return matrix, name_list


def save_picture(picture_name):

        plt.savefig(picture_name+".png",  bbox_inches="tight", dpi = 1000)
    

first = Load_text_into_2D_array('FokusScanAuswertung.csv', 12)
x = first.loadarray()
substract_a_column(x,0,-20820)
multiply_a_column(x,0,2)
names = first.header_names()
x,names = avg_to_columns(x, 5,6, names)

plt.scatter(x[::,0], x[::,5], label = names[5] , color = 'b' )
plt.scatter(x[::,0], x[::,6], label = names[6], color = 'r' )
plt.scatter(x[::,0], x[::,-1], label = names[-1], color = 'c' )
plt.legend()

x, names = calc_A_from_two_columns(x, 5, 6, names)
x, names = calc_I_from_A_with_values(x,-1, 3, 20, names)
plt.figure(2)
plt.scatter(x[::,0], x[::,-1], label = names[-1], color = 'c' )
plt.legend()
save_picture('I0_of_z_from_moment')

x, names = calc_I_in_a0(x, -1, names)

plt.figure(3)
plt.scatter(x[::,0], x[::,-1], label = names[-1], color = 'r' )
plt.legend()
save_picture('a0_of_z_from_moment')

print(x[::,-1])