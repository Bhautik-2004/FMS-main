import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


expense_data = pd.read_csv('MOCK_DATA.csv')
income_data = pd.read_csv('income.csv')


# Validation to input only Numbers
def validate_numeric_input(current_value):
    if current_value == "" or current_value == ".":
        return True
    try:
        float(current_value)
        return True
    except ValueError:
        return False


# Function to add new data
def add_expense():
    global expense_data
    new_window = Toplevel(window)
    new_window.title("Add Expense")
    new_window.geometry("300x250")
    new_window.resizable(False, False)

    if not expense_data.empty:
        last_id = int(expense_data['expense_id'].tail(1).values[0])
        default_id = IntVar(new_window, value=last_id + 1)
    else:
        default_id = 1

    Label(new_window, text='Expense ID: ').grid(row=0, column=0, padx=10, pady=5)
    expense_id_input = Entry(new_window, textvariable=default_id, state='disabled')
    expense_id_input.grid(row=0, column=1, padx=10, pady=5)

    Label(new_window, text='Date: ').grid(row=1, column=0, padx=10, pady=5)
    date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                           date_pattern='yyyy/MM/dd')
    date_input.grid(row=1, column=1, padx=10, pady=5)

    category_values = ['Groceries', 'Utilities', 'Transportation', 'Entertainment', 'Clothing', 'Medical',
                       'Living Expenses', 'Dine Out', 'Charity']
    category_var = StringVar(value='Select')
    Label(new_window, text='Category: ').grid(row=2, column=0, padx=10, pady=5)
    category_input = OptionMenu(new_window, category_var, *category_values)
    category_input.grid(row=2, column=1, padx=10, pady=5)

    vcmd = (new_window.register(validate_numeric_input), '%P')
    Label(new_window, text='Amount: ').grid(row=3, column=0, padx=10, pady=5)
    amount_input = Entry(new_window, validate="key", validatecommand=vcmd)
    amount_input.grid(row=3, column=1, padx=10, pady=5)

    payment_values = ['Debit Card', 'Credit Card', 'Mobile Payment', 'Cash']
    payment_var = StringVar(value='Select')
    Label(new_window, text='Payment Method: ').grid(row=4, column=0, padx=10, pady=5)
    payment_method_input = OptionMenu(new_window, payment_var, *payment_values)
    payment_method_input.grid(row=4, column=1, padx=10, pady=5)

    def submit_data():
        if (not expense_id_input.get() or
                category_var.get() == 'Select' or
                not amount_input.get() or
                payment_var.get() == 'Select'):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            new_expense = pd.DataFrame({
                "expense_id": [expense_id_input.get()],
                "date": [date_input.get_date()],
                "amount": [float(amount_input.get()) if amount_input.get().replace('.', '', 1).isdigit() else 0.0],
                "category": [category_var.get()],
                "payment_method": [payment_var.get()],
            })

            global expense_data
            expense_data = pd.concat([expense_data, new_expense], ignore_index=True)
            expense_data.to_csv('MOCK_DATA.csv', index=False)
            expense_data = pd.read_csv('MOCK_DATA.csv')

            messagebox.showinfo("Success", "Data added successfully!")

            new_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

    Button(new_window, text="Submit", command=submit_data).grid(row=5, columnspan=2, pady=10)


