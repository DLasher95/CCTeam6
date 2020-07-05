import math
import numpy as np
"""
Author: Dylan Lasher
Specs: Python 3.7, Windows 10
Purpose: Assigning input RGB color to a labeled color using Euclidean distance.
"""

class color_check:
    colors = { # Add colors not associated with emotion, like violet, to avoid too far a reach for an emotional color.
        'red': [255, 0, 0],
        'darkred' : [139,0,0],
        'maroon' : [128,0,0],
        'orangered' : [255,69,0],
        'green' : [0, 255, 0],
        'blue': [0, 0, 255],
        'yellow': [255, 255, 0],
        'cyan': [0, 255, 255],
        #'violet': [255, 0, 255],
        #'orange': [255, 170, 0],
        'black': [0, 0, 0],
        'white': [255, 255, 255],
        'brown': [123, 52, 0],
        #'gray': [127, 127, 127],
        'lightblue': [173, 173, 255],
        'olive' : [128, 128, 0],
        'navy' : [0, 0, 128],
        'darkbrown' : [139,69,19],
        'lightgreen': [173, 255, 173],
    }

    # Input: An array of color names
    # Output: An array of related emotions
    def find_emotions(color):
        emotions = []
        for i in range(len(color)):
            if (color[i] == "red" or color[i] == "darkred" or color[i] == "maroon" or color[i] == "orangered"):
                if "anger" not in emotions:
                    emotions.append("anger")
            elif (color[i] == "black"):
                if "fear" not in emotions:
                    emotions.append("fear")
            elif (color[i] == "lightblue" or color[i] == "cyan" or color[i] == "white" or color[i] == "blue"):
                if "calmness" not in emotions:
                    emotions.append("calmness")
            #elif (color[i] == "olive"):
            #    if "disgust" not in emotions:
            #        emotions.append("disgust")
            #elif (color[i] == "green"):
            #    if "envy" not in emotions:
            #        emotions.append("envy")
            elif (color[i] == "yellow" or color[i] == "cyan" or color[i] == "lightblue" or color[i] == "green" or color[i] == "olive"):
                if "happiness" not in emotions:
                    emotions.append("happiness")
            elif ( color[i] == "navy"):
                if "sadness" not in emotions:
                    emotions.append("sadness")
        return emotions

    # Created nested list to hold colors
    color_list = []
    for key in colors.keys():
        color_list.append(colors[key])

    # Input: list of rgb lists, input rgb list
    def closest(color_list, color_input):
        color_list = np.array(color_list)
        color_input = np.array(color_input)
        distances = np.sqrt(np.sum((color_list - color_input) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))
        smallest_distance = color_list[index_of_smallest]
        return smallest_distance

#"""
# Example Run
"""
# Our colors
input_color_1 = [23, 164, 67]
input_color_2 = [100, 100, 150]
input_color_3 = [250,250,250]
input_colors = [input_color_1, input_color_2, input_color_3]

#Find closest colors
closest_names = []
for i in range(len(input_colors)):
    closest_color_weird_format = color_check.closest(color_check.color_list, input_colors[i])
    closest_color_use = [closest_color_weird_format[0][0], closest_color_weird_format[0][1], closest_color_weird_format[0][2]]
    for keys in color_check.colors:
        #print(color_check.colors.get(keys))
        if color_check.colors.get(keys) == closest_color_use:
            closest_names.append(keys)
for i in closest_names:
    print(i)

found_emotions = color_check.find_emotions(closest_names)
print(found_emotions)
"""
