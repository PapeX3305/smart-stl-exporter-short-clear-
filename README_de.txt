 Smart STL Exporter (Live Preview)

Ein Blender‑Add-on für den professionellen Export von STL‑Dateien mit automatischer Einheitenerkennung, benutzerdefinierter Skalierung, Logfile‑Dokumentation und Live‑Vorschau der Maße im N‑Panel.
✨ Features

    ✅ Automatische Einheitenerkennung (Meter, Zentimeter, Millimeter, None → korrekt auf mm skaliert)

    ⚙️ Custom Scale: eigener Skalierungsfaktor für Spezialformate

    📋 Logfile mit Export-Historie:

        Zeitstempel

        Dateiname

        Skalierungsfaktor & Einheit

        Objektliste

        Gesamt‑Bounding‑Box

    🖥️ N‑Panel Integration:

        Export direkt aus dem Sidebar

        Anzeige der letzten Log-Zeile

        Anzeige der Gesamtmaße

        Button zum Öffnen des Logfiles im Blender Texteditor

    🔁 Live‑Update Handler:

        Maße und Bounding Box aktualisieren sich automatisch bei Objekt‑Änderungen, Skalierung oder Auswahlwechsel

    🧠 STL‑Modul‑Check: Warnung, falls das offizielle STL‑Export‑Add-on nicht aktiviert ist

📦 Installation

    Blender → Edit → Preferences → Add-ons → Install… → Datei auswählen

    Add-on aktivieren ✅

    Zusätzlich aktivieren: Import‑Export: STL format (.stl)

📐 Nutzung

    Öffne den 3D‑Viewport und drücke N, um die Sidebar zu öffnen

    Gehe zum Tab Smart STL

    Wähle:

        Objekte für den Export

        Einheit oder benutzerdefinierten Skalierungsfaktor

    Sieh dir die Live‑Vorschau der Maße in mm an

    Klicke auf Export STL

    Optional: Öffne das vollständige Logfile im Texteditor

📁 Logfile

    Automatisch gespeichert unter: Blender Scripts Directory → stl_export_logs → stl_export_log.txt

    Enthält die gesamte Export-Historie mit Zeitstempel und Objektinformationen

🛠️ Hinweise

    Blender arbeitet intern in Metern – für 3D‑Druck ist meist Millimeter erforderlich

    STL‑Dateien in Millimeter → nutze die automatische Erkennung oder Custom Scale = 1000

    Bei Problemen mit zu kleinen Objekten: Szene-Einheit auf Millimeter stellen oder Skalierung aktivieren

👤 Autor

Entwickelt von Andreas Papesch (AndyZ) & Copilot

