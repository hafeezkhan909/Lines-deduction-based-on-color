import os
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt  # To show on the screen
from PIL import Image


def PutText(index, pt1):
    cv2.putText(rgb, "line-" + str(index), pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

# Read the image
file = "../sample-1.jpg"
img = cv2.imread(file)
rgb2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.imshow(rgb)
plt.title('Original Image')
plt.show()

# Make it Black & White

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(rgb, 300, 500)

#edges2 = cv2.Canny(gray, 300, 500, apertureSize=3)


plt.imshow(edges)
plt.title('Edge Image')
plt.xticks([]), plt.yticks([])
#cv2.imwrite("gray.png", edges)
plt.show()

lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 20, 30, 5)


"""
lines_list = []
lines2 = cv2.HoughLinesP(
    edges2,  # Input edge image
    1,  # Distance resolution in pixels
    np.pi / 180,  # Angle resolution in radians
    threshold=200,  # Min number of votes for valid line
    minLineLength=10,  # Min allowed length of line
    maxLineGap=5  # Max allowed gap between line for joining them
)
"""
"""
# Iterate over points
for points in lines2:
    # Extracted points nested in the list
    x1, y1, x2, y2 = points[0]
    # Draw the lines joing the points
    # On the original image
    cv2.line(rgb3, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Maintain a simples lookup list for points
    lines_list.append([(x1, y1), (x2, y2)])

plt.title("New All lines")
plt.imshow(rgb3)  # cmap prevents yellow image
#cv2.imwrite("all-lines.png", rgb3)

plt.show()

"""


im = Image.open(file)  # Can be many different formats.
pix = im.load()

colors = [
    ("black", (0, 0, 0)),
    ("silver", (192, 192, 192)),
    ("gray", (128, 128, 128)),
    ("light-gray", (191, 191, 191)),
    ("white", (255, 255, 255)),
    ("maroon", (128, 0, 0)),
    ("red", (255, 0, 0)),
    ("purple", (128, 0, 128)),
    ("fuchsia", (255, 0, 255)),
    ("green", (0, 128, 0)),
    ("lime", (0, 255, 0)),
    ("olive", (128, 128, 0)),
    ("yellow", (255, 255, 0)),
    ("navy", (0, 0, 128)),
    ("blue", (0, 0, 255)),
    ("teal", (0, 128, 128)),
    ("aqua", (0, 255, 255)),
    ("test", (183, 135, 84))
]

def distance(a,b):
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    dz = a[2]-b[2]
    return math.sqrt(dx*dx+dy*dy+dz*dz)
'''
This function is taking two arguments a and b, which are tuples representing the RGB values of two pixels. It calculates the Euclidean distance between the two pixels.
It first calculates the difference in the red, green, and blue values of the two pixels, which are represents by 'dx', 'dy', 'dz'.
Then it calculates the square of the differences and adds them together.
Finally, square root of it is taken.
'''
def findclosest(pixel):
    mn = 999999
    for name, rgb in colors:
        d = distance(pixel, rgb)
        if d < mn:
            mn = d
            color = name
    return color
'''
The findclosest() function is taking one argument 'pixel', which is a tuple representing the RGB values of a pixel. The function finds the closest color to the pixel in the 'colors' list.
It first initializes a variable 'mn' with a large value.
It then loops over the 'colors' list, for each color it calculates the Euclidean distance between the 'pixel' and the color using the distance() function.
If this distance is less than the current minimum distance, it updates the minimum distance and the closest color.
Finally, it returns the name of the closest color.
'''

contours, z = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
width, height = im.size

#drawing all lines
for line in lines:
    pt1 = (line[0][0], line[0][1])
    pt2 = (line[0][2], line[0][3])
    cv2.line(rgb2, pt1, pt2, (0, 0, 255), 2)
    # cv2.putText(rgb2, "line-"+str(index), pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
plt.title("All lines")
plt.imshow(rgb2)  # cmap prevents yellow image
plt.show()

#Labelling all lines or only someof them