def view_expense():
    new_window = Toplevel(window)
    new_window.title('View Expenses')
    new_window.geometry('550x380')
    new_window.resizable(False, False)

    Label(new_window, text='Start Date: ').grid(row=0, column=0, padx=10, pady=5)
    start_date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                                 date_pattern='yyyy/MM/dd')
    start_date_input.grid(row=0, column=1, padx=10, pady=5)

    Label(new_window, text='End Date: ').grid(row=0, column=2, padx=10, pady=5)
    end_date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                               date_pattern='yyyy/MM/dd')
    end_date_input.grid(row=0, column=3, padx=10, pady=5)

    category_values = ['Groceries', 'Utilities', 'Transportation', 'Entertainment', 'Clothing', 'Medical',
                       'Living Expenses', 'Dine Out', 'Charity']
    category_var = StringVar(value='All')
    Label(new_window, text='Category: ').grid(row=1, column=0, padx=10, pady=5)
    category_input = OptionMenu(new_window, category_var, *category_values)
    category_input.grid(row=1, column=1, padx=10, pady=5)

    # Frame for Treeview and Scrollbars
    view_expense_frame = Frame(new_window)
    view_expense_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # Scrollbars
    view_expense_y_scroll = Scrollbar(view_expense_frame, orient='vertical')
    view_expense_y_scroll.grid(row=0, column=1, sticky='ns')

    view_expense_x_scroll = Scrollbar(view_expense_frame, orient='horizontal')
    view_expense_x_scroll.grid(row=2, column=0, sticky='ew')

    # Treeview to display expenses
    view_expense_table = ttk.Treeview(view_expense_frame, yscrollcommand=view_expense_y_scroll.set,
                                      xscrollcommand=view_expense_x_scroll.set)
    view_expense_table.grid(row=0, column=0)

    # Configure Scrollbars
    view_expense_y_scroll.config(command=view_expense_table.yview)
    view_expense_x_scroll.config(command=view_expense_table.xview)

    view_expense_table['columns'] = ('expense_id', 'date', 'amount', 'category', 'payment_method')
    # format our column
    view_expense_table.column("#0", width=0, stretch=NO)
    view_expense_table.column("expense_id", anchor=CENTER, width=80)
    view_expense_table.column("date", anchor=CENTER, width=80)
    view_expense_table.column("amount", anchor=CENTER, width=80)
    view_expense_table.column("category", anchor=CENTER, width=90)
    view_expense_table.column("payment_method", anchor=CENTER, width=150)

    # Create Headings
    view_expense_table.heading("#0", text="", anchor=CENTER)
    view_expense_table.heading("expense_id", text="ID", anchor=CENTER)
    view_expense_table.heading("date", text="Date", anchor=CENTER)
    view_expense_table.heading("amount", text="Amount", anchor=CENTER)
    view_expense_table.heading("category", text="Category", anchor=CENTER)
    view_expense_table.heading("payment_method", text="Mode of Payment", anchor=CENTER)

    no_data_label = Label(new_window, text='No Data Available', fg='red')
    no_data_label.grid_forget()  # Hidden initially

    def submit():
        start_date = start_date_input.get_date()
        end_date = end_date_input.get_date()

        selected_category = category_var.get()

        expense_data['date'] = pd.to_datetime(expense_data['date'])

        filtered_data = expense_data[(expense_data['date'] >= pd.to_datetime(start_date)) &
                                     (expense_data['date'] <= pd.to_datetime(end_date))]

        if selected_category != 'All':
            filtered_data = filtered_data[filtered_data['category'] == selected_category]

        # Clear the Treeview
        for row in view_expense_table.get_children():
            view_expense_table.delete(row)

        # Insert filtered data into the Treeview
        if filtered_data.empty:
            no_data_label.grid(row=3, column=0, columnspan=4)
        else:
            no_data_label.grid_forget()
            for _, row in filtered_data.iterrows():
                view_expense_table.insert('', 'end', values=(int(row['expense_id']),
                                                             row['date'].strftime('%Y-%m-%d'), row['amount'],
                                                             row['category'], row['payment_method']))

    Button(new_window, text="Submit", command=submit).grid(row=1, column=3, columnspan=2, pady=10)


