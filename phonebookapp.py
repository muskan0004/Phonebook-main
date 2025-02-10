import sqlite3
from tabulate import tabulate

# Database connection
conn = sqlite3.connect("phonebook.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE)''')
conn.commit()


def add_contact():
    """ Adds a new contact """
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email (optional): ")

    try:
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        print("Contact added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Phone or Email already exists!")


def view_contacts():
    """ Displays all contacts """
    cursor.execute("SELECT id, name, phone, email FROM contacts")
    contacts = cursor.fetchall()
    if contacts:
        print(tabulate(contacts, headers=["ID", "Name", "Phone", "Email"], tablefmt="grid"))
    else:
        print("No contacts found.")


def search_contact():
    """ Searches for a contact by name or phone """
    keyword = input("Enter Name or Phone to search: ")
    cursor.execute("SELECT id, name, phone, email FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                   (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()

    if results:
        print(tabulate(results, headers=["ID", "Name", "Phone", "Email"], tablefmt="grid"))
    else:
        print("No matching contact found.")


def edit_contact():
    """ Edits an existing contact """
    contact_id = input("Enter Contact ID to edit: ")
    cursor.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))

    if cursor.fetchone():
        new_name = input("Enter New Name (or press enter to keep current): ")
        new_phone = input("Enter New Phone (or press enter to keep current): ")
        new_email = input("Enter New Email (or press enter to keep current): ")

        if new_name:
            cursor.execute("UPDATE contacts SET name=? WHERE id=?", (new_name, contact_id))
        if new_phone:
            cursor.execute("UPDATE contacts SET phone=? WHERE id=?", (new_phone, contact_id))
        if new_email:
            cursor.execute("UPDATE contacts SET email=? WHERE id=?", (new_email, contact_id))

        conn.commit()
        print("Contact updated successfully!")
    else:
        print("Contact not found.")


def delete_contact():
    """ Deletes a contact """
    contact_id = input("Enter Contact ID to delete: ")
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    print("Contact deleted successfully!")


def main():
    """ Main menu loop """
    while True:
        print("\nPhonebook Menu:")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Edit Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            edit_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Exiting Phonebook. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()