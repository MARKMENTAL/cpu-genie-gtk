import gi
from gi.repository import Gtk, GdkPixbuf
from cpu_info import get_cpu_info, get_cpu_utilization
import shutil
from datetime import datetime
import os
import webbrowser

gi.require_version('Gtk', '3.0')

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="cpu-genie-gtk")
        self.set_border_width(10)
        self.set_default_size(450, 450)
        self.setup_ui()

    def setup_ui(self):
        # Create a Box to hold everything vertically
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(main_box)

        # Create a Menu Bar
        menu_bar = self.create_menu_bar()
        main_box.pack_start(menu_bar, False, False, 0)

        # Create a Notebook
        notebook = Gtk.Notebook()
        main_box.pack_start(notebook, True, True, 0)

        # CPU Tab
        cpu_grid = self.create_cpu_tab()
        notebook.append_page(cpu_grid, Gtk.Label('CPU'))

        # About Tab
        about_box = self.create_about_tab()
        notebook.append_page(about_box, Gtk.Label('About'))

    def create_menu_bar(self):
        menu_bar = Gtk.MenuBar()

        # Create a File menu
        file_menu = Gtk.Menu()
        file_menu_item = Gtk.MenuItem(label="File")
        file_menu_item.set_submenu(file_menu)
        menu_bar.append(file_menu_item)

        # Add "Get CPU Usage" under File menu
        get_cpu_usage_item = Gtk.MenuItem(label="CPU Usage")
        get_cpu_usage_item.connect("activate", self.on_get_cpu_usage_clicked)
        file_menu.append(get_cpu_usage_item)
        
        export_item = Gtk.MenuItem(label="Export to HTML...")
        export_item.connect("activate", self.on_export_clicked)
        file_menu.append(export_item)

        return menu_bar

    def create_cpu_tab(self):
        cpu_grid = Gtk.Grid(column_homogeneous=True, column_spacing=10, row_spacing=5)
        cpu_grid.set_margin_top(40)  # Margin at the top, increased to push text down

        # Retrieve CPU information
        cpu_manufacturer, cpu_model, cpu_cores, cpu_arch = get_cpu_info()

        # Determine and set the CPU logo
        logo_filename = self.get_cpu_logo_filename(cpu_manufacturer, cpu_model)
        if logo_filename:
            self.attach_cpu_logo(cpu_grid, logo_filename)

        # CPU Architecture, Model, and Cores labels and values
        self.attach_label_and_value(cpu_grid, "CPU Architecture:", cpu_arch, 1)
        self.attach_label_and_value(cpu_grid, "CPU Model:", cpu_model, 2)
        self.attach_label_and_value(cpu_grid, "CPU Cores:", cpu_cores, 3)

        return cpu_grid

    def get_cpu_logo_filename(self, manufacturer, model):
        if manufacturer == "Apple":
            return 'apple-logo.jpg'
        elif "Intel" in model:
            return 'intel-logo.png'
        elif "AMD" in model:
            return 'amd-logo.jpg'
        else:
            return None

    def attach_cpu_logo(self, grid, logo_filename):
        logo_image = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(logo_filename, 100, 100, True)
        logo_image.set_from_pixbuf(pixbuf)
        logo_alignment = Gtk.Alignment.new(0.5, 0.5, 0, 0)
        logo_alignment.add(logo_image)
        grid.attach_next_to(logo_alignment, None, Gtk.PositionType.RIGHT, 1, 1)

    def attach_label_and_value(self, grid, label_text, value_text, row):
        label = Gtk.Label(label=label_text)
        value = Gtk.Label(label=value_text)
        value.set_margin_start(10)  # Left padding
        value.set_margin_end(10)  # Right padding
        value_frame = Gtk.Frame()
        value_frame.add(value)
        value_frame.set_margin_end(20)
        grid.attach(label, 0, row, 1, 1)
        grid.attach_next_to(value_frame, label, Gtk.PositionType.RIGHT, 1, 1)

    def create_about_tab(self):
        about_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        about_box.set_homogeneous(False)
        genie_logo_image = Gtk.Image()
        pixbuf_genie = GdkPixbuf.Pixbuf.new_from_file_at_scale('cpu-genie-gtk.jpg', 200, 200, True)
        genie_logo_image.set_from_pixbuf(pixbuf_genie)
        about_box.pack_start(genie_logo_image, True, True, 0)
        about_message = Gtk.Label("Thanks for trying cpu-genie-gtk by markmental")
        about_message.set_justify(Gtk.Justification.CENTER)
        about_box.pack_start(about_message, True, True, 0)

        # New styled label for "Made for Debian GNU/Linux"
        debian_label = Gtk.Label()
        debian_label.set_markup('<span font="10" weight="bold" foreground="#D70a53">Designed for Debian GNU/Linux</span>')
        debian_label.set_justify(Gtk.Justification.CENTER)
        about_box.pack_start(debian_label, True, True, 0)

        # Link to Mark Mental's GitHub profile
        mark_mental_label = Gtk.Label()
        mark_mental_label.set_markup('<a href="https://github.com/markmental">Visit markmental\'s GitHub Profile</a>')
        mark_mental_label.set_justify(Gtk.Justification.CENTER)
        mark_mental_label.connect("activate-link", self.open_link_callback)
        about_box.pack_start(mark_mental_label, True, True, 0)

        return about_box

    def open_link_callback(self, widget, uri):
        webbrowser.open(uri)
        return True
        
    def on_get_cpu_usage_clicked(self, widget):
        cpu_utilization = get_cpu_utilization()
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="CPU Utilization",
        )
        dialog.format_secondary_text(f"Current CPU Utilization: {cpu_utilization}%")
        dialog.run()
        dialog.destroy()

    def on_export_clicked(self, widget):
        try:
            cpu_manufacturer, cpu_model, cpu_cores, cpu_arch = get_cpu_info()
            cpu_utilization = get_cpu_utilization()
            logo_filename = self.get_cpu_logo_filename(cpu_manufacturer, cpu_model)
            
            # Create directory with CPU's name and current date
            current_date = datetime.now().strftime("%Y-%m-%d")
            dir_name = f"{cpu_model}_{current_date}"
            os.makedirs(dir_name, exist_ok=True)

            # Path for the logo file in the new directory
            logo_path = os.path.join(dir_name, os.path.basename(logo_filename))

            # Copy the logo file
            if logo_filename:
                shutil.copy(logo_filename, logo_path)

            # Create and write to index.html
            html_content = f"""
            <html>
            <head>
                <title>CPU Information</title>
            </head>
            <body>
                <img width="100" src="{os.path.basename(logo_filename)}" alt="CPU Logo">
                <h1>CPU Information</h1>
                <p>Manufacturer: {cpu_manufacturer}</p>
                <p>Model: {cpu_model}</p>
                <p>Cores: {cpu_cores}</p>
                <p>Architecture: {cpu_arch}</p>
                <h2>CPU Usage Snapshot</h2>
                <p>Current CPU Utilization: {cpu_utilization}%</p>
            </body>
            </html>
            """
            with open(os.path.join(dir_name, "index.html"), "w") as f:
                f.write(html_content)

            # Display success message box
            self.show_message_box("Export Successful", f"CPU info successfully exported to {dir_name}/index.html")

        except Exception as e:
            self.show_message_box("Export Failed", f"Failed to export CPU info. Error: {str(e)}", Gtk.MessageType.ERROR)

    def show_message_box(self, title, text, message_type=Gtk.MessageType.INFO):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=message_type,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