def edit_and_delete_expense():
    new_window = Toplevel(window)
    new_window.title('Edit/Delete Expenses')
    new_window.geometry('550x410')
    new_window.resizable(False, False)

    Label(new_window, text='Start Date: ').grid(row=0, column=0, padx=10, pady=5)
    start_date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                                 date_pattern='yyyy/MM/dd')
    start_date_input.grid(row=0, column=1, padx=10, pady=5)

    Label(new_window, text='End Date: ').grid(row=0, column=2, padx=10, pady=5)
    end_date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                               date_pattern='yyyy/MM/dd')
    end_date_input.grid(row=0, column=3, padx=10, pady=5)

    category_values = ['Groceries', 'Utilities', 'Transportation', 'Entertainment', 'Clothing', 'Medical',
                       'Living Expenses', 'Dine Out', 'Charity']
    category_var = StringVar(value='All')
    Label(new_window, text='Category: ').grid(row=1, column=0, padx=10, pady=5)
    category_input = OptionMenu(new_window, category_var, *category_values)
    category_input.grid(row=1, column=1, padx=10, pady=5)

    # Frame for Treeview and Scrollbars
    view_expense_frame = Frame(new_window)
    view_expense_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # Scrollbars
    view_expense_y_scroll = Scrollbar(view_expense_frame, orient='vertical')
    view_expense_y_scroll.grid(row=0, column=1, sticky='ns')

    view_expense_x_scroll = Scrollbar(view_expense_frame, orient='horizontal')
    view_expense_x_scroll.grid(row=2, column=0, sticky='ew')

    # Treeview to display expenses
    view_expense_table = ttk.Treeview(view_expense_frame, yscrollcommand=view_expense_y_scroll.set,
                                      xscrollcommand=view_expense_x_scroll.set)
    view_expense_table.grid(row=0, column=0)

    # Configure Scrollbars
    view_expense_y_scroll.config(command=view_expense_table.yview)
    view_expense_x_scroll.config(command=view_expense_table.xview)

    view_expense_table['columns'] = ('expense_id', 'date', 'amount', 'category', 'payment_method')
    # format our column
    view_expense_table.column("#0", width=0, stretch=NO)
    view_expense_table.column("expense_id", anchor=CENTER, width=80)
    view_expense_table.column("date", anchor=CENTER, width=80)
    view_expense_table.column("amount", anchor=CENTER, width=80)
    view_expense_table.column("category", anchor=CENTER, width=90)
    view_expense_table.column("payment_method", anchor=CENTER, width=150)

    # Create Headings
    view_expense_table.heading("#0", text="", anchor=CENTER)
    view_expense_table.heading("expense_id", text="ID", anchor=CENTER)
    view_expense_table.heading("date", text="Date", anchor=CENTER)
    view_expense_table.heading("amount", text="Amount", anchor=CENTER)
    view_expense_table.heading("category", text="Category", anchor=CENTER)
    view_expense_table.heading("payment_method", text="Mode of Payment", anchor=CENTER)

    no_data_label = Label(new_window, text='No Data Available', fg='red')
    no_data_label.grid_forget()  # Hidden initially

    def submit():
        global expense_data
        start_date = start_date_input.get_date()
        end_date = end_date_input.get_date()

        selected_category = category_var.get()

        expense_data['date'] = pd.to_datetime(expense_data['date'])

        filtered_data = expense_data[(expense_data['date'] >= pd.to_datetime(start_date)) &
                                     (expense_data['date'] <= pd.to_datetime(end_date))]

        if selected_category != 'All':
            filtered_data = filtered_data[filtered_data['category'] == selected_category]

        # Clear the Treeview
        for row in view_expense_table.get_children():
            view_expense_table.delete(row)

        # Insert filtered data into the Treeview
        if filtered_data.empty:
            no_data_label.grid(row=3, column=0, columnspan=4)
        else:
            no_data_label.grid_forget()
            for _, row in filtered_data.iterrows():
                view_expense_table.insert('', 'end', values=(int(row['expense_id']),
                                                             row['date'].strftime('%Y-%m-%d'), row['amount'],
                                                             row['category'], row['payment_method']))

    def edit_selected():
        global expense_data
        selected_item = view_expense_table.selection()  # Get selected row

        if selected_item:
            item_values = view_expense_table.item(selected_item, 'values')

            # Extract the first value (expense_id) from the tuple
            expense_id = int(item_values[0])
            edit_window = Toplevel(window)
            edit_window.title(f'Edit Expense #{expense_id}')
            edit_window.geometry('300x250')
            edit_window.resizable(False, False)

            Label(edit_window, text=f'Expense ID: {expense_id}').grid(row=0, column=0, padx=10, pady=10, sticky='w')

            # Retrieve current values
            current_date = expense_data.loc[expense_data['expense_id'] == expense_id, 'date'].values[0]
            current_amount = expense_data.loc[expense_data['expense_id'] == expense_id, 'amount'].values[0]
            current_category = expense_data.loc[expense_data['expense_id'] == expense_id, 'category'].values[0]
            current_payment_method = expense_data.loc[expense_data['expense_id'] == expense_id, 'payment_method'].values[0]

            Label(edit_window, text='Date: ').grid(row=1, column=0, padx=10, pady=5, sticky='w')
            date_input = DateEntry(edit_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                                   date_pattern='yyyy/MM/dd')  # Correct date format
            date_input.set_date(pd.to_datetime(current_date, dayfirst=True).date())  # Ensure day-first parsing
            date_input.grid(row=1, column=1, padx=10, pady=5)

            vcmd = (new_window.register(validate_numeric_input), '%P')
            Label(edit_window, text='Amount: ').grid(row=2, column=0, padx=10, pady=5, sticky='w')
            amount_input = Entry(edit_window, validate='key', validatecommand=vcmd)
            amount_input.insert(0, current_amount)
            amount_input.grid(row=2, column=1, padx=10, pady=5)

            Label(edit_window, text='Category: ').grid(row=3, column=0, padx=10, pady=5, sticky='w')
            category_values = ['Groceries', 'Utilities', 'Transportation', 'Entertainment', 'Clothing', 'Medical',
                               'Living Expenses', 'Dine Out', 'Charity']
            category_var = StringVar(value=current_category)
            category_input = OptionMenu(edit_window, category_var, *category_values)
            category_input.grid(row=3, column=1, padx=10, pady=5)

            Label(edit_window, text='Payment Method: ').grid(row=4, column=0, padx=10, pady=5, sticky='w')
            payment_method_values = ['Debit Card', 'Credit Card', 'Mobile Payment', 'Cash']
            payment_method_var = StringVar(value=current_payment_method)
            payment_method_input = OptionMenu(edit_window, payment_method_var, *payment_method_values)
            payment_method_input.grid(row=4, column=1, padx=10, pady=5)

            def update_expense():
                global expense_data
                # Ensure correct format and day-first approach
                new_date = date_input.get_date().strftime('%Y-%m-%d')  # Format date as day-month-year
                new_amount = float(amount_input.get())  # Convert to float if necessary
                new_category = category_var.get()
                new_payment_method = payment_method_var.get()

                # Update DataFrame
                expense_data.loc[expense_data['expense_id'] == expense_id, 'date'] = new_date
                expense_data.loc[expense_data['expense_id'] == expense_id, 'amount'] = new_amount
                expense_data.loc[expense_data['expense_id'] == expense_id, 'category'] = new_category
                expense_data.loc[expense_data['expense_id'] == expense_id, 'payment_method'] = new_payment_method

                # Update the displayed values in the Treeview
                view_expense_table.item(selected_item,
                                        values=(expense_id, new_date, new_amount, new_category, new_payment_method))

                # Save the updated data to CSV
                expense_data.to_csv('MOCK_DATA.csv', index=False)
                expense_data = pd.read_csv('MOCK_DATA.csv', dayfirst=True)  # Ensure day-first when reloading

                # Close edit window and show success message
                edit_window.destroy()
                messagebox.showinfo("Success", f"Expense #{expense_id} updated successfully!")

            Button(edit_window, text="Update", command=update_expense).grid(row=5, column=0, columnspan=2, pady=10)

        else:
            messagebox.showerror("Error", "No entry selected to edit.")

    def delete_selected():
        global expense_data

        selected_item = view_expense_table.selection()

        if selected_item:
            item_values = view_expense_table.item(selected_item, 'values')

            expense_id = int(item_values[0])

            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
            if confirm:
                view_expense_table.delete(selected_item)

                expense_data = expense_data[expense_data['expense_id'] != expense_id]

                expense_data.to_csv('MOCK_DATA.csv', index=False)
            else:
                messagebox.showerror("Error", "No entry selected to delete.")
        else:
            messagebox.showerror("Error", "No entry selected to delete.")

    Button(new_window, text="Submit", command=submit).grid(row=1, column=3, columnspan=2, pady=10)
    Button(new_window, text="Edit Selected", command=edit_selected).grid(row=4, column=0, columnspan=3, pady=5)
    Button(new_window, text="Delete Selected", command=delete_selected).grid(row=4, column=1, columnspan=4, pady=5)


