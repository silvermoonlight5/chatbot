import os
import tkinter as tk
import threading
from dotenv import load_dotenv

# Load .env FIRST
load_dotenv()


os.environ["HTTPX_FORCE_IPV4"] = "1"

from openai import OpenAI


client = OpenAI()



def ask_ai():
    user_text = user_input.get().strip()
    if not user_text:
        return

    insert_message(user_text, "user")
    user_input.delete(0, tk.END)

    threading.Thread(
        target=get_ai_response,
        args=(user_text,),
        daemon=True
    ).start()

def get_ai_response(user_text):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text,
            timeout=60
        )
        reply = response.output_text
    except Exception as e:
        reply = f"Error: {e}"

    root.after(0, insert_message, reply, "bot")

def insert_message(text, sender):
    chat_box.config(state=tk.NORMAL)

    tag = "user" if sender == "user" else "bot"
    prefix = "You: " if sender == "user" else "Bot: "

    chat_box.insert(tk.END, f"{prefix}{text}\n\n", tag)
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

# ---------- UI ----------

root = tk.Tk()
root.title("AI Chatbot")
root.geometry("520x450")

chat_box = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 11))
chat_box.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

chat_box.tag_config("user", justify="right", foreground="#1a73e8")
chat_box.tag_config("bot", justify="left", foreground="#D1C6C6")

user_input = tk.Entry(root, font=("Arial", 11))
user_input.pack(padx=10, pady=5, fill=tk.X)

tk.Button(root, text="Send", command=ask_ai).pack(pady=5)

root.mainloop()