import numpy as np
import matplotlib.pyplot as plt

X = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']
first_class = [21, 23, 24, 21, 21, 0]
second_aclass = [24, 30, 28, 24, 23, 13]
second_bclass = [25, 31, 27, 24, 21, 14]
third_aclass = [25, 27, 27, 28, 21, 14]
third_bclass = [23, 31, 28, 27, 21, 12]

four_aclass = [26, 30, 29, 28, 19, 10]
four_bclass = [27, 30, 31, 25, 17, 9]
five_aclass = [33, 38, 38, 30, 37, 26]
five_bclass = [31, 44, 40, 35, 34, 20]
five_vclass = [39, 44, 38, 30, 31, 25]

six_aclass = [46, 51, 48, 52, 42, 32]
six_bclass = [37, 55, 51, 52, 46, 30]
six_vclass = [37, 54, 54, 55, 40, 31]

seven_aclass = [45, 47, 42, 39, 32, 27]
seven_bclass = [40, 42, 43, 43, 40, 28]
eight_aclass = [40, 43, 48, 41, 35, 26]
eight_bclass = [40, 41, 47, 45, 40, 19]

nine_aclass = [38, 45, 47, 48, 40, 36]
nine_bclass = [40, 42, 50, 43, 47, 37]
ten_class = [46, 47, 56, 48, 47, 18]
eleven_class = [38, 42, 54, 50, 42, 20]

plt.plot(X, nine_aclass, label='9а класс')
plt.plot(X, nine_bclass, label='9б класс')
plt.plot(X, ten_class, label='10 класс')
plt.plot(X, eleven_class, label='11 класс')

'''
plt.plot(X, four_aclass, label='4а класс')
plt.plot(X, four_bclass, label='4б класс')
plt.plot(X, five_aclass, label='5а класс')
plt.plot(X, five_bclass, label='5б класс')
plt.plot(X, five_vclass, label='5в класс')
'''

'''
plt.plot(X, six_aclass, label='6а класс')
plt.plot(X, six_bclass, label='6б класс')
plt.plot(X, six_vclass, label='6в класс')
'''

plt.xlabel('дни недели')
plt.ylabel('баллы')

plt.legend()
plt.grid(True)
plt.show()