def add_income():
    global income_data
    new_window = Toplevel()
    new_window.title("Add Income")
    new_window.geometry('300x250')
    new_window.resizable(False, False)

    if not expense_data.empty:
        last_id = int(income_data['income_id'].tail(1).values[0])
        default_id = IntVar(new_window, value=last_id + 1)
    else:
        default_id = 1

    Label(new_window, text='Income ID: ').grid(row=0, column=0, padx=10, pady=5)
    income_id_input = Entry(new_window, textvariable=default_id, state="disabled")
    income_id_input.grid(row=0, column=1, padx=10, pady=5)

    Label(new_window, text='Date: ').grid(row=1, column=0, padx=10, pady=5)
    date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                           date_pattern='yyyy/MM/dd')
    date_input.grid(row=1, column=1, padx=10, pady=5)

    vcmd = (new_window.register(validate_numeric_input), '%P')
    Label(new_window, text='Amount: ').grid(row=2, column=0, padx=10, pady=5)
    amount_input = Entry(new_window, validate='key', validatecommand=vcmd)
    amount_input.grid(row=2, column=1, padx=10, pady=5)

    category_values = ['Primary', 'Secondary', 'Passive']
    category_var = StringVar(value='Select')
    Label(new_window, text='Category: ').grid(row=3, column=0, padx=10, pady=5)
    category_input = OptionMenu(new_window, category_var, *category_values)
    category_input.grid(row=3, column=1, padx=10, pady=5)

    payment_method_values = ['Bank Transfer', 'Online']
    payment_method_var = StringVar(value='Select')
    Label(new_window, text='Payment Method: ').grid(row=4, column=0, padx=10, pady=5)
    payment_method_input = OptionMenu(new_window, payment_method_var, *payment_method_values)
    payment_method_input.grid(row=4, column=1, padx=10, pady=5)

    def submit():
        if (not income_id_input.get() or
                category_var.get() == 'Select' or
                not amount_input.get() or
                payment_method_var.get() == 'Select'):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            new_income = pd.DataFrame({
                "income_id": [income_id_input.get()],
                "date": [date_input.get_date()],
                "amount": [float(amount_input.get()) if amount_input.get().replace('.', '', 1).isdigit() else 0.0],
                "category": [category_var.get()],
                "payment_method": [payment_method_var.get()],
            })

            global income_data
            income_data = pd.concat([income_data, new_income], ignore_index=True)
            income_data.to_csv('income.csv', index=False)
            income_data = pd.read_csv('income.csv')

            messagebox.showinfo("Success", "Data added successfully!")

            new_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

    Button(new_window, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=10)


