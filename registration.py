import streamlit as st
import cv2
import numpy as np
import hashlib
import sqlite3 
import pandas as pd
from PIL import Image

# Function to hash passwords
conn = sqlite3.connect('data.db')
c = conn.cursor()
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Function to check hashed passwords
def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# Function to create user table in the database
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

# Function to add user data to the database
def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username, password))
    conn.commit()

# Function to login user
def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username, password))
    data = c.fetchall()
    return data

# Function to view all users
def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data
def about_us():
    st.write(
        """
        # About BodyVision

        We are a team of four students trying to change the world of shopping for the better. 
        You know the feeling when you order clothes but they don’t fit right? Everyone faces 
        the same issue and we wanted to solve it.

        So, we are doing this as our project. We’re building a software tool that can get 
        accurate measurements. We’re determined to make a difference in this industry, so 
        that it benefits both the consumers and the retailers.

        """
    )
    # Load and display contributor images
    st.title("Meet the Team")
    contributor1_img = Image.open("contributor1.jpg")
    contributor2_img = Image.open("contributor2.jpg")
    contributor3_img = Image.open("contributor3.jpg")
    img_width = contributor1_img.width

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image(contributor1_img, caption="Contributor 1", use_column_width=True)
    with col2:
        st.image(contributor2_img, caption="Contributor 2", use_column_width=True)
    with col3:
        st.image(contributor3_img, caption="Contributor 3", use_column_width=True)
# Function to detect shirt dimensions in an image
def detect_shirt(image):
    # Read the image
    img = cv2.imdecode(image, 1)

    if img is None:
        raise ValueError("Unable to read the image file")

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding to binarize the image
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio
    filtered_contours = []
    min_area = 1000
    min_aspect_ratio = 0.5
    max_aspect_ratio = 2.0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if area > min_area and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
            filtered_contours.append(cnt)

    # Detect largest contour (assuming single shirt)
    if len(filtered_contours) > 0:
        largest_contour = max(filtered_contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        width, height = w, h
    else:
        width, height = None, None

    return width, height

# Function to convert pixels to centimeters
def pixels_to_cm(pixels, reference_length_pixels, reference_length_cm):
    # Calculate conversion factor
    conversion_factor = reference_length_cm / reference_length_pixels
    # Convert pixels to centimeters
    length_cm = pixels * conversion_factor
    return length_cm

# Streamlit UI
def main():
    st.set_page_config(
        page_title="BodyVision - Cloth Size Predictor",
        page_icon=":shirt:",
        layout="wide"
    )

    st.title("Welcome to BodyVision")

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        # st.subheader("Home")
        about_us()
          

    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task", ["Predict Cloth Size"])
                if task == "Add Post":
                    st.subheader("Add Your Post")
                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
                    st.dataframe(clean_db)
                elif task == "Predict Cloth Size":
                    st.subheader("Predict Cloth Size")
                    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
                    if uploaded_image is not None:
                        # Process the uploaded image
                        image = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
                        width, height = detect_shirt(image)
                        if width is not None and height is not None:
                            # Convert pixel measurements to centimeters
                            reference_length_pixels = 100  # Example reference length (in pixels)
                            reference_length_cm = 10  # Example reference length (in centimeters)
                            width_cm = pixels_to_cm(width, reference_length_pixels, reference_length_cm)
                            height_cm = pixels_to_cm(height, reference_length_pixels, reference_length_cm)
                            st.write(f"Predicted Cloth Size:")
                            st.write(f"Width: {width_cm*2:.2f} cm")
                            st.write(f"Height: {height_cm*2:.2f} cm")
                        else:
                            st.write("No shirt detected.")
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

if __name__ == '__main__':
    main()
