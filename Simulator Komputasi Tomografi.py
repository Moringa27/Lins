import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.simpledialog import askinteger
from PIL import Image, ImageTk
import numpy as np
from skimage.transform import radon, iradon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure




print("""Tema tersedia:
light = 1
dark = 2""")
tema_pilihan = int(input('Masukkan kode tema pilihan: '))

if tema_pilihan == 1:
    tema_pilihan = 'light'
elif tema_pilihan == 2:
    tema_pilihan = 'dark'

class ImageReconstructionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator Komputasi Tomografi")

        #Pilihan tema
        self.theme_var = tk.StringVar()

        # Create a style to customize the menu bar
        self.style = ttk.Style()

        #Mengatur tema warna
        self.change_theme()

        #Menu Bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Petunjuk Penggunaan", command=self.show_help)

        #Ukuran gambar default
        self.width = 300
        self.height = 300
        
        #Jumlah Proyeksi Default
        #self.num_proj = 180
        #self.theta = np.linspace(0., 180., self.num_proj, endpoint=False)

        #Jenis Filter Default
        self.filter_type = 'hann'
        
        self.image_data = None
        self.sino_data = None
        self.theta = None
        self.return_image = None
        self.intensitas_input = None
        self.intensitas_output = None
        self.ri = None


        # GUI components
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, padx=5, pady=5)

        button_width = 20

        self.buka_gambar_button = tk.Button(self.frame, text="Buka Gambar", command=self.buka_gambar, width=button_width)
        self.buka_gambar_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        self.original_image_label = tk.Label(self.frame, text="citra asli")
        self.original_image_label.grid(row=1, column=0, pady=5, padx=5)

        self.original_image_canvas = tk.Canvas(self.frame, width=self.width, height=self.height)
        self.original_image_canvas.grid(row=2, column=0, pady=5, padx=5)

        self.histogram_awal_button = tk.Button(self.frame, text="Histogram Awal", command=self.histogram_awal, width=button_width)
        self.histogram_awal_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.radon_transform_label = tk.Label(self.frame, text="Plot Histogram awal")
        self.radon_transform_label.grid(row=1, column=1, pady=5, padx=5)

        #self.radon_transform_canvas = tk.Canvas(self.frame, width=self.width, height=self.height)
        #self.radon_transform_canvas.grid(row=5, column=0, pady=5, padx=5)

        self.hasil_proyeksi_button = tk.Button(self.frame, text="Hasil Proyeksi", command=self.hasil_proyeksi, width=button_width)
        self.hasil_proyeksi_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.reconstructed_image_label = tk.Label(self.frame, text="Hasil Proyeksi")
        self.reconstructed_image_label.grid(row=1, column=2, pady=5, padx=5)

        self.reconstructed_image_label = tk.Label(self.frame, text="Hasil Rekonstruksi")
        self.reconstructed_image_label.grid(row=5, column=0, pady=5, padx=5)

        self.radon_recon_label = tk.Label(self.frame, text="histogram rekonstruksi")
        self.radon_recon_label.grid(row=5, column=1, pady=5, padx=5)

        self.rekonstruksi_citra_button = tk.Button(self.frame, text="Rekonstruksi Citra", command=self.rekonstruksi_citra, width=button_width)
        self.rekonstruksi_citra_button.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        self.reconstructed_image_canvas = tk.Canvas(self.frame, width=self.width, height=self.height)
        self.reconstructed_image_canvas.grid(row=6, column=0, pady=5, padx=5)

        self.histogram_rekon_button = tk.Button(self.frame, text="Histogram Rekon", command=self.histogram_rekon, width=button_width)
        self.histogram_rekon_button.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        
        #self.radon_transform_canvas = tk.Canvas(self.frame, width=self.width, height=self.height)
        #self.radon_transform_canvas.grid(row=, column=, pady=5, padx=5)

        self.profile_intensity_button = tk.Button(self.frame, text="Profile Intensity", command=self.plot_intensity_profiles, width=button_width)
        self.profile_intensity_button.grid(row=3, column=2, padx=5, pady=5, sticky='ew')

        self.profil_label = tk.Label(self.frame, text="Profil Intensitas")
        self.profil_label.grid(row=5, column=2, pady=5, padx=5)



    def resize_image(self):
        if self.image_data is not None:
            # Ask the user for the new size
            new_width = simpledialog.askinteger("Resize Image", "Enter the new width:", initialvalue=self.width)
            if new_width is not None:
                self.width = new_width
            
            new_height = simpledialog.askinteger("Resize Image", "Enter the new height:", initialvalue=self.height)
            if new_height is not None:
                self.height = new_height
                
            # Resize the image
            resized_image_data = np.array(Image.fromarray(self.image_data).resize((new_width, new_height)))

            # Update the displayed image
            self.show_image(resized_image_data, self.original_image_canvas) 

    def show_image(self, image_data, canvas):
        if image_data is not None:
            image = Image.fromarray(image_data)
            photo = ImageTk.PhotoImage(image)
            canvas.config(width=image.width, height=image.height)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo
            
    def buka_gambar(self):
        file_path = filedialog.askopenfilename(title="Select Image File",
                                                filetypes=[("Image files", "*.bmp;*.jpg;*.png")])
        if file_path:
            self.image_data = np.array(Image.open(file_path))
            self.intensitas_input = np.mean(self.image_data)

            # Check if the image is color or grayscale
            if len(self.image_data.shape) == 3:  # assuming color image
                self.ri = np.mean(self.image_data[:, :, 0])  # Choose the appropriate channel
            else:
                self.ri = np.mean(self.image_data)

            # Resize the image
            self.resize_image()


    def histogram_awal(self):
        #Create a Figure for the histogram
        fig, ax = plt.subplots(figsize=(3, 3))
        
        # Plot the histogram
        # Perform the same scaling for the original image
        self.image_data = (self.image_data * 255).astype(np.uint8)

        ax.hist(self.image_data.flatten(), bins=256, range=(0, 256), density=True, color='blue', alpha=0.7)
        ax.grid(True)

        # Set the font size for labels
        ax.set_xlabel('Pixel Value', fontsize=6)  # Adjust the fontsize as needed
        ax.set_ylabel('Frequency', fontsize=6)
        ax.tick_params(axis='both', which='both', labelsize=5)
        print("Mean Pixel Value - Original:", np.mean(self.image_data))

        # Create a Canvas widget for Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas_widget = canvas.get_tk_widget()

        # Embed the Canvas widget into the Tkinter frame
        canvas_widget.grid(row=2, column=1, columnspan=1, pady=3, padx=3)

        # Draw the Canvas
        canvas.draw()

    def hasil_proyeksi(self):
        new_num_proj = askinteger("Jumlah Proyeksi", "Masukkan Jumlah Proyeksi:")
        if new_num_proj is not None:
            self.num_proj = new_num_proj
            self.theta = np.linspace(0., self.num_proj, endpoint=False)

        # Create a circular mask
        center = (self.image_data.shape[0] // 2, self.image_data.shape[1] // 2)
        radius = min(center[0], center[1])
        y, x = np.ogrid[:self.image_data.shape[0], :self.image_data.shape[1]]
        mask = ((x - center[1]) ** 2 + (y - center[1]) ** 2 > (self.image_data.shape[0] // 2) ** 2)

        # Apply the mask to the image
        self.image_data[mask] = 0

        # Calculate pad_width based on the shape of the image_data
        pad_width = ((0, 0), (self.image_data.shape[0] // 2, self.image_data.shape[0] // 2))

        # Zero-padding the image to avoid the warning
        padded_image = np.pad(self.image_data, pad_width, mode='constant', constant_values=0)
        print("padded_image shape:", padded_image.shape)

        self.sino_data = radon(padded_image, theta=self.theta)
        print("sino_data shape:", self.sino_data.shape)

        # Display the projection result
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.grid(True)

        ax.imshow(self.sino_data, cmap='gray', extent=(0, 360, 0, self.sino_data.shape[0]), aspect='auto')
        ax.set_title('Radon Transform', fontsize=8)
        ax.set_xlabel('Projection Angle (degrees)',fontsize=7)
        ax.set_ylabel('Projection Position',fontsize=7)
        ax.tick_params(axis='both', which='both', labelsize=6)
    
        # Create a Canvas widget for Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas_widget = canvas.get_tk_widget()

        # Embed the Canvas widget into the Tkinter frame
        canvas_widget.grid(row=2, column=2, columnspan=1, pady=3, padx=3)

        # Draw the Canvas
        canvas.draw()

    
    def rekonstruksi_citra(self):
        if self.sino_data is None or self.theta is None:
            messagebox.showerror("Error", "Proyeksi sinogram belum dihitung. Hitung proyeksi terlebih dahulu.")
            return

        # Menyediakan pilihan filter yang tersedia
        available_filters = ['hann', 'ramp', 'shepp-logan', 'cosine', 'butterworth']
        filter_str = ', '.join(available_filters)

        # Get the user-inputted filter_type value using simpledialog
        new_filter_type = simpledialog.askstring("Jenis Filter", f"Masukkan Jenis Filter ({filter_str}):", initialvalue=self.filter_type)
        if new_filter_type is not None and new_filter_type in available_filters:
            self.filter_type = new_filter_type

            try:
                radon_image = iradon(self.sino_data, theta=self.theta, filter_name=self.filter_type, interpolation='linear')
                if radon_image is not None:
                    self.return_image = radon_image
                    self.return_image = (self.return_image * 255).astype(np.uint8)  # Convert to uint8 if necessary
                    # Flip nilai piksel jika diperlukan
                    self.return_image = 255 - self.return_image
            
                    # Show the resized image with the button
                    self.show_resized_reconstructed_image()
                else:
                    messagebox.showerror("Error", "Error in reconstructing image. Radon image is None.")
            except Exception as e:
                messagebox.showerror("Error", f"Error in reconstructing image: {str(e)}")


    def show_resized_reconstructed_image(self):
        # Ask the user for the new size
        new_width = simpledialog.askinteger("Resize Image", "Enter the new width:", initialvalue=self.width)
        if new_width is not None:
                self.width = new_width
        new_height = simpledialog.askinteger("Resize Image", "Enter the new height:", initialvalue=self.height)
        if new_width is not None:
                self.height = new_height
                
        # Resize the reconstructed image
        resized_reconstructed_image = np.array(Image.fromarray(self.return_image).resize((new_width, new_height)))

        # Update the displayed images on the canvases
        #self.show_image(self.image_data, self.original_image_canvas)
        #self.show_image(self.sino_data, self.radon_transform_canvas)
        self.show_image(resized_reconstructed_image, self.reconstructed_image_canvas)

    def resize_reconstructed_image(self):
        if self.return_image is not None:
            # Ask the user for the new size
            new_width = simpledialog.askinteger("Resize Image", "Enter the new width:", initialvalue=self.width)
            if new_width is not None:
                self.width = new_width
            new_height = simpledialog.askinteger("Resize Image", "Enter the new height:", initialvalue=self.height)
            if new_width is not None:
                self.height = new_height
                
            # Resize the reconstructed image
            resized_reconstructed_image = np.array(Image.fromarray(self.return_image).resize((new_width, new_height)))

            # Update the displayed images on the canvases
           # self.show_image(self.image_data, self.original_image_canvas)
            #self.show_image(self.sino_data, self.radon_transform_canvas)
            self.show_image(resized_reconstructed_image, self.reconstructed_image_canvas)

       # else:
           # messagebox.showwarning("Warning", "No reconstructed image to resize. Please reconstruct an image first.")

       
    def histogram_rekon(self):
        if self.return_image is None:
            messagebox.showerror("Error", "Reconstructed image is None.")
            return

        # Convert to uint8 if necessary
        self.return_image = (self.return_image * 255).astype(np.uint8)
        
        #Create a Figure for the histogram
        fig, ax = plt.subplots(figsize=(3, 3))

        ax.hist(self.return_image.flatten(), bins=256, range=(0, 256), density=True, color='green', alpha=0.7)
        ax.grid(True)

        ax.set_xlabel('Pixel Value', fontsize=6)  # Adjust the fontsize as needed
        ax.set_ylabel('Frequency', fontsize=6)
        ax.tick_params(axis='both', which='both', labelsize=5)
        # Add these lines at the end of both functions to display the mean pixel value

        print("Mean Pixel Value - Reconstructed:", np.mean(self.return_image))

        # Create a Canvas widget for Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas_widget = canvas.get_tk_widget()

        # Embed the Canvas widget into the Tkinter frame
        canvas_widget.grid(row=6, column=1, columnspan=1, pady=3, padx=3)

        # Draw the Canvas
        canvas.draw()
    

    def plot_intensity_profiles(self):
        if self.image_data is not None and self.return_image is not None:
        # Get the center of the image
            center = (self.image_data.shape[0] // 2, self.image_data.shape[1] // 2)

        # Extract intensity profiles along a horizontal and vertical line passing through the center
            horizontal_profile_original = self.image_data[center[0], :]
            vertical_profile_original = self.image_data[:, center[1]]

            horizontal_profile_reconstructed = self.return_image[center[0], :]
            vertical_profile_reconstructed = self.return_image[:, center[1]]


        # Normalize the reconstructed profiles to have a similar mean as the original
            mean_original_horizontal = np.mean(horizontal_profile_original)
            mean_original_vertical = np.mean(vertical_profile_original)

            mean_reconstructed_horizontal = np.mean(horizontal_profile_reconstructed)
            mean_reconstructed_vertical = np.mean(vertical_profile_reconstructed)

            horizontal_profile_reconstructed = (horizontal_profile_reconstructed + mean_original_horizontal - mean_reconstructed_horizontal)
            vertical_profile_reconstructed = (vertical_profile_reconstructed + mean_original_vertical - mean_reconstructed_vertical)

        # Create a new Tkinter Toplevel window
            #profile_window = tk.Toplevel(self.root)
            #profile_window.title("Intensity Profiles")

        # Create a Matplotlib figure
            fig = Figure(figsize=(6, 3))

        # Plot horizontal intensity profiles
            ax1 = fig.add_subplot(1, 2, 1)
            ax1.plot(horizontal_profile_original, label='Horizontal Profile (Original)')
            ax1.plot(horizontal_profile_reconstructed, label='Horizontal Profile (Reconstructed)')
            ax1.set_title('Horizontal Intensity Profiles', fontsize=6)
            ax1.set_xlabel('Pixel Position', fontsize=6)
            ax1.set_ylabel('Intensity', fontsize=6)
            ax1.tick_params(axis='both', which='both', labelsize=5)
            ax1.legend(fontsize=5)

        # Plot vertical intensity profiles
            ax2 = fig.add_subplot(1, 2, 2)
            ax2.plot(vertical_profile_original, label='Vertical Profile (Original)')
            ax2.plot(vertical_profile_reconstructed, label='Vertical Profile (Reconstructed)')
            ax2.set_title('Vertical Intensity Profiles', fontsize=6)
            ax2.set_xlabel('Pixel Position', fontsize=6)
            ax2.set_ylabel('Intensity', fontsize=6)
            ax2.tick_params(axis='both', which='both', labelsize=5)
            ax2.legend(fontsize=5)
            
        # Adjust layout
            plt.tight_layout()

        # Create a Canvas widget for Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            canvas_widget = canvas.get_tk_widget()

        # Embed the Canvas widget into the Tkinter frame
            canvas_widget.grid(row=6, column=2, columnspan=1, pady=3, padx=3)

        # Draw the Canvas
            canvas.draw()
        else:
            messagebox.showwarning("Warning", "No image or reconstructed image to plot intensity profiles.")


    def show_help(self):
        help_text = """
Petunjuk Penggunaan:
1. Buka Gambar:
- Klik menu "File" dan pilih "Buka Gambar".
- Pilih file gambar dengan format BMP, JPG, atau PNG.
- Gambar akan ditampilkan di layar.

2. Histogram Awal:
- Klik tombol "Histogram Awal" untuk menampilkan histogram dari gambar.

3. Hasil Proyeksi:
- Klik tombol "Hasil Proyeksi" untuk menampilkan hasil proyeksi gambar.

4. Rekonstruksi Citra:
- Klik tombol "Rekonstruksi Citra" untuk merekonstruksi citra dari hasil proyeksi.
- Anda dapat mengatur jenis filter dan ukuran citra hasil rekonstruksi.

5. Histogram Rekon:
- Klik tombol "Histogram Rekon" untuk menampilkan histogram citra hasil rekonstruksi.

6. Profile Intensity:
- Klik tombol "Profile Intensity" untuk menampilkan grafik intensitas horizontal dan vertikal.

Note: Pastikan untuk membuka gambar sebelum melakukan operasi lainnya.
        """
        messagebox.showinfo('Petunjuk Penggunaan', help_text)

    def change_theme(self):
        theme_choice = self.theme_var.get()

        if theme_choice == "light":
            self.style.theme_use('clam')  # Atur tema ke 'clam' atau tema sesuai preferensi
            self.root.tk_setPalette(background="#FFFFFF", foreground="#000000")  # Ganti warna sesuai keinginan
            self.style.configure("TButton", font=("Arial", 10), foreground="black", background="#E1E1E1")  # Ganti font dan warna button sesuai keinginan
            self.style.configure("TLabel", font=("Arial", 12, "bold"), foreground="black", background="#F0F0F0")  # Ganti font dan warna label sesuai keinginan

        elif theme_choice == "dark":
            self.style.theme_use('clam')  # Atur tema ke 'clam' atau tema sesuai preferensi
            self.root.tk_setPalette(background="#002240", foreground="#FFFFFF")  # Ganti warna sesuai keinginan
            self.style.configure("TButton", font=("Arial", 10, "bold"), foreground="white", background="#333333")  # Ganti font dan warna button sesuai keinginan
            self.style.configure("TLabel", font=("Arial", 12, "bold"), foreground="white", background="#2E2E2E")  # Ganti font dan warna label sesuai keinginan

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageReconstructionApp(root)

    #ukuran GUI
    window_width = 1250
    window_height = 850
    root.geometry(f"{window_width}x{window_height}")

    # Tema awal
    app.theme_var.set(tema_pilihan)
    app.change_theme()
    
    root.mainloop()