def view_income():
    new_window = Toplevel(window)
    new_window.title('View Income')
    new_window.geometry('550x380')
    new_window.resizable(False, False)

    Label(new_window, text='Start Date: ').grid(row=0, column=0, padx=10, pady=5)
    start_date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                                 date_pattern='yyyy/MM/dd')
    start_date_input.grid(row=0, column=1, padx=10, pady=5)

    Label(new_window, text='End Date: ').grid(row=0, column=2, padx=10, pady=5)
    end_date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                               date_pattern='yyyy/MM/dd')
    end_date_input.grid(row=0, column=3, padx=10, pady=5)

    category_values = ['Primary', 'Secondary', 'Passive']
    category_var = StringVar(value='All')
    Label(new_window, text='Category: ').grid(row=1, column=0, padx=10, pady=5)
    category_input = OptionMenu(new_window, category_var, *category_values)
    category_input.grid(row=1, column=1, padx=10, pady=5)

    # Frame for Treeview and Scrollbars
    view_income_frame = Frame(new_window)
    view_income_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # Scrollbars
    view_income_y_scroll = Scrollbar(view_income_frame, orient='vertical')
    view_income_y_scroll.grid(row=0, column=1, sticky='ns')

    view_income_x_scroll = Scrollbar(view_income_frame, orient='horizontal')
    view_income_x_scroll.grid(row=2, column=0, sticky='ew')

    # Treeview to display income
    view_income_table = ttk.Treeview(view_income_frame, yscrollcommand=view_income_y_scroll.set,
                                     xscrollcommand=view_income_x_scroll.set)
    view_income_table.grid(row=0, column=0)

    # Configure Scrollbars
    view_income_y_scroll.config(command=view_income_table.yview)
    view_income_x_scroll.config(command=view_income_table.xview)

    view_income_table['columns'] = ('income_id', 'date', 'amount', 'category', 'payment_method')
    # format our column
    view_income_table.column("#0", width=0, stretch=NO)
    view_income_table.column("income_id", anchor=CENTER, width=80)
    view_income_table.column("date", anchor=CENTER, width=80)
    view_income_table.column("amount", anchor=CENTER, width=80)
    view_income_table.column("category", anchor=CENTER, width=90)
    view_income_table.column("payment_method", anchor=CENTER, width=150)

    # Create Headings
    view_income_table.heading("#0", text="", anchor=CENTER)
    view_income_table.heading("income_id", text="ID", anchor=CENTER)
    view_income_table.heading("date", text="Date", anchor=CENTER)
    view_income_table.heading("amount", text="Amount", anchor=CENTER)
    view_income_table.heading("category", text="Category", anchor=CENTER)
    view_income_table.heading("payment_method", text="Mode of Payment", anchor=CENTER)

    no_data_label = Label(new_window, text='No Data Available', fg='red')
    no_data_label.grid_forget()  # Hidden initially

    def submit():
        start_date = start_date_input.get_date()
        end_date = end_date_input.get_date()

        selected_category = category_var.get()

        income_data['date'] = pd.to_datetime(income_data['date'])

        filtered_data = income_data[(income_data['date'] >= pd.to_datetime(start_date)) &
                                    (income_data['date'] <= pd.to_datetime(end_date))]

        if selected_category != 'All':
            filtered_data = filtered_data[filtered_data['category'] == selected_category]

        # Clear the Treeview
        for row in view_income_table.get_children():
            view_income_table.delete(row)

        # Insert filtered data into the Treeview
        if filtered_data.empty:
            no_data_label.grid(row=3, column=0, columnspan=4)
        else:
            for _, row in filtered_data.iterrows():
                view_income_table.insert('', 'end', values=(int(row['income_id']),
                                                            row['date'].strftime('%Y-%m-%d'), row['amount'],
                                                            row['category'],row['payment_method']))

    Button(new_window, text="Submit", command=submit).grid(row=1, column=3, columnspan=2, pady=10)


