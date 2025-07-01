import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time

class SnapGuesserApp:
    def __init__(self, master):
        self.master = master
        master.title("Snapchat Password Guesser")

        self.running = False
        self.password_list_file = ""
        self.current_attempt = 0
        self.found_password = None

        # Widgets
        self.username_label = tk.Label(master, text="اسم المستخدم:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = tk.Entry(master, width=40)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        self.file_label = tk.Label(master, text="ملف قائمة كلمات المرور:")
        self.file_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.file_path_entry = tk.Entry(master, width=30, state="readonly")
        self.file_path_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(master, text="استعراض", command=self.browse_file)
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)

        self.start_button = tk.Button(master, text="بدء التخمين", command=self.start_guessing)
        self.start_button.grid(row=2, column=0, padx=5, pady=5)
        self.stop_button = tk.Button(master, text="إيقاف التخمين", command=self.stop_guessing, state="disabled")
        self.stop_button.grid(row=2, column=1, padx=5, pady=5)

        self.status_label = tk.Label(master, text="الحالة: جاهز")
        self.status_label.grid(row=3, column=0, padx=5, pady=5, columnspan=3, sticky="w")

        self.progress_label = tk.Label(master, text="التقدم: 0 محاولة")
        self.progress_label.grid(row=4, column=0, padx=5, pady=5, columnspan=3, sticky="w")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            initialdir="./",
            title="اختر ملف قائمة كلمات المرور",
            filetypes=(("ملفات نصية", "*.txt"), ("جميع الملفات", "*.* "))
        )
        if file_path:
            self.password_list_file = file_path
            self.file_path_entry.config(state="normal")
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
            self.file_path_entry.config(state="readonly")

    def start_guessing(self):
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("خطأ", "الرجاء إدخال اسم المستخدم.")
            return
        if not self.password_list_file:
            messagebox.showerror("خطأ", "الرجاء اختيار ملف قائمة كلمات المرور.")
            return

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="الحالة: بدء التخمين...")
        self.current_attempt = 0
        self.found_password = None

        # Start guessing in a separate thread to keep GUI responsive
        self.guessing_thread = threading.Thread(target=self._guess_password_logic, args=(username, self.password_list_file))
        self.guessing_thread.start()

    def stop_guessing(self):
        self.running = False
        self.status_label.config(text="الحالة: إيقاف التخمين...")

    def _guess_password_logic(self, username, password_list_file):
        try:
            with open(password_list_file, 'r', encoding='latin-1') as f:
                for password in f:
                    if not self.running:
                        break
                    password = password.strip()
                    self.current_attempt += 1
                    self.progress_label.config(text=f"التقدم: {self.current_attempt} محاولة - محاولة: {password}")
                    self.master.update_idletasks()

                    # Simulate login attempt
                    # In a real scenario, you would send a request to Snapchat's API here
                    # and check the response.
                    time.sleep(0.01) # Simulate network delay

                    # This is a placeholder for actual password verification
                    if password == "testpassword": # Replace with actual logic to check if password is correct
                        self.found_password = password
                        break

            if self.found_password:
                self.status_label.config(text=f"الحالة: تم العثور على كلمة المرور: {self.found_password}")
                messagebox.showinfo("نجاح", f"تم العثور على كلمة المرور لـ {username}: {self.found_password}")
            elif self.running: # Only if not stopped by user
                self.status_label.config(text="الحالة: لم يتم العثور على كلمة المرور في القائمة.")
                messagebox.showinfo("انتهى", "لم يتم العثور على كلمة المرور في القائمة المحددة.")
            else:
                self.status_label.config(text="الحالة: تم إيقاف التخمين.")

        except FileNotFoundError:
            self.status_label.config(text=f"الحالة: خطأ - ملف قائمة كلمات المرور غير موجود.")
            messagebox.showerror("خطأ", f"ملف قائمة كلمات المرور \'{password_list_file}\' غير موجود.")
        except Exception as e:
            self.status_label.config(text=f"الحالة: خطأ - {e}")
            messagebox.showerror("خطأ", f"حدث خطأ: {e}")
        finally:
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")


if __name__ == '__main__':
    root = tk.Tk()
    app = SnapGuesserApp(root)
    root.mainloop()

