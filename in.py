import cv2
# from google.colab.patches import cv2_imshow

def measure_object(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Display the image
    cv2_imshow(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Ask the user to draw a rectangle around the object to measure
    print("Click and drag to draw a rectangle around the object to measure.")
    roi = cv2.selectROI("Image", img, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()

    # Extract the coordinates of the rectangle
    x, y, w, h = roi

    # Measure the width and height of the rectangle
    width_pixels = w
    height_pixels = h

    print(f"Width of the object: {width_pixels} pixels")
    print(f"Height of the object: {height_pixels} pixels")

# Prompt the user to input the path of the image
image_path = input("Enter the path of the image: ")

# Call the measure_object function with the user-input image path
measure_object(image_path)
