import streamlit as st

# -------------------------------
# Define Node and Circular Linked List
# -------------------------------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def add_friend(self, name):
        new_node = Node(name)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def remove_friend(self, name):
        if not self.head:
            return
        curr = self.head
        prev = None
        while True:
            if curr.data == name:
                if prev:
                    prev.next = curr.next
                else:
                    temp = self.head
                    while temp.next != self.head:
                        temp = temp.next
                    temp.next = self.head.next
                    self.head = self.head.next
                break
            prev = curr
            curr = curr.next
            if curr == self.head:
                break

    def get_friends(self):
        friends = []
        if not self.head:
            return friends
        temp = self.head
        while True:
            friends.append(temp.data)
            temp = temp.next
            if temp == self.head:
                break
        return friends


# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Social Media Friend List", layout="centered")
st.title("👥 Social Media Friend List")

# Session state for users
if "users" not in st.session_state:
    st.session_state.users = {}

# Add a new user
st.subheader("➕ Add New User")
new_user = st.text_input("Enter new user name:")
if st.button("Add User"):
    if new_user:
        if new_user in st.session_state.users:
            st.warning("User already exists!")
        else:
            st.session_state.users[new_user] = CircularLinkedList()
            st.success(f"User '{new_user}' added successfully!")
    else:
        st.warning("Please enter a valid name!")

# Display existing users
if st.session_state.users:
    st.subheader("👤 Manage Friends")
    selected_user = st.selectbox("Select a user:", list(st.session_state.users.keys()))

    friend_action = st.radio("Choose action:", ["Add Friend", "Remove Friend"], horizontal=True)
    friend_name = st.text_input("Enter friend's name:")

    if st.button("Submit Action"):
        user_list = st.session_state.users[selected_user]
        if friend_action == "Add Friend":
            user_list.add_friend(friend_name)
            st.success(f"Friend '{friend_name}' added to {selected_user}'s list!")
        elif friend_action == "Remove Friend":
            user_list.remove_friend(friend_name)
            st.info(f"Friend '{friend_name}' removed from {selected_user}'s list!")

    st.write(f"📋 {selected_user}'s Friends:")
    st.write(st.session_state.users[selected_user].get_friends())

# -------------------------------
# Mutual Connections
# -------------------------------
st.subheader("🔍 Find Mutual Connections Between Two Users")

if len(st.session_state.users) < 2:
    st.info("Add at least 2 users to find mutual connections.")
else:
    col1, col2 = st.columns(2)
    with col1:
        user1 = st.selectbox("Select User 1:", list(st.session_state.users.keys()), key="u1")
    with col2:
        user2 = st.selectbox("Select User 2:", list(st.session_state.users.keys()), key="u2")

    if user1 == user2:
        st.warning("Please select two different users!")
    else:
        if st.button("Find Mutual Connections"):
            friends1 = set(st.session_state.users[user1].get_friends())
            friends2 = set(st.session_state.users[user2].get_friends())
            mutual = friends1.intersection(friends2)

            st.write(f"Mutual Connections between {user1} and {user2}:")
            if mutual:
                st.success(list(mutual))
            else:
                st.info("No mutual connections found.")
