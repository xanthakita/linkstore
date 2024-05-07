import streamlit as st
import pandas as pd
import qrcode 
import loguru
from pymongo import MongoClient
from PIL import Image
from io import BytesIO
from datetime import datetime

# setup logfile
date_obj = datetime(2023, 3, 8)
thedate = date_obj.strftime("%m%d%Y")
LOGFILE = f"/opt/logs/linkstore_{thedate}.log"
logger = loguru.logger
logger.add(LOGFILE, serialize=True)

# Function to connect to MongoDB and return the collection
def connect_to_mongodb():
    try:
        # Connect to MongoDB running on localhost
        client = MongoClient('mongodb://localhost:27017/')
        db = client['linkstore']  # Connect to 'linkstore' database
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Function to get collection names from MongoDB
def get_collection_names():
    db = connect_to_mongodb()
    return db.list_collection_names()

# Function to parse Adobe PDF date format to standard datetime string
def parse_adobe_pdf_date(adobe_date):
    if adobe_date.startswith("D:") and len(adobe_date) >= 16:
        adobe_date = adobe_date[2:]  # Remove the 'D:' prefix
        try:
            parsed_date = datetime.strptime(adobe_date[:14], "%Y%m%d%H%M%S")  # Parse the date and time
            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")  # Convert to standard datetime string
        except ValueError:
            logger.error("Date could not be parsed")
            return None
    else:
        return None

# Function to display data
def display_data(df):
    for index, row in df.iterrows():
        # Create a two-column layout
        col1, col2 = st.columns([1, 3])

        # Display QR code in the first column
        with col1:
            # Generate QR code for the URL
            st.write("Open PDF")
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(row['link'])
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((150, 150))
            qr_image = Image.new("RGB", (150, 150), "white")
            qr_image.paste(img)
            st.image(qr_image, use_column_width=False)

        # Display text information in the second column
        with col2:
            st.header(f"{row['title']}")
            st.write(f"**Category:** {row['category']}")
            if 'summary' in row:
                st.write(f"Summary: [{row['summary']}] ")
            else:
                st.write("Summary: N/A")
            published_time = parse_adobe_pdf_date(row['metatags'].get('creationdate', ""))
            st.write(f"**Published Time:** {published_time}")
            st.write(f"**Link:** [{row['displayLink']}]({row['link']})")
            st.write(f"**Snippet:** {row['snippet']}")
            st.write(f"**ID:** {row['id']}")

        # Add a horizontal rule between entries
        st.markdown("---")


# Main function
def main():
    # Set title
    st.title("Linkstore")
    st.subheader("Global Emancipation network")
    """ 
    This is a resource library intended to provide resorces for people trying to learn more about 
    human trafficking in all of its forms and child protection. 
    The goal is to also provide local resource information so that users can find local 
    help and support if you have seen or expereienced human trafficking or child endangerment!
    """

    # Sidebar for selecting collections
    selected_collections = st.sidebar.multiselect("Select collections", get_collection_names())

    if not selected_collections:
        # Display document counts for each collection in the main area
        st.header("Document Counts")
        db = connect_to_mongodb()
        if db is not None:
            collection_counts = {name: db[name].estimated_document_count() for name in get_collection_names()}
            for name, count in collection_counts.items():
                st.write(f"- {name}: {count}")
        else:
            st.error("Failed to connect to MongoDB. Please check your connection settings.")
            logger.error("Failed to connect to MongoDB. Please check your connection settings.")
    else:
        # Display document data for the selected collections
        for collection_name in selected_collections:
            logger.info(f"selected:{collection_name}")
            st.header(f"Documents in Collection: {collection_name}")
            collection = connect_to_mongodb()[collection_name]
            cursor = collection.find()
            df = pd.DataFrame(list(cursor))
            display_data(df)

if __name__ == "__main__":
    main()
