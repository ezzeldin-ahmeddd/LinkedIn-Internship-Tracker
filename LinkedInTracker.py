import customtkinter as ctk
from internshiptracker import (get_jobs,
                               save_applied,
                               get_applied_jobs,
                               is_applied,
                               remove_applied,
                               export_applied_jobs)
import webbrowser
def apply_job(job):
    save_applied(job)
    run_tracker()
ctk.set_appearance_mode("dark")
def remove_job(job):
    remove_applied(job)
    show_applied_jobs()
    run_tracker()
app=ctk.CTk()
app.title("Linkedin Internship Tracker")
app.geometry("1200x800")
title_label=ctk.CTkLabel(
    app,
    text="Linkedin Internship Tracker",
    font=("Arial", 20, "bold"),
)
title_label.pack(pady=20)
jobs_frame=ctk.CTkScrollableFrame(
    app,
    width=1100,
    height=600,
)
jobs_frame.pack(pady=20)
def run_tracker():
    for widget in jobs_frame.winfo_children():
        widget.destroy()
    jobs=get_jobs()
    for job in jobs:
        card=ctk.CTkFrame(jobs_frame)
        card.pack(
            fill="x",
            padx=10,
            pady=10,
        )
        info=f"""
{job['title']}
{job['company']}
{job['location']}
{job['date posted']}
"""
        label=ctk.CTkLabel(
            card,
            text=info,
            justify="left",
        )
        label.pack(
            anchor="w",
            padx=10,
            pady=10,
        )
        link_button=ctk.CTkButton(
            card,
            text="Open Link",
            command=lambda url=job['link']:
            webbrowser.open(url),
        )
        link_button.pack(
            side="left",
            padx=10,
            pady=10,
        )
        if is_applied(job):
            applied_button=ctk.CTkButton(
                card,
                text="Applied",
                state="disabled",
            )
        else:
            applied_button=ctk.CTkButton(
                card,
                text="Apply",
                command=lambda j=job,
                btn=card:
                apply_job(j)
            )
        applied_button.pack(
            side="right",
            padx=10,
            pady=10,
        )
refresh_button=ctk.CTkButton(
        app,
        text="Refresh",
        command=run_tracker,
    )
refresh_button.pack(pady=20)
sidebar=ctk.CTkFrame(
    app,
    width=200
)
menu_visible=False
def toggle_menu():
    global menu_visible
    if menu_visible:
        sidebar.place_forget()
    else:
        sidebar.place(x=0,y=50,relheight=1)
    menu_visible=not menu_visible
menu_button=ctk.CTkButton(
    app,
    text="☰",
    width=40,
    command=lambda:toggle_menu()
)
jobs_button=ctk.CTkButton(
    sidebar,
    text="Find Jobs",
    command=run_tracker
)
jobs_button.pack(pady=20)
def show_applied_jobs():
    for widget in jobs_frame.winfo_children():
        widget.destroy()
    jobs=get_applied_jobs()
    for job in jobs:
        card = ctk.CTkFrame(jobs_frame)
        card.pack(
            fill="x",
            padx=10,
            pady=10,
        )
        info = f"""
    {job['title']}
    {job['company']}
    {job['location']}
    {job['date posted']}
    """
        label = ctk.CTkLabel(
                card,
                text=info,
                justify="left",
            )
        label.pack(
                anchor="w",
                padx=10,
                pady=10,
            )
        link_button = ctk.CTkButton(
                card,
                text="Open Link",
                command=lambda url=job['link']:
                webbrowser.open(url),
            )
        link_button.pack(
                side="left",
                padx=10,
                pady=10,
            )
        remove_button = ctk.CTkButton(
            card,
            text="Remove Job",
            fg_color="red",
            command=lambda j=job:
            remove_job(j)
        )
        remove_button.pack(
            side="right",
            padx=10,
            pady=10,
        )
        applied_button = ctk.CTkButton(
                card,
                text="Applied",
                command=lambda j=job:
                save_applied(j),
            )
        applied_button.pack(
                side="right",
                padx=10,
                pady=10,
            )
applied_jobs_button=ctk.CTkButton(
    sidebar,
    text="Applied Jobs",
    command=show_applied_jobs
)
applied_jobs_button.pack(pady=20)
export_button=ctk.CTkButton(
    sidebar,
    text="Export Jobs",
    command=export_applied_jobs
)
export_button.pack(pady=20)
menu_button.place(x=10,y=10)

app.mainloop()
        