def PutText(index, pt1):
        cv2.putText(rgb, "line-" + str(index), pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

# Index of the Lines
index = 0
all_lines = []
colored_lines = []

# Filtering the lines based on color and surrounding pixels
for line in lines:
    pt1 = (line[0][0], line[0][1])
    pt2 = (line[0][2], line[0][3])
    all_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
    '''
    This for loop is iterating over the lines detected in the image, which are stored in the variable lines. For each line, it first extracts the starting and ending point of the line 
    and stores them in the variable pt1 and pt2 respectively. It then adds the line to a list of all lines with the line index, and coordinates of the starting and ending point of the line.
    '''
    if pt1[1] < height/2 or pt2[1] < height/2:
        index = index + 1
        continue
    '''
    The if statement is checking whether either of the y-coordinate of the starting or the ending point is lying in the upper half of the image (by dividing the height by 2). If the line 
    lies in the upper half of the image, it increments the index by 1 and skips that line (moving on to the next iteration in the for loop). Therefore this part of the code is not 
    considering the upper half of the image and not processing them further. 
    '''
    pick_color = "test" #The variable pick_color is being used to specify the color that the code is looking for (In this case it is set to white)
    number_of_pix = 1 #The variable number_of_pix is being used to specify the no. of pixels around staring and ending point of the line that should be checked for the specified color.

    # Original point
    if (findclosest(pix[pt1[0], pt1[1]]) == pick_color or findclosest(pix[pt2[0], pt2[1]]) == pick_color):
        cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
        colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
        PutText(index, pt1)
        '''
        If either the staring or ending point of the line is the specified color, it will draw the line on the image in red color and add the line details to the colored_lines list with the line
        index and call PutText function to add the text the image
        '''

    elif(pt1[0] + number_of_pix < width and pt1[1] + number_of_pix < height) and (pt2[0] + number_of_pix < width and pt2[1] + number_of_pix < height):
        for x in range(1, number_of_pix+1):


            # Upper left
            if (findclosest(pix[pt1[0]-x, pt1[1]-x]) == pick_color or findclosest(pix[pt2[0]-x, pt2[1]-x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break



            # Upper middle
            elif (findclosest(pix[pt1[0]-x, pt1[1]]) == pick_color or findclosest(pix[pt2[0]-x, pt2[1]]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # Upper right
            elif (findclosest(pix[pt1[0]-x, pt1[1]+x]) == pick_color or findclosest(pix[pt2[0]-x, pt2[1]+x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # left
            elif (findclosest(pix[pt1[0], pt1[1]-x]) == pick_color or findclosest(pix[pt2[0], pt2[1]-x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # right
            elif (findclosest(pix[pt1[0], pt1[1] + x]) == pick_color or findclosest(pix[pt2[0], pt2[1] + x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            #Lower right
            elif (findclosest(pix[pt1[0]+x, pt1[1]+x]) == pick_color or findclosest(pix[pt2[0]+x, pt2[1]+x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # lower middle
            elif (findclosest(pix[pt1[0]+x, pt1[1]]) == pick_color or findclosest(pix[pt2[0]+x, pt2[1]]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # Lower left
            elif (findclosest(pix[pt1[0] + x, pt1[1]-x]) == pick_color or findclosest(pix[pt2[0] + x, pt2[1]-x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break

    index = index + 1

    '''
    Once it is determined that the starting or ending point does not consist of the specified color, it consequently enters the nested loop that iterates over the range of 1 to 
    number_of_pix+1. For each iteration, it checks whether any of the 8 neighboring pixels of starting and ending point of the line has the specified color with the help of findclosest()
    function. The 8 pixels as mentioned above are: upper left, upper middle, upper right, left, right, lower left, lower middle, and lower right. Hence, if any of the neighboring pixels has
    the specified color, it draws the line on the image.

    In summary, initially the elif statement in the block of code is checking that the point of the line is not going out of the boundary of the image by adding number of pixels to the point 
    and checking if it is still within the image or not. And then it checks in a grid of 3x3 around the point if it contains the color that is needed or not. If it finds it, it colors the
    line in red and saves the information of the line, otherwise it continues to the next line.
    '''


# Writing the output text file
with open('../all-lines.txt', 'w') as f:
    for line in all_lines:
        f.write("line-" + str(line[0]) + " [" + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "]\n")

with open('../colored-lines.txt', 'w') as f:
    for line in colored_lines:
        f.write("line-" + str(line[0]) + " [" + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "]\n")



plt.title(pick_color+ " Lines" + " " + "("+str(number_of_pix)+") Pixel")
plt.imshow(rgb)
plt.show()
