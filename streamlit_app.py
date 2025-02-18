import streamlit as st
import requests
import json

# App title & Layout
st.set_page_config(page_title="Firestore UI", layout="wide")

# Initialize session state
if "base_url" not in st.session_state:
    st.session_state.base_url = None
if "db_name" not in st.session_state:
    st.session_state.db_name = None
if "collections" not in st.session_state:
    st.session_state.collections = None
if "selected_collection" not in st.session_state:
    st.session_state.selected_collection = None
if "documents" not in st.session_state:
    st.session_state.documents = None
if "show_raw" not in st.session_state:
    st.session_state.show_raw = False  # Toggle for raw JSON

# Step 1: Enter Firestore-like Base URL & Database Name
st.title("🔥 Firebase Firestore-Like Interface")

if st.session_state.base_url:
    base_url = st.text_input("Base URL:", st.session_state.base_url)
else:
    base_url = st.text_input("Base URL (e.g., http://localhost:5000):")

if st.session_state.db_name:
    db_name = st.text_input("Database Name:", st.session_state.db_name)
else:
    db_name = st.text_input("Database Name (without .db):")

# Store values persistently
if base_url and db_name:
    st.session_state.base_url = base_url
    st.session_state.db_name = db_name

# Fetch collections
if st.button("Fetch Collections"):
    if base_url and db_name:
        url = f"{base_url}/collections?db={db_name}.db"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("collections"):
                    st.session_state.collections = data["collections"]
                else:
                    st.error("No collections found in the database.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter both Base URL and Database Name.")

# Step 2: Display Collections (Firestore Style)
if st.session_state.collections:
    st.subheader("📂 Firestore Collections")
    selected_collection = st.selectbox("Select Collection:", st.session_state.collections)

    if st.button("Load Documents"):
        st.session_state.selected_collection = selected_collection
        doc_url = f"{base_url}/collections/{selected_collection}?db={db_name}.db"
        try:
            doc_response = requests.get(doc_url)
            if doc_response.status_code == 200:
                docs = doc_response.json()
                st.session_state.documents = docs
            else:
                st.error(f"Error fetching documents: {doc_response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# Step 3: Display Documents in Firestore Format
if st.session_state.documents:
    st.subheader(f"📄 Documents in `{st.session_state.selected_collection}`")

    # Toggle raw data view
    st.session_state.show_raw = st.checkbox("Show Raw JSON Data", value=False)

    if st.session_state.show_raw:
        st.json(st.session_state.documents)  # Show raw JSON
    else:
        # Firestore-style document display
        for doc in st.session_state.documents:
            with st.expander(f"🆔 {doc['id']}"):
                st.write("### Document Data:")
                for key, value in doc["data"].items():
                    st.write(f"🔹 **{key}:** `{value}`")  # Firestore style display