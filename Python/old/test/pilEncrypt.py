# Import the modules
#from PIL import Image
import random
import cv2
import sys


def pilEncrypt(cars, frame, counter):

        # Load an image from the hard drive
        # img = cv2.imread(image_location)
        img = frame

        # Showing original unencrypted image
        # cv2.imshow('Original', img)
        # k = cv2.waitKey(0)

        # how many license plates (#num of plates, 0, 0)
        # itemset((x, y, [B:0,G:1,R:2]), [new_value])
        num_plates = 0

        for car in cars:
            if car.coords[counter][0] is not -1:
                print(car.coords[counter])
                num_plates += 1

        img.itemset((0, 0, 0), num_plates)

        for n, car in enumerate(cars):
                # coordinates of top left and bottom right points
                x1, y1, width, height = car.coords[counter]
                if x1 is -1:
                    continue

                # used to set Plate meta data, increased by 4 for each plate
                i = 1

                # looping though for each plate in the image
                # license plate string for plate
                lp = car.final_plate
                print(lp)

                # seed from ascii values of lp
                seed = 0
                for p in range(0, len(lp)):
                    seed = seed + ord(lp[p])

                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x1 + width)
                y2 = int(y1 + height)

                random.seed(seed)

                # encrypting image plate
                for x in range(x1, x2):
                    for y in range(y1, y2 ):
                        # getting bgr value of pixel
                        b, g, r = img[y, x]
                        # encrypting image
                        img.itemset((y, x, 0), b ^ random.randint(1, 255))
                        img.itemset((y, x, 1), g ^ random.randint(1, 255))
                        img.itemset((y, x, 2), r ^ random.randint(1, 255))

                # Adding coordinate metadata to the image

                # Sets metadata for x1
                img.itemset((0, i, 0), int(x1 % 100))
                img.itemset((0, i, 1), int(x1/100))

                # Sets metadata for y1
                img.itemset((0, i+1, 0), int(y1 % 100))
                img.itemset((0, i+1, 1), int(y1/100))

                # Sets metadata for x2
                img.itemset((0, i+2, 0), int(x2 % 100))
                img.itemset((0, i+2, 1), int(x2/100))

                # Sets metadata for y2
                img.itemset((0, i+3, 0), int(y2 % 100))
                img.itemset((0, i+3, 1), int(y2/100))

                i += 4

                # Display cords
                print("Plate ", n, "coordinates")
                print("x1", x1)
                print("y1", y1)
                print("x2", x2)
                print("y2", y2, "\n")

        # displaying encrypted image
        # cv2.imshow('Encrypted', img)
        # k = cv2.waitKey(0)

        # saving image
        # cv2.imwrite(image_location, img)
        return img
