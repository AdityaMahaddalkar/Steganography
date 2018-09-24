'''
Simple image cryptography example.
More improvisation required
Note: As picture is 2700 x 1800 = 4860000 characters can be hidden
Defect : The contrast and color quality of image changes drastically, improvement needed
'''

import cv2
import numpy as np


class Steg:

    def __init__(self):
        self.image = cv2.imread('NationalPark.jpg')
        self.tailer = (7, 3, 3)   # Ascii value for DEL 111 11 11 ~ 127
        ''' test
        print(self.image.shape)
        '''

    def ret_str_len_7(self, string):
        return '0'*(7-len(string)) + string

    def ret_str_len_2(self, string):
        return '0'*(2-len(string)) + string

    def ret_str_len_3(self, string):
        return '0'*(3-len(string)) + string

    def int_to_bin(self, integer):

        if integer == 0:
            return '000'
        if integer == 1:
            return '001'
        if integer == 2:
            return '010'
        if integer == 3:
            return '011'
        if integer == 4:
            return '100'
        if integer == 5:
            return '101'
        if integer == 6:
            return '110'
        if integer == 7:
            return '111'

    def ret_binary(self, character):
        try:
            return bin(ord(character))[2:]
        except Exception as e:
            pass

    def encode(self, message):

        # Divide binary ascii values into 3 parts to be stored in 3 planes
        list_char = [x for x in message]
        print(list_char)
        list_char = [self.ret_str_len_7(bin(ord(x))[2:]) for x in list_char]
        bin_triplets = [(int(x[:3], 2), int(
            x[3:5], 2), int(x[5:], 2)) for x in list_char]

        # Append the tailer to end

        bin_triplets.append(self.tailer)
        for x in bin_triplets:
            print(x)
        # Store the message in image considering row major
        iter = 0
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                '''
                self.image[i, j, 0] ^= bin_triplets[iter][0]
                self.image[i, j, 1] ^= bin_triplets[iter][1]
                self.image[i, j, 2] ^= bin_triplets[iter][2]
                '''

                # Extract binary values of each plane of each pixel
                b, g, r = bin(self.image[i, j, 0])[2:], bin(
                    self.image[i, j, 1])[2:], bin(self.image[i, j, 2])[2:]

                # test

                # Encode the values as LSB in bgr plane

                b = b[:-3] + self.int_to_bin(bin_triplets[iter][0])[-3:]
                g = g[:-2] + self.int_to_bin(bin_triplets[iter][1])[-2:]
                r = r[:-2] + self.int_to_bin(bin_triplets[iter][2])[-2:]

                # Replace the values in original image
                self.image[i, j] = [int(b, 2), int(g, 2), int(r, 2)]

                if(bin_triplets[iter] == (7, 3, 3)):
                    break

                iter += 1

            if(bin_triplets[iter] == (7, 3, 3)):
                break
        print('Out of the loop')
        print('Successfully encoded')
        retval = cv2.imwrite('EncodedImage.png', self.image)
        print('retval: ', retval)
        '''test
        '''
        print('Pixel 1: ', self.image[0, 0])
        print('Pixel 2: ', self.image[0, 1])
        print('Pixel 3: ', self.image[0, 2])

    def decode(self, image_file):
        ascii_list = []

        image = cv2.imread(image_file)
        print('Pixel 1: ', image[0, 0])
        print('Pixel 2: ', image[0, 1])
        print('Pixel 3: ', image[0, 2])
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):

                b, g, r = image[i, j]

                curr_element = (
                    int(self.ret_str_len_3((bin(b)[2:])[-3:]), 2), int(self.ret_str_len_2((bin(g)[2:])[-2:]), 2), int(self.ret_str_len_2((bin(r)[2:])[-2:]), 2))

                if curr_element == (7, 3, 3):
                    break

                ascii_letter = int(self.ret_str_len_3(bin(curr_element[0])[
                    2:]) + self.ret_str_len_2(bin(curr_element[1])[2:]) + self.ret_str_len_2(bin(curr_element[2])[2:]), 2)
                ascii_list.append(ascii_letter)
            if curr_element == (7, 3, 3):
                break
        out_message = ''.join(map(chr, ascii_list))
        print(out_message)


if __name__ == '__main__':
    s = Steg()
    s.encode(input())
    s.decode('EncodedImage.png')
