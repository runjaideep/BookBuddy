import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

from datetime import datetime
import requests

API_URL = "http://localhost:8000"

st.title("Book Buddy")

tab1, tab2, tab3 = st.tabs(["My Library","Add to Library","Recommendations"])

with tab1:
    st.title("Library Dashboard")

    if st.button("Show Library"):
        try:
            response = requests.get(f"{API_URL}/bookbuddy/library/")
            if response.status_code == 200:
                library_data = response.json()
                data = {
                    "Title": [book["title"] for book in library_data],
                    "Author": [book["author"] for book in library_data],
                    "Progress": [book["progress"] for book in library_data],
                }
                df = pd.DataFrame(data).set_index("Title")
                df_sorted = df.sort_values("Title",ascending=True)
                st.subheader("Books Analysis")
                st.table(df_sorted)
            else:
                st.error(f"Something went wrong: {response.status_code}")
        except Exception as e:
            st.error(f"Error occurred: {e}")

with tab2:
    st.title("Add to Library")

    # Dropdown to select what to add
    options = ["Genre", "Author", "Book"]
    choice = st.selectbox("What would you like to add?", options)

    if choice == "Genre":
        genre_name = st.text_input("Enter Genre Name:")
        if st.button("Add Genre"):
            if genre_name.strip():
                try:
                    response = requests.post(f"{API_URL}/bookbuddy/genres/", json={"name": genre_name})
                    if response.status_code == 200:
                        st.success(f"Genre '{genre_name}' added successfully!")
                    else:
                        st.error(f"Failed to add genre: {response.status_code}")
                except Exception as e:
                    st.error(f"Error occurred: {e}")
            else:
                st.error("Genre name cannot be empty!")

    elif choice == "Author":
        author_name = st.text_input("Enter Author Name:")
        if st.button("Add Author"):
            try:
                response = requests.post(f"{API_URL}/bookbuddy/authors/", json={"name": author_name})
                if response.status_code == 201:
                    st.success(f"Author '{author_name}' added successfully!")
                else:
                    st.error(f"Failed to add author: {response.status_code}")
            except Exception as e:
                st.error(f"Error occurred: {e}")

    elif choice == "Book":
        title = st.text_input("Enter Book Title:")
        author_id = st.number_input("Enter Author ID:", min_value=1, step=1)
        genre_id = st.number_input("Enter Genre ID:", min_value=1, step=1)
        total_pages = st.number_input("Enter Total Pages:", min_value=1, step=1)
        rating = st.number_input("Enter Rating (1-5):", min_value=1.0, max_value=5.0, step=0.1)
        if st.button("Add Book"):
            try:
                payload = {
                    "title": title,
                    "author_id": author_id,
                    "genre_id": genre_id,
                    "total_pages": total_pages,
                    "rating": rating,
                }
                response = requests.post(f"{API_URL}/bookbuddy/books/", json=payload)
                if response.status_code == 201:
                    st.success(f"Book '{title}' added successfully!")
                else:
                    st.error(f"Failed to add book: {response.status_code}")
            except Exception as e:
                st.error(f"Error occurred: {e}")

with tab3:
    options = ["Book", "Author"]
    choice = st.selectbox("How would you like to get recommendations", options)
    if choice == "Book":
        title = st.text_input("Enter Book Title:")
        if st.button("Generate"):
            if title.strip():
                try:
                    response = requests.get(f"{API_URL}/bookbuddy/recommendations/", params={"title": title})
                    if response.status_code == 200:
                        recommendations = response.json()
                        recommendations = {
                            "Title": [book["title"] for book in recommendations],
                            "Author": [book["author"] for book in recommendations],
                            "Description": [book["description"] for book in recommendations],
                            "Link": [book["link"] for book in recommendations]
                        }
                        df = pd.DataFrame(recommendations)
                        df_sorted = df.sort_values("Title", ascending=True)
                        st.subheader("Recommendations")
                        gb = GridOptionsBuilder.from_dataframe(df_sorted)
                        gb.configure_column("Description", wrapText=True, autoHeight=True, width=400)  # Adjust width
                        gb.configure_default_column(resizable=True)
                        grid_options = gb.build()
                        #st.table(df_sorted)
                        AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True)
                    else:
                        st.error(f"Something went wrong: {response.status_code}")
                except Exception as e:
                    st.error(f"Error occurred: {e}")
            else:
                st.error("Book title cannot be empty!")
