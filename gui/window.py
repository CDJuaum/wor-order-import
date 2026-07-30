from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("WhatsApp Excel Importer")
        self.resize(520, 530)

        self.create_widgets()
        self.create_layout()
        self.apply_style()


    def create_widgets(self):

        self.title = QLabel("New service detected")

        # Top fields
        self.date = QLineEdit()
        self.hour = QLineEdit()

        self.service = QLineEdit()
        self.tag = QLineEdit()

        self.address = QTextEdit()
        self.address.setFixedHeight(80)
        self.address.setPlaceholderText("Service address...")

        self.client = QLineEdit()
        self.phone = QLineEdit()

        # Warnings
        self.warnings = QTextEdit()
        self.warnings.setReadOnly(True)
        self.warnings.setFixedHeight(45)
        self.warnings.setText("No warnings")

        self.warnings.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
            }
        """)

        # Auto import
        self.auto_import = QCheckBox(
            "Auto import valid services"
        )

        self.auto_import.setToolTip(
            "Automatically imports services that pass validation without asking for confirmation."
        )

        # Buttons
        self.cancel_button = QPushButton("Cancel")
        self.import_button = QPushButton("Import")

        self.import_button.setObjectName("ImportButton")


    def create_layout(self):

        main_layout = QVBoxLayout()


        main_layout.addWidget(self.title)


        # Date / Hour

        date_hour = QHBoxLayout()

        date_box = QVBoxLayout()
        date_box.addWidget(QLabel("Date"))
        date_box.addWidget(self.date)

        hour_box = QVBoxLayout()
        hour_box.addWidget(QLabel("Hour"))
        hour_box.addWidget(self.hour)

        date_hour.addLayout(date_box)
        date_hour.addLayout(hour_box)

        main_layout.addLayout(date_hour)


        # Service / Tag

        service_tag = QHBoxLayout()

        service_box = QVBoxLayout()
        service_box.addWidget(QLabel("Service"))
        service_box.addWidget(self.service)

        tag_box = QVBoxLayout()
        tag_box.addWidget(QLabel("Tag"))
        tag_box.addWidget(self.tag)

        service_tag.addLayout(service_box, 3)
        service_tag.addLayout(tag_box, 1)

        main_layout.addLayout(service_tag)


        # Address

        main_layout.addWidget(
            QLabel("Address")
        )

        main_layout.addWidget(
            self.address
        )


        # Client / Phone

        client_phone = QHBoxLayout()

        client_box = QVBoxLayout()
        client_box.addWidget(QLabel("Client"))
        client_box.addWidget(self.client)

        phone_box = QVBoxLayout()
        phone_box.addWidget(QLabel("Phone"))
        phone_box.addWidget(self.phone)

        client_phone.addLayout(client_box, 3)
        client_phone.addLayout(phone_box, 2)

        main_layout.addLayout(client_phone)


        # Separator

        warning_group = QGroupBox(
            "Warnings / Errors"
        )

        warning_layout = QVBoxLayout()
        warning_layout.addWidget(self.warnings)

        warning_group.setLayout(
            warning_layout
        )

        main_layout.addWidget(
            warning_group
        )

        main_layout.setStretchFactor(
            warning_group,
            0
        )

        # Auto import

        main_layout.addWidget(
            self.auto_import
        )

        main_layout.addStretch()


        # Buttons

        buttons = QHBoxLayout()

        buttons.addWidget(
            self.cancel_button
        )

        buttons.addWidget(
            self.import_button
        )

        main_layout.addLayout(
            buttons
        )


        self.setLayout(main_layout)


    def apply_style(self):

        self.setStyleSheet("""
            QWidget {
                font-size: 12px;
            }

            QLineEdit, QTextEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 6px;
            }

            QPushButton {
                padding: 8px;
                border-radius: 6px;
            }

            QPushButton:hover {
                font-weight: bold;
            }

            QPushButton#ImportButton {
                background-color: #2d89ef;
                color: white;
            }

            QPushButton#ImportButton:hover {
                background-color: #1b6ec2;
            }

            QGroupBox {
                margin-top: 10px;
                padding-top: 10px;
            }
        """)