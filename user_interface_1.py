from tkinter import  *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

def sql_run_query(query,parameters=()):
    #connection object
    conn=psycopg2.connect(dbname="studentdb",user="postgres",password="9052251174",host="localhost",port="5432")

    #creating database cursor
    cur=conn.cursor()

    query_result=None
    try:
        cur.execute(query,parameters)
        if query.lower().startswith("select"):
            query_result=cur.fetchall()
        conn.commit()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error",str(e))
    finally:
        cur.close()
        conn.close()
    return query_result


#refreshes the data every time the function is called
def refresh_treeview():
    #to avoid duplicates and clear the current preview
    for item in tree.get_children(): #gives all the rows under tree view
        tree.delete(item)
    #select query will not have any parameters
    records = sql_run_query("select * from students;")
    if records:
        for r in records:
            tree.insert('', END, values=r)

#insert data
def insert_data():
    query="insert into students(name,address,age,number) values(%s,%s,%s,%s)"
    parameters = (name_input.get(),address_input.get(),age_input.get(),num_input.get())
    sql_run_query(query,parameters)
    messagebox.showinfo("Info","Data inserted succesfully ")
    refresh_treeview()

#delete data
def delete_data():
    selected_item=tree.selection()[0] #gives row id
    student_id=tree.item(selected_item)['values'][0] 
    query="delete from students where student_id=%s"
    parameters=(student_id,)
    sql_run_query(query,parameters)
    messagebox.showinfo("Info","Data deleted succesfuly")
    refresh_treeview()
root=Tk()
root.title("Student system")

#update_data 
def update_data():
    selected_item=tree.selection()[0] #gives row id
    student_id=tree.item(selected_item)['values'][0]
    query="update students set name=%s, address=%s, age=%s, number=%s where student_id=%s"
    parameters = (name_input.get(),address_input.get(),age_input.get(),num_input.get(),student_id)
    sql_run_query(query,parameters)
    messagebox.showinfo("Info","Data updated succesfully")
    refresh_treeview()

#create table
def create_table():
    query="Create table if not exists students(student_id serial primary key,name text,address text,age int,number text);"
    sql_run_query(query)
    messagebox.showinfo("Info","Table created")
    refresh_treeview()
#creating a frame
frame = LabelFrame(root,text="student Data")
frame.grid(row=0,column=0,padx=10,pady=10,sticky="ew")

#creating a label on frame not on window
#placing the label on frame at (0,0)
#name
Label(frame,text="Name:").grid(row=0,column=0,padx=2,sticky="w")
name_input=Entry(frame)
name_input.grid(row=0,column=1,pady=2,sticky="ew")

#address
Label(frame,text="Address:").grid(row=1,column=0,padx=2,sticky="w")
address_input=Entry(frame)
address_input.grid(row=1,column=1,pady=2,sticky="ew")

#Age
Label(frame,text="Age:").grid(row=2,column=0,padx=2,sticky="w")
age_input=Entry(frame)
age_input.grid(row=2,column=1,pady=2,sticky="ew")

#number
Label(frame,text="number:").grid(row=3,column=0,padx=2,sticky="w")
num_input=Entry(frame)
num_input.grid(row=3,column=1,pady=2,sticky="ew")

# new frame for buttons
button_frame=Frame(root)
button_frame.grid(row=4,column=0,padx=5,sticky="ew")

#creating table
Button(button_frame,text="Create Table",command=create_table).grid(row=0,column=0,pady=5,sticky="ew")
#insert data
Button(button_frame,text="insert Data",command=insert_data).grid(row=1,column=0,pady=5,sticky="ew")
#read data
Button(button_frame,text="read Data").grid(row=2,column=0,pady=5,sticky="ew")
#update_data
Button(button_frame,text="Update Data",command=update_data).grid(row=3,column=0,pady=5,sticky="ew")
#delete data
Button(button_frame,text="delete Data",command=delete_data).grid(row=4,column=0,pady=5,sticky="ew")

#creating tree veiw
tree_frame=Frame(root)
tree_frame.grid(row=0,column=1,pady=10,sticky="nsew")

#creating the scroll bar
tree_scroll=Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT,fill=Y)

tree=ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="browse")
tree.pack()
#connecting tree_view scroll bar
tree_scroll.config(command=tree.yview)

#creating attribute columns in tree_view
tree['columns']=("student_id","name","address","age","number")
tree.column("#0",width=0,stretch=NO)
tree.column("student_id",anchor=CENTER,width=80)
tree.column("name",anchor=CENTER,width=120)
tree.column("address",anchor=CENTER,width=120)
tree.column("age",anchor=CENTER,width=50)
tree.column("number",anchor=CENTER,width=120)
#configure headings

tree.heading("student_id",text="ID",anchor=CENTER)
tree.heading("name",text="Name",anchor=CENTER)
tree.heading("address",text="Address",anchor=CENTER)
tree.heading("age",text="Age",anchor=CENTER)
tree.heading("number",text="Number",anchor=CENTER)

refresh_treeview()

root.mainloop()