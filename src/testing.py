import os
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt  # To show on the screen
from PIL import Image


def PutText(index, pt1):
    cv2.putText(rgb, "line-" + str(index), pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

# Read the image
file = "/home/hafeez/Desktop/cropped_images"

# Define the path to the directory where the cropped images will be saved
output_a = "/home/hafeez/Desktop/edge_images"
output_b = "/home/hafeez/Desktop/all_lines_images"
output_c = "/home/hafeez/Desktop/final_images"
# Create the output directory if it doesn't already exist
if not os.path.exists(output_a):
    os.makedirs(output_a)

if not os.path.exists(output_b):
    os.makedirs(output_b)

if not os.path.exists(output_c):
    os.makedirs(output_c)

for file_name in os.listdir(file):
        x = os.path.join(file, file_name)
        img = cv2.imread(x)
        rgb2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #plt.imshow(rgb)
        #plt.title('Original Image')
        #plt.show()
        #cv2.imwrite(os.path.join(output_a, file_name), img)
        # Make it Black & White

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(rgb, 300, 500)
        cv2.imwrite(os.path.join(output_a, file_name), edges)
        #edges2 = cv2.Canny(gray, 300, 500, apertureSize=3)


        #plt.imshow(edges)
        #plt.title('Edge Image')
        #plt.xticks([]), plt.yticks([])
        #cv2.imwrite("gray.png", edges)
        #plt.show()
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 20, 30, 5)

        im = Image.open(x)
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

        def findclosest(pixel):
            mn = 999999
            for name, rgb in colors:
                d = distance(pixel, rgb)
                if d < mn:
                    mn = d
                    color = name
            return color


        contours, z = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        width, height = im.size

        #drawing all lines
        for line in lines:
            pt1 = (line[0][0], line[0][1])
            pt2 = (line[0][2], line[0][3])
            cv2.line(rgb2, pt1, pt2, (0, 0, 255), 2)
            # cv2.putText(rgb2, "line-"+str(index), pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        #plt.title("All lines")
        #plt.imshow(rgb2)  # cmap prevents yellow image
        #plt.show()
        cv2.imwrite(os.path.join(output_b, file_name), rgb2)

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

            if pt1[1] < height/2 or pt2[1] < height/2:
                index = index + 1
                continue

            pick_color = "test" #The variable pick_color is being used to specify the color that the code is looking for (In this case it is set to white)
            number_of_pix = 1 #The variable number_of_pix is being used to specify the no. of pixels around staring and ending point of the line that should be checked for the specified color.

    # Original point
            if (findclosest(pix[pt1[0], pt1[1]]) == pick_color or findclosest(pix[pt2[0], pt2[1]]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)

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


        # Writing the output text file
        save_lines = "/home/hafeez/Desktop/all_lines"
        save_colors = "/home/hafeez/Desktop/colored_lines"
        fold = file_name[:-4] + 'all-lines.txt'
        if not os.path.exists(save_lines):
            os.makedirs(save_lines)

        cold = file_name[:-4] + 'colored-lines.txt'
        if not os.path.exists(save_colors):
            os.makedirs(save_colors)

        a = os.path.join(save_lines, fold)
        with open(a, 'w') as f:
            for line in all_lines:
                f.write("line-" + str(line[0]) + " [" + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "]\n")

        b = os.path.join(save_colors, cold)
        with open(b, 'w') as f:
            for line in colored_lines:
                f.write("line-" + str(line[0]) + " [" + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "]\n")



        #plt.title(pick_color+ " Lines" + " " + "("+str(number_of_pix)+") Pixel")
        #plt.imshow(rgb)
        #plt.show()
        cv2.imwrite(os.path.join(output_c, file_name), rgb)