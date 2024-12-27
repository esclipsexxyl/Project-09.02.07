from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
import CTkMessagebox
import bcrypt
import base64
import sqlite3
import random
import smtplib
# База данных

connection = sqlite3.connect('myshitty_database.db')
cursor = connection.cursor()

# Главный фрейм (окно регистрации)
    # Аттрибуты
root = ctk.CTk()
root.geometry("400x500")
root._set_appearance_mode("dark")
root.resizable(False,False)
root.title('Окно регистрации')
root.iconbitmap('mark.ico')
root.eval('tk::PlaceWindow . center')
ctk.FontManager.load_font("Nunito.ttf")
# Переключение видимости пароля
viewswitcher1 = True
viewswitcher2 = True
viewswitcher3 = True
currentuser = ""
localpoints = 0
localcode = 1
localmail = ""
admin = False


def switchh1():
    global viewswitcher1
    if viewswitcher1==True:
        viewswitcher1=False
        rpasshider.configure(image=hideicon)
        rpassentry.configure(show="")
    else:
        viewswitcher1=True
        rpasshider.configure(image=viewicon)
        rpassentry.configure(show="*")

def switchh2():
    global viewswitcher2
    if viewswitcher2==True:
        viewswitcher2=False
        rrpasshider.configure(image=hideicon)
        rrpassentry.configure(show="")
    else:
        viewswitcher2=True
        rrpasshider.configure(image=viewicon)
        rrpassentry.configure(show="*")
def switchh3():
    global viewswitcher3
    if viewswitcher3==True:
        viewswitcher3=False
        rpasshiderA.configure(image=hideiconA)
        rpassentryA.configure(show="")
    else:
        viewswitcher3=True
        rpasshiderA.configure(image=viewiconA)
        rpassentryA.configure(show="*")

# Переключения между окнами
def goto_auth():
    root.withdraw()
    authframe.deiconify()

def goto_reset():
    authframe.withdraw()
    emailconf.deiconify()

def goto_reg():
    authframe.withdraw()
    root.deiconify()

def check_on_error():
    getlogin = loginentry.get()
    gotlogin = getlogin.replace(" ", "")
    getpass = rpassentry.get()
    confpass = rrpassentry.get()
    getmail = mailentry.get()
    if len (getlogin) < 1 or len (getpass) < 1 or len (getmail) < 1:
        CTkMessagebox.CTkMessagebox(title="Ошибка!", message="Поля не могут быть пустыми.", icon="cancel",font=("Nunito",14),fade_in_duration=85,topmost=True,button_color="#f7f7f7",button_hover_color="#bfbfbf",button_text_color="#000000")
    elif gotlogin.isdigit():
        CTkMessagebox.CTkMessagebox(title="Ошибка!", message="Логин не может быть числом.", icon="cancel",font=("Nunito",14),fade_in_duration=85,topmost=True,button_color="#f7f7f7",button_hover_color="#bfbfbf",button_text_color="#000000")
    elif getpass!=confpass:
        CTkMessagebox.CTkMessagebox(title="Ошибка!", message="Введенные пароли не совпадают.", icon="cancel",font=("Nunito",14),fade_in_duration=85,topmost=True,button_color="#f7f7f7",button_hover_color="#bfbfbf",button_text_color="#000000")
    else:
        reg_newuser(loginentry.get(), rpassentry.get(), mailentry.get())