def edit_and_delete_income():
    new_window = Toplevel(window)
    new_window.title('Edit/Delete Expenses')
    new_window.geometry('550x410')
    new_window.resizable(False, False)

    Label(new_window, text='Start Date: ').grid(row=0, column=0, padx=10, pady=5)
    start_date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                                 date_pattern='yyyy/MM/dd')
    start_date_input.grid(row=0, column=1, padx=10, pady=5)

    Label(new_window, text='End Date: ').grid(row=0, column=2, padx=10, pady=5)
    end_date_input = DateEntry(new_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                               date_pattern='yyyy/MM/dd')
    end_date_input.grid(row=0, column=3, padx=10, pady=5)

    category_values = ['Primary', 'Secondary', 'Passive']
    category_var = StringVar(value='All')
    Label(new_window, text='Category: ').grid(row=1, column=0, padx=10, pady=5)
    category_input = OptionMenu(new_window, category_var, *category_values)
    category_input.grid(row=1, column=1, padx=10, pady=5)

    # Frame for Treeview and Scrollbars
    view_income_frame = Frame(new_window)
    view_income_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # Scrollbars
    view_income_y_scroll = Scrollbar(view_income_frame, orient='vertical')
    view_income_y_scroll.grid(row=0, column=1, sticky='ns')

    view_income_x_scroll = Scrollbar(view_income_frame, orient='horizontal')
    view_income_x_scroll.grid(row=2, column=0, sticky='ew')

    # Treeview to display income
    view_income_table = ttk.Treeview(view_income_frame, yscrollcommand=view_income_y_scroll.set,
                                     xscrollcommand=view_income_x_scroll.set)
    view_income_table.grid(row=0, column=0)

    # Configure Scrollbars
    view_income_y_scroll.config(command=view_income_table.yview)
    view_income_x_scroll.config(command=view_income_table.xview)

    view_income_table['columns'] = ('income_id', 'date', 'amount', 'category', 'payment_method')
    # format our column
    view_income_table.column("#0", width=0, stretch=NO)
    view_income_table.column("income_id", anchor=CENTER, width=80)
    view_income_table.column("date", anchor=CENTER, width=80)
    view_income_table.column("amount", anchor=CENTER, width=80)
    view_income_table.column("category", anchor=CENTER, width=90)
    view_income_table.column("payment_method", anchor=CENTER, width=150)

    # Create Headings
    view_income_table.heading("#0", text="", anchor=CENTER)
    view_income_table.heading("income_id", text="ID", anchor=CENTER)
    view_income_table.heading("date", text="Date", anchor=CENTER)
    view_income_table.heading("amount", text="Amount", anchor=CENTER)
    view_income_table.heading("category", text="Category", anchor=CENTER)
    view_income_table.heading("payment_method", text="Mode of Payment", anchor=CENTER)

    no_data_label = Label(new_window, text='No Data Available', fg='red')
    no_data_label.grid_forget()  # Hidden initially

    def submit():
        start_date = start_date_input.get_date()
        end_date = end_date_input.get_date()

        selected_category = category_var.get()

        income_data['date'] = pd.to_datetime(income_data['date'])

        filtered_data = income_data[(income_data['date'] >= pd.to_datetime(start_date)) &
                                    (income_data['date'] <= pd.to_datetime(end_date))]

        if selected_category != 'All':
            filtered_data = filtered_data[filtered_data['category'] == selected_category]

        # Clear the Treeview
        for row in view_income_table.get_children():
            view_income_table.delete(row)

        # Insert filtered data into the Treeview
        if filtered_data.empty:
            no_data_label.grid(row=3, column=0, columnspan=4)
        else:
            for _, row in filtered_data.iterrows():
                view_income_table.insert('', 'end', values=(int(row['income_id']),
                                                            row['date'].strftime('%Y-%m-%d'), row['amount'],
                                                            row['category'], row['payment_method']))

    Button(new_window, text="Submit", command=submit).grid(row=1, column=3, columnspan=2, pady=10)

    def edit_selected():
        global income_data
        selected_item = view_income_table.selection()  # Get selected row

        if selected_item:
            item_values = view_income_table.item(selected_item, 'values')

            # Extract the first value (income_id) from the tuple
            income_id = int(item_values[0])
            edit_window = Toplevel(window)
            edit_window.title(f'Edit Expense #{income_id}')
            edit_window.geometry('300x250')
            edit_window.resizable(False, False)

            Label(edit_window, text=f'Expense ID: {income_id}').grid(row=0, column=0, padx=10, pady=10, sticky='w')

            # Retrieve current values
            current_amount = income_data.loc[income_data['income_id'] == income_id, 'amount'].values[0]
            current_date = income_data.loc[income_data['income_id'] == income_id, 'date'].values[0]
            current_category = income_data.loc[income_data['income_id'] == income_id, 'category'].values[0]
            current_payment_method = income_data.loc[income_data['income_id'] == income_id, 'payment_method'].values[0]

            Label(edit_window, text='Date: ').grid(row=1, column=0, padx=10, pady=5, sticky='w')
            date_input = DateEntry(edit_window, width=12, background='darkblue', foreground='white', borderwidth=2,
                                   date_pattern='yyyy/MM/dd')  # Correct date format
            date_input.set_date(pd.to_datetime(current_date, dayfirst=True).date())  # Ensure day-first parsing
            date_input.grid(row=1, column=1, padx=10, pady=5)

            vcmd = (edit_window.register(validate_numeric_input), '%P')
            Label(edit_window, text='Amount: ').grid(row=2, column=0, padx=10, pady=5, sticky='w')
            amount_input = Entry(edit_window, validate='key', validatecommand=vcmd)
            amount_input.insert(0, current_amount)
            amount_input.grid(row=2, column=1, padx=10, pady=5)

            category_values = ['Primary', 'Secondary', 'Passive']
            category_var = StringVar(value=current_category)
            Label(edit_window, text='Category: ').grid(row=3, column=0, padx=10, pady=5)
            category_input = OptionMenu(edit_window, category_var, *category_values)
            category_input.grid(row=3, column=1, padx=10, pady=5)

            Label(edit_window, text='Payment Method: ').grid(row=4, column=0, padx=10, pady=5, sticky='w')
            payment_method_values = ['Bank Transfer', 'Online']
            payment_method_var = StringVar(value=current_payment_method)
            payment_method_input = OptionMenu(edit_window, payment_method_var, *payment_method_values)
            payment_method_input.grid(row=4, column=1, padx=10, pady=5)

            def update_income():
                global income_data
                # Ensure correct format and day-first approach
                new_date = date_input.get_date().strftime('%Y-%m-%d')  # Format date as day-month-year
                new_amount = float(amount_input.get())  # Convert to float if necessary
                new_category = category_var.get()
                new_payment_method = payment_method_var.get()

                # Update DataFrame
                income_data.loc[income_data['income_id'] == income_id, 'date'] = new_date
                income_data.loc[income_data['income_id'] == income_id, 'amount'] = new_amount
                income_data.loc[income_data['income_id'] == income_id, 'category'] = new_category
                income_data.loc[income_data['income_id'] == income_id, 'payment_method'] = new_payment_method

                # Update the displayed values in the Treeview
                view_income_table.item(selected_item,
                                        values=(income_id, new_date, new_amount, new_category, new_payment_method))

                # Save the updated data to CSV
                income_data.to_csv('income.csv', index=False)
                income_data = pd.read_csv('income.csv', dayfirst=True)  # Ensure day-first when reloading

                # Close edit window and show success message
                edit_window.destroy()
                messagebox.showinfo("Success", f"Expense #{income_id} updated successfully!")

            Button(edit_window, text="Update", command=update_income).grid(row=5, column=0, columnspan=2, pady=10)

        else:
            messagebox.showerror("Error", "No entry selected to edit.")

    def delete_selected():
        global income_data

        selected_item = view_income_table.selection()

        if selected_item:
            item_values = view_income_table.item(selected_item, 'values')

            income_id = int(item_values[0])

            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
            if confirm:
                view_income_table.delete(selected_item)

                income_data = income_data[income_data['income_id'] != income_id]

                income_data.to_csv('income.csv', index=False)
            else:
                messagebox.showerror("Error", "No entry selected to delete.")
        else:
            messagebox.showerror("Error", "No entry selected to delete.")

    Button(new_window, text="Submit", command=submit).grid(row=1, column=3, columnspan=2, pady=10)
    Button(new_window, text="Edit Selected", command=edit_selected).grid(row=4, column=0, columnspan=3, pady=5)
    Button(new_window, text="Delete Selected", command=delete_selected).grid(row=4, column=1, columnspan=4, pady=5)

