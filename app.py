import streamlit as st
import sqlite3

# Function to create a SQLite database and table
def create_table():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_user(name, age):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

# Function to retrieve all users
def get_users():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to update user
def update_user(user_id, new_name, new_age):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (new_name, new_age, user_id))
    conn.commit()
    conn.close()

# Function to delete user
def delete_user(user_id):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Main Streamlit app
def main():
    st.title("Streamlit App with SQLite3")
    create_table()

    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create":
        st.subheader("Add New User")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)

        if st.button("Add"):
            if name:
                insert_user(name, age)
                st.success(f"User {name} added successfully!")
            else:
                st.warning("Please enter a name.")

    elif choice == "Read":
        st.subheader("View All Users")
        users = get_users()
        if users:
            for user in users:
                st.write(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")
        else:
            st.write("No users found.")

    elif choice == "Update":
        st.subheader("Update User")
        users = get_users()
        user_ids = [user[0] for user in users]
        user_id = st.selectbox("Select User ID", user_ids)

        if user_id:
            new_name = st.text_input("New Name")
            new_age = st.number_input("New Age", min_value=0, max_value=120, step=1)

            if st.button("Update"):
                if new_name:
                    update_user(user_id, new_name, new_age)
                    st.success("User updated successfully!")
                else:
                    st.warning("Please enter a new name.")

    elif choice == "Delete":
        st.subheader("Delete User")
        users = get_users()
        user_ids = [user[0] for user in users]
        user_id = st.selectbox("Select User ID to Delete", user_ids)

        if st.button("Delete"):
            delete_user(user_id)
            st.success("User deleted successfully!")

if __name__ == "__main__":
    main()