def reg_newuser(login,password,mail):
    logincheck = cursor.execute("SELECT * FROM users WHERE login = (?)",(login,)).fetchall()
    if logincheck==[]:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)
        print(f"пароль - {password}, хэш - {password_hash}")
        clearlogin = login.replace(" ","")
        #cursor.execute(f"INSERT INTO users (login, password, points, email) VALUES ('{login}', '{password_hash}', 0, '{mail}')")
        cursor.execute("INSERT INTO users (login, password, points, email) VALUES (?,?,?,?)",(clearlogin,password_hash,0,mail))
        connection.commit()
        CTkMessagebox.CTkMessagebox(title="Уведомление", message="Пользователь был успешно зарегистрирован.",
                                    icon="check", font=("Nunito", 14), fade_in_duration=85, topmost=True,
                                    button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")
        goto_auth()
    else:
        CTkMessagebox.CTkMessagebox(title="Ошибка!", message="Пользователь с таким логином уже существует.", icon="cancel",font=("Nunito",14),fade_in_duration=85,topmost=True,button_color="#f7f7f7",button_hover_color="#bfbfbf",button_text_color="#000000")

def auth_user():
    global currentuser; global admin
    login = loginentryA.get()
    password = rpassentryA.get()
    clearlogin=login.replace(" ","")
    acc = cursor.execute("SELECT * FROM users WHERE login = (?)",(clearlogin,)).fetchall()
    if acc!=[]:
        getpassword = cursor.execute("SELECT password FROM users WHERE login = (?)",(clearlogin,)).fetchone()
        if bcrypt.checkpw(password.encode(), getpassword[0]):
            CTkMessagebox.CTkMessagebox(title="Уведомление", message=f"Добро пожаловать, {login}!",
                                    icon="check", font=("Nunito", 14), fade_in_duration=85, topmost=True,
                                    button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")
            currentuser = clearlogin; authframe.withdraw(); lkframe.deiconify(); infolabel.configure(text=f'Вы вошли под именем: {currentuser}.')
            updatepoints(); pointslabel.configure(text=f"Ваше количество баллов: {localpoints}")
            getadmin = cursor.execute("SELECT adminuse FROM users WHERE login = (?)", (clearlogin,)).fetchone()
            print(getadmin)
            if getadmin[0]==1:
                admin=True
        else:
            CTkMessagebox.CTkMessagebox(title="Ошибка!", message="Неверный пароль.", icon="cancel",font=("Nunito",14),fade_in_duration=85,topmost=True,button_color="#f7f7f7",button_hover_color="#bfbfbf",button_text_color="#000000")
    else:
        CTkMessagebox.CTkMessagebox(title="Ошибка!", message="Пользователь с таким логином не существует.",
                                    icon="cancel", font=("Nunito", 14), fade_in_duration=85, topmost=True,
                                    button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")

def updatepoints():
    global localpoints; global currentuser
    findpoints = cursor.execute("SELECT points FROM users WHERE login = (?)",(currentuser,)).fetchone()
    localpoints = findpoints[0]
    print(f"Количество баллов = {localpoints}")

def addpoints():
    global localpoints; global currentuser; global admin
    if admin==True:
        localpoints=localpoints+1; pointslabel.configure(text=f"Ваше количество баллов: {localpoints}")
        cursor.execute("UPDATE users SET points = ? WHERE login = ?",(localpoints,currentuser))
        connection.commit()

def minuspoints():
    global localpoints; global currentuser; global admin
    if admin==True:
        localpoints=localpoints-1; pointslabel.configure(text=f"Ваше количество баллов: {localpoints}")
        cursor.execute("UPDATE users SET points = ? WHERE login = ?",(localpoints,currentuser))
        connection.commit()

def sendmail():
    global localcode; localcode = random.randint(111111, 999999)
    global localmail; localmail = mailentry2.get()
    mailcheck = cursor.execute("SELECT * FROM users WHERE email = (?)", (localmail,)).fetchall()
    if mailcheck!=[]:
        smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpserver.ehlo()
        smtpserver.login('foxpadte@gmail.com', 'УБРАЛ ПАРОЛЬ ИЗ-ЗА ЦЕЛЕЙ БЕЗОПАСНОСТИ')
        smtpserver.sendmail('foxpadte@gmail.com', localmail, str(localcode))
        smtpserver.close()
        CTkMessagebox.CTkMessagebox(title="Уведомление", message="Код для верификации сброса пароля был отправлен вам на электронную почту.",
                                icon="check", font=("Nunito", 14), fade_in_duration=85, topmost=True,
                                button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")
        emailconf.withdraw()
        emailconf2.deiconify()
    else:
        CTkMessagebox.CTkMessagebox(title="Ошибка",message="Нет пользователя с такой почтой.",icon="cancel", font=("Nunito", 14), fade_in_duration=85, topmost=True,button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")
        emailconf.withdraw()
        authframe.deiconify()

def confirmcode():
    global localcode
    usercode = codeentry.get()
    if str(localcode)==str(usercode):
        CTkMessagebox.CTkMessagebox(title="Уведомление",
                                    message="Код сброса пароля совпадает.",
                                    icon="check", font=("Nunito", 14), fade_in_duration=85, topmost=True,
                                    button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")
        emailconf2.withdraw(); nwpassframe.deiconify()
    else:
        CTkMessagebox.CTkMessagebox(title="Ошибка",
                                    message="Неверный код.",
                                    icon="cancel", font=("Nunito", 14), fade_in_duration=85, topmost=True,
                                    button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")

def resetpass():
    global localmail
    nwpass=nwpassentry.get()
    nwpass2=nwpassentry2.get()
    if len (nwpass) < 1 or len (nwpass2) < 1:
        CTkMessagebox.CTkMessagebox(title="Ошибка",message="Новый пароль не может быть пустым.",icon="cancel", font=("Nunito", 14), fade_in_duration=85, topmost=True,button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")
    elif nwpass!=nwpass2:
        CTkMessagebox.CTkMessagebox(title="Ошибка",message="Введенные пароли не совпадают.",icon="cancel", font=("Nunito", 14), fade_in_duration=85, topmost=True,button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")
    else:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(nwpass.encode(), salt)
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (password_hash, localmail))
        connection.commit()
        CTkMessagebox.CTkMessagebox(title="Уведомление",message="Новый пароль был успешно установлен.",icon="check", font=("Nunito", 14), fade_in_duration=85, topmost=True,button_color="#f7f7f7", button_hover_color="#bfbfbf", button_text_color="#000000")
        nwpassframe.withdraw(); authframe.deiconify()

def exit_user():
    global localpoints;global localuser;global localmail;global admin
    localpoints=0;localuser="";localmail="";admin=False
    lkframe.withdraw()
    rpassentry.delete(0, 'end');rrpassentry.delete(0, 'end');rpassentryA.delete(0, 'end')
    mailentry.delete(0, 'end');loginentry.delete(0, 'end');loginentryA.delete(0, 'end')
    root.deiconify()

# Загрузка иконок в фрейм регистрации
viewicon = ImageTk.PhotoImage(Image.open("./view.ico").resize((20,20)))
hideicon = ImageTk.PhotoImage(Image.open("./hide.ico").resize((20,20)))
    # Виджеты
loginlabel = ctk.CTkLabel(root,text='Логин', font=('Nunito',16));loginlabel.pack(pady=10)
loginentry = ctk.CTkEntry(root, placeholder_text='Придумайте логин', height=35, width=250,font=('Nunito',14));loginentry.pack()
rpasslabel = ctk.CTkLabel(root,text='Пароль', font=('Nunito',16));rpasslabel.pack(pady=10)
rpassentry = ctk.CTkEntry(root, placeholder_text='Придумайте пароль', height=35, width=250, show="*",font=('Nunito',14));rpassentry.pack()
rpasshider = ctk.CTkButton(root, image=viewicon, text='', width=35, fg_color="#f7f7f7", hover_color="#bfbfbf",font=('Nunito',14), command=switchh1);rpasshider.place(x=335,y=135)
rrpasslabel = ctk.CTkLabel(root,text='Подтверждение пароля', font=('Nunito',16));rrpasslabel.pack(pady=10)
rrpassentry = ctk.CTkEntry(root, placeholder_text='Введите пароль', height=35, width=250, show="*",font=('Nunito',14));rrpassentry.pack()
rrpasshider = ctk.CTkButton(root, image=viewicon, text='', width=35, fg_color="#f7f7f7", hover_color="#bfbfbf",font=('Nunito',14), command=switchh2);rrpasshider.place(x=335,y=218)
maillabel = ctk.CTkLabel(root, text='Электронная почта', font=('Nunito',16));maillabel.pack(pady=10)
mailentry = ctk.CTkEntry(root, placeholder_text='Введите почту', height=35, width=250,font=('Nunito',14));mailentry.pack()
regbutton = ctk.CTkButton(root, text='Зарегистрироваться',font=('Nunito',22),text_color="#000000", fg_color="#f7f7f7", hover_color="#bfbfbf", height=45, command=check_on_error);regbutton.pack(pady=35)
toauthbutton = ctk.CTkButton(root, text='Есть аккаунт? Авторизуйтесь здесь.', fg_color="transparent",font=('Nunito',14), hover_color="#242424", command=goto_auth);toauthbutton.place(x=74,y=455)

# Фрейм авторизации

authframe=ctk.CTk()
authframe.geometry("400x500")
authframe._set_appearance_mode("dark")
authframe.resizable(False,False)
authframe.title('Окно авторизации')
authframe.iconbitmap('mark.ico')
#authframe.eval('tk::PlaceWindow . center')

# Загрузка иконок в фрейм авторизации
img1 = Image.open("./view.ico").resize((20,20)); img2 = Image.open("./hide.ico").resize((20,20))
viewiconA = ImageTk.PhotoImage(master=authframe,image=img1)
hideiconA = ImageTk.PhotoImage(master=authframe,image=img2)

    # Виджеты
loginlabelA = ctk.CTkLabel(authframe,text='Логин', font=('Nunito',16));loginlabelA.pack(pady=10)
loginentryA = ctk.CTkEntry(authframe, placeholder_text='Введите логин', height=35, width=250,font=('Nunito',14));loginentryA.pack()
rpasslabelA = ctk.CTkLabel(authframe,text='Пароль', font=('Nunito',16));rpasslabelA.pack(pady=10)
rpassentryA = ctk.CTkEntry(authframe, placeholder_text='Введите пароль', height=35, width=250, show="*",font=('Nunito',14));rpassentryA.pack()
rpasshiderA = ctk.CTkButton(authframe, text='',image=viewiconA, width=35, fg_color="#f7f7f7", hover_color="#bfbfbf", command=switchh3);rpasshiderA.place(x=335,y=135)
authbutton = ctk.CTkButton(authframe, text='Авторизоваться',font=('Nunito',22),text_color="#000000", fg_color="#f7f7f7", hover_color="#bfbfbf", height=45,command=auth_user);authbutton.pack(pady=35)
toresetbutton = ctk.CTkButton(authframe, text='Забыли пароль? Сбросьте его здесь', fg_color="transparent",font=('Nunito',14), hover_color="#242424", command=goto_reset);toresetbutton.place(x=74,y=425)
toregbutton = ctk.CTkButton(authframe, text='Нет аккаунта? Зарегистрируйтесь здесь.', fg_color="transparent",font=('Nunito',14), hover_color="#242424", command=goto_reg);toregbutton.place(x=66,y=455)

# Фрейм личнего кабинета

lkframe=ctk.CTk()
lkframe.geometry("400x500")
lkframe._set_appearance_mode("dark")
lkframe.resizable(False,False)
lkframe.title('Личный кабинет')
lkframe.iconbitmap('profile.ico')

img3 = Image.open("./coin.ico").resize((25,20))
coinimg = ImageTk.PhotoImage(master=lkframe,image=img3)

# Виджеты
infolabel = ctk.CTkLabel(lkframe,text=f'Вы вошли под именем: N/A.', font=('Nunito',16));infolabel.pack(pady=10)
pointslabel = ctk.CTkLabel(lkframe,text=f'Ваше количество баллов: ', font=('Nunito',16));pointslabel.pack(pady=15)
addbutton = ctk.CTkButton(lkframe,image=coinimg, text='Добавить балл',font=('Nunito',22),text_color="#000000", fg_color="#f7f7f7", hover_color="#bfbfbf", height=45,command=addpoints);addbutton.pack(pady=10)
minusbutton = ctk.CTkButton(lkframe,image=coinimg, text='Снять балл',font=('Nunito',22),text_color="#000000", fg_color="#f7f7f7", hover_color="#bfbfbf", height=45,command=minuspoints);minusbutton.pack(pady=5)
exitbutton = ctk.CTkButton(lkframe, text='Выйти из аккаунта', fg_color="transparent",font=('Nunito',14), hover_color="#242424", command=exit_user);exitbutton.place(x=130,y=455)


# Окно сброса пароля 1
emailconf=ctk.CTk()
emailconf.geometry("400x250")
emailconf._set_appearance_mode("dark")
emailconf.resizable(False,False)
emailconf.title('Сброс пароля')
emailconf.iconbitmap('profile.ico')

# Виджеты
maillabel2 = ctk.CTkLabel(emailconf, text='Электронная почта', font=('Nunito',16));maillabel2.pack(pady=10)
mailentry2 = ctk.CTkEntry(emailconf, placeholder_text='Введите почту', height=35, width=250,font=('Nunito',14));mailentry2.pack()
yobutton = ctk.CTkButton(emailconf, text='Отправить сообщение на почту',font=('Nunito',22),text_color="#000000", fg_color="#f7f7f7", hover_color="#bfbfbf", height=45,command=sendmail);yobutton.pack(pady=35)

# Окно сброса пароля 2
emailconf2=ctk.CTk()
emailconf2.geometry("400x250")
emailconf2._set_appearance_mode("dark")
emailconf2.resizable(False,False)
emailconf2.title('Сброс пароля')
emailconf2.iconbitmap('profile.ico')

# Виджеты
codelabel = ctk.CTkLabel(emailconf2, text='Код верификации', font=('Nunito',16));codelabel.pack(pady=10)
codeentry = ctk.CTkEntry(emailconf2, placeholder_text='Введите код с электронной почты', height=35, width=250,font=('Nunito',14));codeentry.pack()
codebutton = ctk.CTkButton(emailconf2, text='Подтвердить',font=('Nunito',22),text_color="#000000", fg_color="#f7f7f7", hover_color="#bfbfbf", height=45,command=confirmcode);codebutton.pack(pady=35)

# Окно сброса пароля 3
nwpassframe=ctk.CTk()
nwpassframe.geometry("400x500")
nwpassframe._set_appearance_mode("dark")
nwpassframe.resizable(False,False)
nwpassframe.title('Сброс пароля')
nwpassframe.iconbitmap('profile.ico')

# Виджеты
nwpasslabel = ctk.CTkLabel(nwpassframe,text='Новый пароль', font=('Nunito',16));nwpasslabel.pack(pady=10)
nwpassentry = ctk.CTkEntry(nwpassframe, placeholder_text='Придумайте пароль', height=35, width=250, font=('Nunito',14));nwpassentry.pack()
nwpasslabel2 = ctk.CTkLabel(nwpassframe,text='Подтверждение пароля', font=('Nunito',16));nwpasslabel2.pack(pady=10)
nwpassentry2 = ctk.CTkEntry(nwpassframe, placeholder_text='Введите пароль', height=35, width=250, font=('Nunito',14));nwpassentry2.pack()
respassbutton = ctk.CTkButton(nwpassframe, text='Сбросить пароль',font=('Nunito',22),text_color="#000000", fg_color="#f7f7f7", hover_color="#bfbfbf", height=45,command=resetpass);respassbutton.pack(pady=35)
# Запуск программы
root.mainloop()


