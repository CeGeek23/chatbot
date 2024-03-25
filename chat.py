import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QAction, QFileDialog, QScrollArea, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QFile

class ChatBotWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        
    def initUI(self):
        self.setWindowTitle("The Maintainer App")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(600, 350, 800, 900)

        # Charger les styles CSS à partir du fichier styles.css
        style_file = QFile("styles.css")
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = style_file.readAll().data().decode("utf-8")
            style_file.close()

        # Création de la zone de texte pour l'entrée de l'utilisateur
        self.input_edit = QTextEdit()
        self.input_edit.setMaximumHeight(120)
        self.input_edit.setStyleSheet(style_sheet)

        # Création du bouton d'envoi
        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setObjectName("send_button")
        self.send_button.setShortcut("Ctrl+Return")
        self.send_button.setStyleSheet(style_sheet)

        # Création du bouton pour effacer la conversation
        self.clear_button = QPushButton("Effacer")
        self.clear_button.clicked.connect(self.clear_message)
        self.clear_button.setObjectName("clear_button")
        self.clear_button.setShortcut("Ctrl+x")
        self.clear_button.setStyleSheet(style_sheet)

        # Création de l'action "Ouvrir" dans la barre de menu
        open_action = QAction(QIcon("open.png"), "Ouvrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        # Création de l'action "Sauvegarder" dans la barre de menu
        save_action = QAction(QIcon(""), "Sauvegarder", self)
        save_action.setShortcut("Ctrl+s")
        save_action.triggered.connect(self.save_conversation)

        # Création des actions pour le thème jour et nuit
        day_theme_action = QAction(QIcon(), "Thème Jour", self)
        day_theme_action.triggered.connect(self.set_day_theme)

        night_theme_action = QAction(QIcon(), "Thème Nuit", self)
        night_theme_action.triggered.connect(self.set_night_theme)

        # Création de la barre de menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Options")
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(day_theme_action)
        file_menu.addAction(night_theme_action)

        # Création du layout vertical pour organiser les widgets
        vbox = QVBoxLayout()

        # Création d'un widget pour afficher les messages dans une zone déroulante
        self.message_widget = QWidget()
        self.message_layout = QVBoxLayout()
        self.message_widget.setLayout(self.message_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.message_widget)

        vbox.addWidget(scroll_area)
        vbox.addWidget(self.input_edit)

        hbox = QHBoxLayout()
        hbox.addWidget(self.send_button)
        hbox.addWidget(self.clear_button)

        vbox.addLayout(hbox)

        # Création du widget principal et assignation du layout
        main_widget = QWidget()
        main_widget.setLayout(vbox)
        self.setCentralWidget(main_widget)

    def send_message(self):

        user_input = self.input_edit.toPlainText()
        self.display_message(f"Utilisateur: {user_input}", "#075E54")
        self.bot_response = self.get_bot_response(user_input)
        self.current_char = 0
        self.input_edit.clear()
        self.bot_message_label = QLabel()
        self.bot_message_label.setStyleSheet("styles.css")
        self.bot_message_label.setWordWrap(True)

        # Ajouter le widget QLabel du message du bot à la layout
        self.message_layout.addWidget(self.bot_message_label)

        # Démarrer le QTimer pour afficher la réponse du chatbot caractère par caractère
        self.timer.singleShot(100, self.display_bot_response)

    def display_message(self, message, color):
        # Création d'un widget QLabel pour afficher le message dans une bulle
        message_label = QLabel(message)
        message_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
                font-size: 12px;
                color: white;
                max-height: 30px;
                font-size : 20px;
                font-family : Helvetica;
            }}
        """)
        message_label.setWordWrap(True)

        # Ajout du widget QLabel au layout
        self.message_layout.addWidget(message_label)

        # Défilement vers le bas pour afficher le dernier message
        scroll_area = self.message_widget.parentWidget()

    def display_bot_response(self):
        if self.current_char >= len(self.bot_response):
            # Arrêter le QTimer
            self.timer.stop()
            # Faire défiler vers le bas pour afficher le dernier message
            scroll_area = self.message_widget.parentWidget()
            return

        # Afficher les caractères un par un avec un délai de 100 ms
        self.bot_message_label.setText(self.bot_response[:self.current_char + 1])
        self.current_char += 1

        # Défilement vers le bas pour afficher le dernier message
        scroll_area = self.message_widget.parentWidget()

        # Démarrer le QTimer pour afficher le caractère suivant après un délai
        self.timer.singleShot(100, self.display_bot_response)

    def get_bot_response(self, user_input):
        # Implémentez ici votre logique pour interagir avec votre système expert
        # et obtenir la réponse du chatbot
        # Remplacez cette ligne par l'appel à votre système expert
        return "Ceci est la réponse du ChatBot."

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Ouvrir un fichier", "", "Fichiers texte (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.input_edit.setPlainText(file_content)

    def save_conversation(self):
        # Ouvrir une boîte de dialogue pour sélectionner l'emplacement de sauvegarde du fichier
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Sauvegarder la conversation", "", "Fichiers texte (*.txt)")

        if file_path:
            # Récupérer le contenu de tous les messages affichés
            conversation = ""
            for i in range(self.message_layout.count()):
                message_widget = self.message_layout.itemAt(i).widget()
                if isinstance(message_widget, QLabel):
                    message_text = message_widget.text()
                    conversation += message_text + "\n"

            # Sauvegarder la conversation dans le fichier
            with open(file_path, "w") as file:
                file.write(conversation)
        return("conversation saved")

    def set_day_theme(self):
        # Changer le thème de l'application pour le thème jour
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QLabel {
                background-color: #075E54;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #25D366;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 8px;
                font-size: 12px;
            }
        """)

    def set_night_theme(self):
        # Changer le thème de l'application pour le thème nuit
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222222;
            }
            QLabel {
                background-color: #DCF8C6;
                color: black;
                border-radius: 10px;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #25D366;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
            QTextEdit {
                background-color: #333333;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 8px;
                font-size: 12px;
            }
        """)

    def clear_message(self) :
        # Effacer tous les messages affichés
        for i in reversed(range(self.message_layout.count())):
            self.message_layout.itemAt(i).widget().deleteLater()
            print(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatBotWindow()
    window.show()
    sys.exit(app.exec_())