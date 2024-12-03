import streamlit as st
import pandas as pd
import json
import os
import base64
from PIL import Image
import io
import smtplib

st.set_page_config(
    page_title="St. Xavier's High School",
    page_icon="stxaviers_icon.png",  # Replace with your image path
    layout="wide",
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Define folder and data file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
DATA_FOLDER = os.path.join(BASE_DIR, "stxaviers")  # Path to stxaviers folder
DATA_FILE = os.path.join(DATA_FOLDER, "school.json")  # Path to data.json

# Ensure the folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.error("Error reading the data file. Initializing with default data.")
    return {
        'events': [],
        'academic_programs': {
            'Spark': {'description': '', 'logo': ''},
            'Ulipsu': {'description': '', 'logo': ''},
            'e Abhyas Academy': {'description': '', 'logo': ''},
            'Learn Smart': {'description': '', 'logo': ''},
            'Lead': {'description': '', 'logo': ''},
            'Pinnacle': {'description': '', 'logo': ''},
            'SSMPE Sports': {'description': '', 'logo': ''}
        },
        'home_content': '',
        'chairman_photo': '',
        'principal_photo': '',
        'inauguration_photo': '',
        'news': [],
        'school_logo': ''
    }

# Save data
def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file)
    except IOError as e:
        st.error(f"Error saving data: {e}")

# Function to save uploaded images as base64
def save_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            return base64.b64encode(img_byte_arr).decode()
        except Exception as e:
            st.error(f"Error processing the uploaded image: {e}")
            return ""
    return ""
# Add this line to initialize data
data = load_data()  # Ensure `data` is loaded at the start of the script




# Navigation
def navigation():
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", ["Home", "About Us", "Contact Us", "Academic Programs", "Events", "News", "Admin Login"])

# Display school logo
def display_school_logo(data):
    if 'school_logo' in data and data['school_logo']:
        st.image(base64.b64decode(data['school_logo']), width=100)
    else:
        st.write("School logo not available")

#Homepage
def home(data):
    # First column for school logo
    col1, col2 = st.columns([1, 4])
    with col1:
        display_school_logo(data)  # Assuming this function is defined elsewhere to display the logo
    with col2:
        st.title("Welcome to St. Xavier's High School")

    # Display home content
    st.markdown(data.get('home_content', ''))

    # Display latest news
    st.subheader("Latest News")
    for news_item in data.get('news', [])[:3]:  # Display only the latest 3 news items
        st.write(news_item)

    # Display leadership photos (Chairman and Principal)
    st.subheader("Our Leadership")
    col1, col2 = st.columns(2)
    with col1:
        if data.get('chairman_photo'):  # Safer access using .get
            st.image(base64.b64decode(data['chairman_photo']), caption="E. Anthony Reddy sir (Chairman sir)")
        else:
            st.write("Chairman photo not available")
    with col2:
        if data.get('principal_photo'):  # Safer access using .get
            st.image(base64.b64decode(data['principal_photo']), caption="G. Mar Reddy sir (Principal sir)")
        else:
            st.write("Principal photo not available")

    # Display Inauguration photo
    st.subheader("School Inauguration")
    col1, col2, col3 = st.columns(3)  # Creating three columns
    with col1:
        if data.get('inauguration_photo'):  # Safer access using .get
            st.image(base64.b64decode(data['inauguration_photo']), caption="Inauguration Photo")
        else:
            st.write("Inauguration photo not available")

        

# About Us page
def about_us(data):
    col1, col2 = st.columns([1, 4])
    with col1:
        display_school_logo(data)  # Assuming this function displays the school's logo
    with col2:
        st.title("About Us")
    
    # Display the About Us content from the data
    if 'about_us' in data and data['about_us']:
        st.write(data['about_us'])  # Show the updated content
    else:
        # If 'about_us' is empty, show default text
        st.write("St. Xavier's High School is committed to providing quality education and nurturing young minds.")


