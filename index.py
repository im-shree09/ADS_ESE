from pymongo import MongoClient
import tkinter as tk
db_url = 'mongodb://localhost:27017/adsdb'

# create a connection to the database
client = MongoClient(db_url)

# specify the database name
db_name = 'adsdb'

# access the database
db = client[db_name]

# specify the collection name
collection_name = 'test1'

# access the collection
collection = db[collection_name]

import tkinter as tk
from pymongo import MongoClient

class MyGUI:
    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # create a label for the title
        title_label = tk.Label(self.root, text='CRUD Operations', font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # create a frame to hold the input fields and buttons
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # create input fields for the document data
        name_label = tk.Label(input_frame, text='Name:')
        name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        age_label = tk.Label(input_frame, text='Age:')
        age_label.grid(row=1, column=0, padx=5, pady=5)
        self.age_entry = tk.Entry(input_frame)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        city_label = tk.Label(input_frame, text='City:')
        city_label.grid(row=2, column=0, padx=5, pady=5)
        self.city_entry = tk.Entry(input_frame)
        self.city_entry.grid(row=2, column=1, padx=5, pady=5)

        # create buttons for CRUD operations
        create_button = tk.Button(input_frame, text='Create', command=self.create_doc)
        create_button.grid(row=3, column=0, padx=5, pady=5)

        read_button = tk.Button(input_frame, text='Read', command=self.read_doc)
        read_button.grid(row=3, column=1, padx=5, pady=5)

        update_button = tk.Button(input_frame, text='Update', command=self.update_doc)
        update_button.grid(row=3, column=2, padx=5, pady=5)

        delete_button = tk.Button(input_frame, text='Delete', command=self.delete_doc)
        delete_button.grid(row=3, column=3, padx=5, pady=5)

        # create a label to display status messages
        self.status_label = tk.Label(self.root, text='', fg='green')
        self.status_label.pack(pady=10)

    def create_doc(self):
        # get the input data from the entry fields
        name = self.name_entry.get()
        age = self.age_entry.get()
        city = self.city_entry.get()

        # create a new document in the collection
        result = self.db.insert_one({'name': name, 'age': age, 'city': city})

        # display the status message
        if result.acknowledged:
            self.status_label.config(text='Document created successfully')
        else:
            self.status_label.config(text='Failed to create document')
          
            
    def read_doc(self):
        self.status_label.config(text='')
        name = self.name_entry.get()
        print(name)
        if name:
            # query the database for the document
            doc = self.db.find_one({'name': name})
            print(doc)
            # check if the document exists
            if doc:
                # display the document data
                self.age_entry.delete(0, tk.END)
                self.age_entry.insert(0, str(doc.get('age', '')))
                self.city_entry.delete(0, tk.END)
                self.city_entry.insert(0, doc.get('city', ''))

                # update the status label
                self.status_label.config(text='Document found')
            else:
                # clear the input fields
                self.age_entry.delete(0, tk.END)
                self.city_entry.delete(0, tk.END)

                # update the status label
                self.status_label.config(text='Document not found')
        else:
                # update the status label
                self.status_label.config(text='Please enter a name')
                
    def update_doc(self):
        # clear the status label
        self.status_label.config(text='')

        # get the name of the document to update
        name = self.name_entry.get()

        # check if the name is not empty
        if name:
            # get the age and city from the input fields
            age = self.age_entry.get()
            city = self.city_entry.get()

            # check if either age or city is provided
            if age or city:
                # create a dictionary with the update fields
                update_fields = {}
                if age:
                    update_fields['age'] = int(age)
                if city:
                    update_fields['city'] = city

                # update the document in the database
                result = self.db.update_one({'name': name}, {'$set': update_fields})

                # check if the update was successful
                if result.modified_count == 1:
                    # update the status label
                    self.status_label.config(text='Document updated')
                else:
                    # update the status label
                    self.status_label.config(text='Document not updated')
            else:
                # update the status label
                self.status_label.config(text='Please enter at least one field to update')
        else:
            # update the status label
            self.status_label.config(text='Please enter a name')

    
    def delete_doc(self):
        # clear the status label
        self.status_label.config(text='')

        # get the name of the document to delete
        name = self.name_entry.get()

    # check if the name is not empty
        if name:
            # delete the document from the database
            result = self.db.delete_one({'name': name})

            # check if the document was deleted
            if result.deleted_count > 0:
                # clear the input fields
                self.age_entry.delete(0, tk.END)
                self.city_entry.delete(0, tk.END)

                # update the status label
                self.status_label.config(text='Document deleted')
            else:
                # update the status label
                self.status_label.config(text='Document not found')
        else:
            # update the status label
            self.status_label.config(text='Please enter a name')
        
            
gui = MyGUI(collection)