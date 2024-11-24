import customtkinter

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.title("CustomTkinter Sample Menu Bar.py")

def button_callback():
    print("Button click", combobox_1.get())

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.grid(row=0, pady=10, padx=0)

optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."])
optionmenu_1.grid(row=0, column=0, pady=10, padx=10)
optionmenu_1.set("CTk Option Menu")

combobox_1 = customtkinter.CTkComboBox(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."])
combobox_1.grid(row=0, column=1, pady=10, padx=0)
combobox_1.set("CTk Combo Box")

appearance_mode_optionemenu = customtkinter.CTkOptionMenu(frame_1, values=["Light", "Dark", "System"], command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=0, column=2, padx=0, pady=10)

scaling_optionemenu = customtkinter.CTkOptionMenu(frame_1, values=["80%", "90%", "100%", "110%", "120%"], command=change_scaling_event)
scaling_optionemenu.grid(row=0, column=3, padx=0, pady=10)

text_1 = customtkinter.CTkTextbox(master=frame_1, width=600, height=70)
text_1.grid(row=1, column=0, columnspan=4, pady=10, padx=10)
text_1.insert("0.0", "Lorem Ipsum adalah contoh teks atau dummy dalam industri percetakan dan penataan huruf atau typesetting. Lorem Ipsum telah menjadi standar contoh teks sejak tahun 1500an, saat seorang tukang cetak yang tidak dikenal mengambil sebuah kumpulan teks dan mengacaknya untuk menjadi sebuah buku contoh huruf. Ia tidak hanya bertahan selama 5 abad, tapi juga telah beralih ke penataan huruf elektronik, tanpa ada perubahan apapun. Ia mulai dipopulerkan pada tahun 1960 dengan diluncurkannya lembaran-lembaran Letraset yang menggunakan kalimat-kalimat dari Lorem Ipsum, dan seiring munculnya perangkat lunak Desktop Publishing seperti Aldus PageMaker juga memiliki versi Lorem Ipsum.")

app.mainloop()