# Contact Us page
def contact_us(data):
    col1, col2 = st.columns([1, 4])
    with col1:
        display_school_logo(data)  # Assuming this function displays the school's logo
    with col2:
        st.title("Contact Us")

    # Display the Contact Us content dynamically from the data
    if 'contact_us' in data and data['contact_us']:
        st.write(data['contact_us'])  # Show the updated content
        
    else:
        st.write("    ")

        # Contact Form
    st.subheader("💬 Have Questions? Let’s Connect!")
    with st.form("contact_form"):
        name = st.text_input("Your Name", placeholder="Enter your name 🔤")
        email = st.text_input("Your Email", placeholder="Enter your email ✉️")
        message = st.text_area("Your Message", placeholder="Type your message here 📝")
       submitted = st.form_submit_button("Submit")
        if submitted:
    new_message = {
        "name": name,
        "email": email,
        "message": message
    }
    with open("school.json", "a") as file:
        json.dump(new_message, file)
        file.write("\n")  # Add a newline for each message
    st.success("Thank you for reaching out! We’ll get back to you as soon as possible. 🌟")

       else:
        st.error("Please fill out all fields.")                          


# Academic Programs page
def academic_programs(data):
    col1, col2 = st.columns([1, 4])
    with col1:
        display_school_logo(data)
    with col2:
        st.title("Academic Programs")
    for program, details in data['academic_programs'].items():
        st.subheader(program)
        col1, col2 = st.columns([1, 3])
        with col1:
            if details['logo']:
                st.image(base64.b64decode(details['logo']), width=100)
            else:
                st.write("Logo not available")
        with col2:
            st.write(details['description'])

# Events page
def events(data):
    col1, col2 = st.columns([1, 4])
    with col1:
        display_school_logo(data)
    with col2:
        st.title("Events")
    for event in data['events']:
        st.write(f"**{event['name']}** - {event['date']}")
        st.write(event['description'])
        st.write("---")

# News page
def news(data):
    col1, col2 = st.columns([1, 4])
    with col1:
        display_school_logo(data)
    with col2:
        st.title("News")
    for news_item in data['news']:
        st.write(news_item)
        st.write("---")

