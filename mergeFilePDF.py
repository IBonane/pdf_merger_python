from PyPDF2 import PdfMerger
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusionner des PDF")

        # Appliquer le thème
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Vous pouvez changer 'clam' à d'autres thèmes disponibles

        # Configurer la taille initiale de la fenêtre
        self.root.geometry("600x600")

        # Cadre principal pour organiser les composants
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=10, expand=True, fill=tk.BOTH)

        # Liste des fichiers PDF
        self.file_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(pady=10, side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Cadre pour les boutons d'action
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10, padx=10, side=tk.LEFT)

        # Bouton pour ajouter des fichiers PDF
        add_button = ttk.Button(button_frame, text="Ajouter des PDF", command=self.add_pdf_files)
        add_button.pack(pady=5, fill=tk.X)

        # Bouton pour supprimer des fichiers PDF sélectionnés
        remove_button = ttk.Button(button_frame, text="Supprimer sélection", command=self.remove_selected_files)
        remove_button.pack(pady=5, fill=tk.X)

        # Bouton pour vider tous les fichiers PDF
        clear_button = ttk.Button(button_frame, text="Vider tous", command=self.clear_all_files)
        clear_button.pack(pady=5, fill=tk.X)

        # Label et champ de saisie pour le nom du fichier fusionné
        result_filename_label = ttk.Label(button_frame, text="Nom du fichier fusionné:")
        result_filename_label.pack(pady=5)

        self.result_filename_entry = ttk.Entry(button_frame)
        self.result_filename_entry.pack(pady=5)

        # Boutons ⇧ et ⇩ pour déplacer les fichiers
        move_buttons_frame = ttk.Frame(button_frame)
        move_buttons_frame.pack(pady=10)

        up_button = ttk.Button(move_buttons_frame, text="⇧", command=self.move_selection_up, width=5)
        up_button.pack(pady=2, padx=5, fill=tk.X)

        down_button = ttk.Button(move_buttons_frame, text="⇩", command=self.move_selection_down, width=5)
        down_button.pack(pady=2, padx=5, fill=tk.X)

        # Bouton pour fusionner les fichiers PDF
        merge_button = ttk.Button(button_frame, text="Fusionner", command=self.merge_pdfs)
        merge_button.pack(pady=10)

        # Bouton pour quitter l'application
        quit_button = ttk.Button(button_frame, text="Quitter", command=self.root.destroy)
        quit_button.pack(pady=40)

    def add_pdf_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Fichiers PDF", "*.pdf")])

        if files:
            for file in files:
                self.file_listbox.insert(tk.END, file)
            print("Fichiers ajoutés :")
            for file in files:
                print(file)

    def remove_selected_files(self):
        selected_indices = self.file_listbox.curselection()

        if selected_indices:
            for index in reversed(selected_indices):
                self.file_listbox.delete(index)

            print("Fichiers supprimés :")
            for index in selected_indices:
                print(self.file_listbox.get(index))

    def clear_all_files(self):
        self.file_listbox.delete(0, tk.END)
        print("Tous les fichiers supprimés.")

    def move_selection_up(self):
        selected_indices = list(self.file_listbox.curselection())

        if selected_indices and selected_indices[0] > 0:
            for index in selected_indices:
                item = self.file_listbox.get(index)
                self.file_listbox.delete(index)
                self.file_listbox.insert(index - 1, item)

            # Mettre à jour la sélection après le déplacement
            new_indices = [index - 1 for index in selected_indices]
            self.file_listbox.selection_clear(0, tk.END)
            for index in new_indices:
                self.file_listbox.selection_set(index)

    def move_selection_down(self):
        selected_indices = list(self.file_listbox.curselection())

        if selected_indices and selected_indices[-1] < self.file_listbox.size() - 1:
            for index in reversed(selected_indices):
                item = self.file_listbox.get(index)
                self.file_listbox.delete(index)
                self.file_listbox.insert(index + 1, item)

            # Mettre à jour la sélection après le déplacement
            new_indices = [index + 1 for index in selected_indices]
            self.file_listbox.selection_clear(0, tk.END)
            for index in new_indices:
                self.file_listbox.selection_set(index)

    def merge_pdfs(self):
        files_to_merge = [self.file_listbox.get(index) for index in range(self.file_listbox.size())]

        if not files_to_merge:
            print("Veuillez ajouter des fichiers PDF.")
            return

        # Demander où enregistrer le fichier fusionné
        result_filename = self.result_filename_entry.get()
        if not result_filename:
            result_filename = "resultat_fusion.pdf"

        self.merged_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Fichiers PDF", "*.pdf")],
                                                             initialfile=result_filename)

        if self.merged_pdf_path:
            # Fusionner les fichiers PDF
            pdf_merger = PdfMerger()
            for file_path in files_to_merge:
                pdf_merger.append(file_path)

            # Enregistrer le fichier fusionné
            with open(self.merged_pdf_path, "wb") as merged_file:
                pdf_merger.write(merged_file)

            print(f"Fusion PDF réussie. Fichier enregistré sous {self.merged_pdf_path}")
        else:
            print("Opération annulée.")

if __name__ == "__main__":
    root = ThemedTk(theme="clam")  # Vous pouvez changer 'clam' à d'autres thèmes disponibles
    app = PDFMergerApp(root)
    root.mainloop()