def recent_transactions():
    global expense_data, income_data

    new_window = Toplevel(window)
    new_window.title('Edit/Delete Expenses')
    new_window.geometry('520x280')
    new_window.resizable(False, False)

    # Frame for Treeview and Scrollbars
    view_income_frame = Frame(new_window)
    view_income_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # Scrollbars
    view_income_y_scroll = Scrollbar(view_income_frame, orient='vertical')
    view_income_y_scroll.grid(row=0, column=1, sticky='ns')

    view_income_x_scroll = Scrollbar(view_income_frame, orient='horizontal')
    view_income_x_scroll.grid(row=2, column=0, sticky='ew')

    # Treeview to display income
    view_income_table = ttk.Treeview(view_income_frame, yscrollcommand=view_income_y_scroll.set,
                                     xscrollcommand=view_income_x_scroll.set)
    view_income_table.grid(row=0, column=0)

    # Configure Scrollbars
    view_income_y_scroll.config(command=view_income_table.yview)
    view_income_x_scroll.config(command=view_income_table.xview)

    view_income_table['columns'] = ('type', 'date', 'amount', 'category', 'payment_method')
    # format our column
    view_income_table.column("#0", width=0, stretch=NO)
    view_income_table.column("type", anchor=CENTER, width=80)
    view_income_table.column("date", anchor=CENTER, width=80)
    view_income_table.column("amount", anchor=CENTER, width=80)
    view_income_table.column("category", anchor=CENTER, width=90)
    view_income_table.column("payment_method", anchor=CENTER, width=150)

    # Create Headings
    view_income_table.heading("#0", text="", anchor=CENTER)
    view_income_table.heading("type", text="Type", anchor=CENTER)
    view_income_table.heading("date", text="Date", anchor=CENTER)
    view_income_table.heading("amount", text="Amount", anchor=CENTER)
    view_income_table.heading("category", text="Category", anchor=CENTER)
    view_income_table.heading("payment_method", text="Mode of Payment", anchor=CENTER)

    no_data_label = Label(new_window, text='No Data Available', fg='red')
    no_data_label.grid_forget()  # Hidden initially

    # Load and process data
    income_data = pd.read_csv('income.csv')
    expense_data = pd.read_csv('MOCK_DATA.csv')

    # Add a 'Type' column dynamically
    income_data['type'] = 'Income'
    expense_data['type'] = 'Expense'

    recent_df = pd.concat([income_data.tail(), expense_data.tail()])
    recent_df['date'] = pd.to_datetime(recent_df['date'])
    recent_df = recent_df.sort_values(by='date', ascending=False)

    for row in view_income_table.get_children():
            view_income_table.delete(row)

    # Insert filtered data into the Treeview
    if recent_df.empty:
        no_data_label.grid(row=3, column=0, columnspan=4)
    else:
        for _, row in recent_df.iterrows():
            view_income_table.insert('', 'end', values=(row['type'],
                                                        row['date'].strftime('%Y-%m-%d'), row['amount'],
                                                        row['category'], row['payment_method']))