# Admin login function
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "stxaviers" and password == "xaviers":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# Admin Panel
def admin_panel(data):
    if st.session_state.logged_in:
        st.title("Admin Panel")
        

    def load_contact_messages():
    try:
        with open("school.json", "r") as file:
            # Read all the messages in the file
            messages = file.readlines()

            # Display each message
            for msg in messages:
                message = json.loads(msg)  # Convert each line to a Python dictionary
                st.write(f"### Message from {message['name']}")
                st.write(f"**Email**: {message['email']}")
                st.write(f"**Message**: {message['message']}")
                st.write("---")  # Separator for better readability
    except FileNotFoundError:
        st.error("No messages found. Please submit a message first.")
    except json.JSONDecodeError:
        st.error("Error reading the messages. Please check the JSON file.")
        # Section to view submitted contact messages
    st.subheader("View Contact Messages")
    if st.button("Load Contact Messages"):
        load_contact_messages()  # Call the function to load and display messages

        # Modify About Us Content
        st.subheader("Modify About Us Content")
        about_us_content = st.text_area("About Us Content", data.get('about_us', ''))  # Display current content if exists
        if st.button("Update About Us"):
            if about_us_content:
                data['about_us'] = about_us_content  # Save the updated content
                save_data(data)
                st.success("About Us content updated successfully!")
                st.rerun()

        # Other sections for modifying school logo, events, etc.


        # Modify School Logo
        st.subheader("Modify School Logo")
        school_logo = st.file_uploader("Upload School Logo", type=["png", "jpg", "jpeg"])
        if st.button("Update School Logo"):
            if school_logo:
                logo_base64 = save_uploaded_image(school_logo)
                data['school_logo'] = logo_base64
                save_data(data)
                st.success("School logo updated successfully!")
                st.rerun()

        # Modify Contact Us Content
        st.subheader("Modify Contact Us Content")
        contact_us_content = st.text_area("Contact Us Content", data.get('contact_us', ''))  # Display current content if exists
        if st.button("Update Contact Us"):
            if contact_us_content:
                data['contact_us'] = contact_us_content  # Save the updated content
                save_data(data)
                st.success("Contact Us content updated successfully!")
                st.rerun()

        # Modify Events
        st.subheader("Modify Events")
        event_name = st.text_input("Event Name")
        event_date = st.date_input("Event Date")
        event_description = st.text_area("Event Description")
        if st.button("Add Event"):
            data['events'].append({
                'name': event_name,
                'date': str(event_date),
                'description': event_description
            })
            save_data(data)
            st.success("Event added successfully!")
            st.rerun()

        # Delete Events
        st.subheader("Delete Events")
        event_to_delete = st.selectbox("Select Event to Delete", [f"{event['name']} - {event['date']}" for event in data['events']])
        if st.button("Delete Event"):
            event_name, event_date = event_to_delete.split(' - ')
            data['events'] = [event for event in data['events'] if not (event['name'] == event_name and event['date'] == event_date)]
            save_data(data)
            st.success("Event deleted successfully!")
            st.rerun()

        # Modify Academic Programs
        st.subheader("Modify Academic Programs")
        program = st.selectbox("Select Program", list(data['academic_programs'].keys()))
        program_description = st.text_area("Program Description", data['academic_programs'][program]['description'])
        program_logo = st.file_uploader(f"Upload {program} Logo", type=["png", "jpg", "jpeg"])
        if st.button("Update Program"):
            data['academic_programs'][program]['description'] = program_description
            if program_logo:
                logo_base64 = save_uploaded_image(program_logo)
                data['academic_programs'][program]['logo'] = logo_base64
            save_data(data)
            st.success("Program updated successfully!")
            st.rerun()

        # Modify Home Page Content
        st.subheader("Modify Home Page Content")
        home_content = st.text_area("Home Page Content", data['home_content'])
        if st.button("Update Home Content"):
            data['home_content'] = home_content
            save_data(data)
            st.success("Home content updated successfully!")
            st.rerun()

        # Update Chairman, Principal, and Inauguration Photos
        st.subheader("Update Photos")
        chairman_photo = st.file_uploader("Upload Chairman Photo", type=["png", "jpg", "jpeg"])
        principal_photo = st.file_uploader("Upload Principal Photo", type=["png", "jpg", "jpeg"])
        inauguration_photo = st.file_uploader("Upload Inauguration Photo", type=["png", "jpg", "jpeg"])

        if st.button("Update Photos"):
            updates_made = False

            # Chairman Photo Update
            if chairman_photo:
                chairman_base64 = save_uploaded_image(chairman_photo)
                if chairman_base64:
                    data['chairman_photo'] = chairman_base64
                    updates_made = True

            # Principal Photo Update
            if principal_photo:
                principal_base64 = save_uploaded_image(principal_photo)
                if principal_base64:
                    data['principal_photo'] = principal_base64
                    updates_made = True

            # Inauguration Photo Update
            if inauguration_photo:
                inauguration_base64 = save_uploaded_image(inauguration_photo)
                if inauguration_base64:
                    data['inauguration_photo'] = inauguration_base64
                    updates_made = True

            # Save updated data and show success message
            if updates_made:
                save_data(data)
                st.success("Photos updated successfully!")
                st.rerun()
            else:
                st.warning("No photos were uploaded. Please upload at least one photo to update.")

        # Other existing sections like Modify School Logo, Modify Events, etc
                
        # Modify News Section
        st.subheader("Modify News Section")
        news_item = st.text_input("Add News Item")
        if st.button("Add News"):
            data['news'].insert(0, news_item)  # Add new item at the beginning
            save_data(data)
            st.success("News item added successfully!")
            st.rerun()

        # Delete News Item
        st.subheader("Delete News Item")
        news_to_delete = st.selectbox("Select News Item to Delete", data['news'])
        if st.button("Delete News Item"):
            data['news'].remove(news_to_delete)
            save_data(data)
            st.success("News item deleted successfully!")
            st.rerun()

# You would need to call this admin panel in your main function (e.g., when logged in).
# Main function
def main():
    # Load data
    data = load_data()
    
    # Navigation
    page = navigation()
    
    # Render pages
    if page == "Home":
        home(data)
    elif page == "About Us":
        about_us(data)
    elif page == "Contact Us":
        contact_us(data)
    elif page == "Academic Programs":
        academic_programs(data)
    elif page == "Events":
        events(data)
    elif page == "News":
        news(data)
    elif page == "Admin Login":
        if st.session_state.logged_in:
            admin_panel(data)
        else:
            admin_login()

    # Logout button
    if st.session_state.logged_in:
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
