📦 Smart STL Exporter (Live Preview)

A Blender add‑on for professional STL export with automatic unit detection, custom scaling, logfile documentation, and live preview of dimensions in the N‑Panel.
✨ Features

    ✅ Automatic unit detection (Meters, Centimeters, Millimeters, None → correctly scaled to mm)

    ⚙️ Custom Scale: define your own scaling factor for special formats

    📋 Logfile with export history:

        Timestamp

        File name

        Scale factor & unit

        Object list

        Total bounding box

    🖥️ N‑Panel integration:

        Export directly from the sidebar

        Display of the last log entry

        Display of total dimensions

        Button to open the logfile in Blender’s Text Editor

    🔁 Live‑Update Handler:

        Dimensions and bounding box automatically update when objects are changed, scaled, or re‑selected

    🧠 STL module check: warning if Blender’s official STL export add‑on is not enabled

📦 Installation

    Blender → Edit → Preferences → Add-ons → Install… → select the file

    Enable the add‑on ✅

    Also enable: Import‑Export: STL format (.stl)

📐 Usage

    Open the 3D Viewport and press N to open the sidebar

    Go to the Smart STL tab

    Choose:

        Objects to export

        Unit or custom scale factor

    View the live preview of dimensions in mm

    Click Export STL

    Optionally: open the full logfile in the Text Editor

📁 Logfile

    Automatically saved under: Blender Scripts Directory → stl_export_logs → stl_export_log.txt

    Contains the full export history with timestamp and object information

🛠️ Notes

    Blender internally uses meters – for 3D printing, millimeters are usually required

    STL files in millimeters → use automatic detection or set Custom Scale = 1000

    If objects appear too small: set the scene unit to Millimeters or enable scaling

👤 Author

Developed by Andreas Papesch (AndyZ) & copilot