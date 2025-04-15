import tkinter 
from tkinter import *
from tkinter.filedialog import askopenfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from decouple import config

attachment_path = None

email = config("EMAIL")
password = config("PASSWORD")

def go():
    global attachment_path

    email_id = label1_entry.get()
    subject = label2_entry.get()
    body = label3_entry.get()

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email_id
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={attachment_path}")
        msg.attach(part)  
        attachment.close()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email_id, msg.as_string())
    server.quit()

    attachment_path = None

    label1_entry.delete(0, tkinter.END)
    label3_entry.delete(0, tkinter.END)
    label2_entry.delete(0, tkinter.END)
    label4_entry.delete(0, tkinter.END)

    label_temp = Label(frame1, text="Successful")
    label_temp.pack(pady=5, padx=5)

def show():
    file = askopenfile(mode='r', filetypes=[('All Files', '*.*')])
    if file:
        global attachment_path
        attachment_path = file.name
        label4_entry.delete(0, tkinter.END)  
        label4_entry.insert(0, attachment_path)

base = tkinter.Tk()
base.geometry("500x600")

frame1 = Frame(base, width="400", height="500", bg="light green")

label1 = Label(frame1, text="Fast E-Mail", bg="light yellow", fg="black")
label1.pack(pady=10, padx=10)

separator_frame = Frame(frame1, height=1, bg="black")
separator_frame.pack(fill=tkinter.X, pady=5)

label1_ID = Label(frame1, text="Enter receiver's email ID", bg="light green", fg="black")
label1_ID.pack(pady=2, padx=2)
label1_entry = Entry(frame1, width="50", bg="light yellow")
label1_entry.pack(pady=2, padx=2)

label2_ID = Label(frame1, text="Enter Subject", bg="light green", fg="black")
label2_ID.pack(pady=2, padx=2)
label2_entry = Entry(frame1, width="50", bg="light yellow")
label2_entry.pack(pady=2, padx=2)

label3_ID = Label(frame1, text="Enter Body of the message", bg="light green", fg="black")
label3_ID.pack(pady=2, padx=2)
label3_entry = Entry(frame1, width="50", bg="light yellow")
label3_entry.pack(pady=2, padx=2)

label4_ID = Label(frame1, text="Select the file if you want to send the file", bg="light green", fg="black")
label4_ID.pack(pady=2, padx=2)
label4_entry = Entry(frame1, width="50", bg="light yellow")
label4_entry.pack(pady=2, padx=2)
button4 = Button(frame1, text="Open", command=show, width="10", bg="light pink", fg="black")
button4.pack()

button = Button(frame1, text="Send", command=go, width="30", bg="light blue", fg="black")
button.pack(pady=20, padx=10)

frame1.pack(expand=True)

base.mainloop()
