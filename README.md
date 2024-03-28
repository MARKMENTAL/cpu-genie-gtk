# cpu-genie-gtk

cpu-genie-gtk is a Python GTK application designed for Debian Linux, providing CPU information and utilization monitoring in a user-friendly interface. Inspired by CPU-Z, this application fetches detailed CPU specifications and real-time utilization data.

## Features

- **CPU Information Display**: View detailed information about your CPU, including manufacturer, model, number of cores, and architecture.
- **Real-time CPU Utilization**: Monitor current CPU utilization to gauge system performance.
- **Export to HTML**: Export CPU information to an HTML file for easy sharing and reference.
- **Sleek Interface**: Enjoy a clean and intuitive user interface for effortless navigation.

## Requirements

- **Python 3**: Ensure you have Python 3 installed on your Debian Linux system.
- **GTK 3.0**: This application relies on GTK 3.0 for its graphical interface.

## Dependencies to install (Debian)
```bash
sudo apt-get install python3-gi gobject-introspection gir1.2-gtk-3.0 python3-psutil
```

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/markmental/cpu-genie-gtk.git
```

2. Navigate to the project directory:

```bash
cd cpu-genie-gtk
```

3. Execute the main script to launch the application:

```bash
python main.py
```

## Usage

Upon launching the application, you will be presented with a window displaying CPU information and utilization data. The main window consists of two tabs:

- **CPU Tab**: Displays detailed CPU information, including architecture, model, and number of cores.
- **About Tab**: Provides information about the application and its creator.

You can navigate between these tabs using the tabs located at the top of the window.

### Exporting CPU Information

To export CPU information to an HTML file, follow these steps:

1. Click on the "File" menu at the top of the window.
2. Select "Export to HTML..." from the dropdown menu.
3. Choose a destination folder for the exported file.
4. A success message will appear upon successful export.

### Monitoring CPU Utilization

To monitor real-time CPU utilization, click on the "File" menu and select "CPU Usage." A dialog box will display the current CPU utilization percentage.

## Credits

cpu-genie-gtk is developed by markmental. Visit [markmental's GitHub Profile](https://github.com/markmental) for more projects and contributions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Note: cpu-genie-gtk is not affiliated with CPU-Z, Intel, Apple, AMD or any other CPU Manufacturer. "CPU-Z" is a registered trademark of CPUID.*
