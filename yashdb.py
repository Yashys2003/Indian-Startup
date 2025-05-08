import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Management")

        # Labels and entries for database connection
        self.label_db_name = tk.Label(root, text="Database Name:")
        self.label_db_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_db_name = tk.Entry(root)
        self.entry_db_name.grid(row=0, column=1, padx=10, pady=5)
        self.entry_db_name.insert(tk.END, "yashdb")  # Default value for database name
        
        self.label_username = tk.Label(root, text="Username:")
        self.label_username.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_username = tk.Entry(root)
        self.entry_username.grid(row=1, column=1, padx=10, pady=5)
        
        self.label_password = tk.Label(root, text="Password:")
        self.label_password.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=5)
        
        self.connect_button = tk.Button(root, text="Connect", command=self.login)
        self.connect_button.grid(row=3, columnspan=2, padx=10, pady=10)

        # Dropdown menu for table selection
        self.table_selection_label = tk.Label(root, text="Select Table:")
        self.table_selection_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.tables = ["STARTUP", "FOUNDERS", "FUNDING", "GROWTH", "NEWS", "AWARDS", "PARTNERS", "CUSTOMERS", "COMPETITORS", "EMPLOYEES"]
        self.selected_table = tk.StringVar(root)
        self.selected_table.set(self.tables[0])  # Default table selection

        self.table_dropdown = tk.OptionMenu(root, self.selected_table, *self.tables)
        self.table_dropdown.grid(row=4, column=1, padx=10, pady=5)

        # Buttons for database operations (initially hidden)
        self.insert_button = tk.Button(root, text="Insert Data", command=self.insert_data, state=tk.DISABLED)
        self.insert_button.grid(row=5, column=0, padx=10, pady=10)
        
        self.display_button = tk.Button(root, text="Display Data", command=self.display_data, state=tk.DISABLED)
        self.display_button.grid(row=5, column=1, padx=10, pady=10)
        
        self.update_button = tk.Button(root, text="Update Data", command=self.update_data, state=tk.DISABLED)
        self.update_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="Delete Data", command=self.delete_data, state=tk.DISABLED)
        self.delete_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Treeview to display table data
        self.treeview = ttk.Treeview(root)
        self.treeview.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        
        # Scrollbars for Treeview
        self.scrollbar_vertical = ttk.Scrollbar(root, orient="vertical", command=self.treeview.yview)
        self.scrollbar_vertical.grid(row=8, column=2, sticky="ns")
        self.treeview.configure(yscrollcommand=self.scrollbar_vertical.set)

        self.scrollbar_horizontal = ttk.Scrollbar(root, orient="horizontal", command=self.treeview.xview)
        self.scrollbar_horizontal.grid(row=9, column=0, columnspan=2, sticky="ew")
        self.treeview.configure(xscrollcommand=self.scrollbar_horizontal.set)

        # Button to display all table details
        self.display_all_button = tk.Button(root, text="Display All Tables", command=self.display_all_table_details, state=tk.DISABLED)
        self.display_all_button.grid(row=10, columnspan=2, padx=10, pady=10)

        # Entry widget and button for custom queries
        self.query_entry = tk.Entry(root)
        self.query_entry.grid(row=11, column=0, padx=10, pady=5, columnspan=2, sticky="ew")

        self.execute_query_button = tk.Button(root, text="Execute Query", command=self.execute_custom_query, state=tk.DISABLED)
        self.execute_query_button.grid(row=12, column=0, padx=10, pady=5, columnspan=2)

    def connect_to_database(self):
        try:
            db_name = self.entry_db_name.get()
            username = self.entry_username.get()
            password = self.entry_password.get()
            
            if username == "yash" and password == "Yash@2003":
                connection = sqlite3.connect(db_name)
                return connection
            else:
                messagebox.showerror("Error", "Invalid username or password!")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to the database: {str(e)}")
            return None

    def login(self):
        connection = self.connect_to_database()
        if connection:
            self.connect_button.config(state=tk.DISABLED)
            self.insert_button.config(state=tk.NORMAL)
            self.display_button.config(state=tk.NORMAL)
            self.update_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.display_all_button.config(state=tk.NORMAL)
            self.execute_query_button.config(state=tk.NORMAL)
            messagebox.showinfo("Success", "Login successful!")

    def insert_data(self):
        table_name = self.selected_table.get()
        column_names = self.get_column_names(table_name)
        data = self.get_insertion_data(column_names)
        if data:
            self.execute_insert_query(table_name, column_names, data)
            messagebox.showinfo("Success", "Data inserted successfully!")

    def get_column_names(self, table_name):
        connection = self.connect_to_database()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            return [col[1] for col in columns]
        return []

    def get_insertion_data(self, column_names):
        data = []
        for col in column_names:
            value = simpledialog.askstring("Insert Data", f"Enter value for {col}:")
            if value is None:
                return None
            data.append(value)
        return data

    def execute_insert_query(self, table_name, column_names, data):
     try:
        connection = self.connect_to_database()
        if connection:
            cursor = connection.cursor()
            columns = ', '.join(column_names)
            placeholders = ', '.join(['?' for _ in range(len(column_names))])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, data)
            connection.commit()
            connection.close()
            self.display_data()  # Update the displayed data after insertion
            messagebox.showinfo("Success", "Data inserted successfully!")
     except Exception as e:
        messagebox.showerror("Error", f"Failed to insert data: {str(e)}")

    def delete_data(self):
        table_name = self.selected_table.get()
        column_names = self.get_column_names(table_name)
        conditions = self.get_deletion_conditions(column_names)
        if conditions:
            self.execute_delete_query(table_name, conditions)
            messagebox.showinfo("Success", "Data deleted successfully!")

    def get_deletion_conditions(self, column_names):
        conditions = []
        for col in column_names:
            value = simpledialog.askstring("Delete Data", f"Enter value for {col} to delete:")
            if value is None:
                return None
            conditions.append((col, value))
        return conditions

    def execute_delete_query(self, table_name, conditions):
        try:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()
                where_clause = ' AND '.join([f"{col} = ?" for col, _ in conditions])
                values = [val for _, val in conditions]
                query = f"DELETE FROM {table_name} WHERE {where_clause}"
                cursor.execute(query, values)
                connection.commit()
                connection.close()
                self.display_data()  # Update the displayed data after deletion
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete data: {str(e)}")

    def display_data(self):
        connection = self.connect_to_database()
        if connection:
            table_name = self.selected_table.get()
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            connection.close()
            self.display_data_in_treeview(data)

    def display_data_in_treeview(self, data):
        # Clear existing treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Insert new data into treeview
        if data:
            # Get column names from cursor description
            cursor = self.connect_to_database().cursor()
            cursor.execute(f"SELECT * FROM {self.selected_table.get()}")
            columns = [desc[0] for desc in cursor.description]
            
            # Configure Treeview columns
            self.treeview["columns"] = columns
            self.treeview.heading("#0", text="Index")
            for col in columns:
                self.treeview.heading(col, text=col)
            
            # Insert data into Treeview
            index = 1
            for row in data:
                self.treeview.insert("", "end", text=index, values=row)
                index += 1

    def display_all_table_details(self):
        connection = self.connect_to_database()
        if connection:
            for table in self.tables:
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                data = cursor.fetchall()
                messagebox.showinfo(f"{table} Details", f"{table}:\n{data}")

    def execute_custom_query(self):
        query = self.query_entry.get()
        if query:
            connection = self.connect_to_database()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute(query)
                    data = cursor.fetchall()
                    connection.close()
                    if data:
                        messagebox.showinfo("Query Result", f"Query executed successfully:\n{data}")
                    else:
                        messagebox.showinfo("Query Result", "Query executed successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to execute query: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter a query to execute.")

    def update_data(self):
        table_name = self.selected_table.get()
        column_names = self.get_column_names(table_name)
        conditions = self.get_update_conditions(column_names)
        if conditions:
            self.execute_update_query(table_name, conditions)
            messagebox.showinfo("Success", "Data updated successfully!")

    def get_update_conditions(self, column_names):
        conditions = {}
        for col in column_names:
            value = simpledialog.askstring("Update Data", f"Enter new value for {col}:")
            if value is None:
                return None
            conditions[col] = value
        return conditions

    def execute_update_query(self, table_name, conditions):
        try:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()
                set_clause = ', '.join([f"{col} = ?" for col in conditions.keys()])
                values = list(conditions.values())
                query = f"UPDATE {table_name} SET {set_clause}"
                cursor.execute(query, values)
                connection.commit()
                connection.close()
                self.display_data()  # Update the displayed data after updating
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update data: {str(e)}")

root = tk.Tk()
app = DatabaseGUI(root)
root.mainloop()