# Main Tkinter window
window = Tk()
window.title('FMS')
window.geometry("900x500")

# Menus
menubar = Menu(window)
window.config(menu=menubar)

dashboard_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Dashboard', menu=dashboard_menu)
dashboard_menu.add_command(label='Summary Overview')
dashboard_menu.add_command(label='Recent Transactions', command=recent_transactions)
dashboard_menu.add_separator()
dashboard_menu.add_command(label='Exit', command=window.quit)

expenses_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Expenses', menu=expenses_menu)
expenses_menu.add_command(label='Add Expense', command=add_expense)
expenses_menu.add_command(label='View Expenses', command=view_expense)
expenses_menu.add_command(label='Edit/Delete Expense', command=edit_and_delete_expense)

income_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Income', menu=income_menu)
income_menu.add_command(label='Add Income', command=add_income)
income_menu.add_command(label='View Income', command=view_income)
income_menu.add_command(label='Edit/Delete Income', command=edit_and_delete_income)

budget_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Budget', menu=budget_menu)
budget_menu.add_command(label='Set Budget')
budget_menu.add_command(label='View Budget')
budget_menu.add_command(label='Edit Budget')
budget_menu.add_command(label='Delete Budget')

calculator_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Calculators', menu=calculator_menu)
calculator_menu.add_command(label='Budget Calculator')
calculator_menu.add_command(label='Savings Calculator')
calculator_menu.add_command(label='Loan Calculator')
calculator_menu.add_command(label='Investment Calculator')

settings_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Settings', menu=settings_menu)
settings_menu.add_command(label='Categories')
settings_menu.add_command(label='Currency')
settings_menu.add_command(label='User Preferences')

help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='User Guide')
help_menu.add_command(label='FAQs')
help_menu.add_separator()
help_menu.add_command(label='About')

# text_widget = Text(window, height=20, width=40)
# text_widget.pack()

# Categorize Expense
expense_by_catg = expense_data.groupby('category')['amount'].sum()
# print(expense_by_catg)
#
# text_widget.insert(END, "Expenses by Category:\n")
# for category, amount in expense_by_catg.items():
#     text_widget.insert(END, f"{category}: ${amount:.2f}\n")
#
# text_widget.config(state=DISABLED)
window.mainloop()
