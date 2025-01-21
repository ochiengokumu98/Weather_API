import sys
import requests
from PyQt5.QtWidgets import (QApplication, QLabel,
                             QVBoxLayout, QWidget,
                             QLineEdit, QPushButton)  
from PyQt5.QtCore import Qt
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Widgets
        self.city_label = QLabel("Enter the name of the city:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        #self.temperature_label = QLabel("70℉", self)
        #self.emoji_label = QLabel("☀️", self)
        #self.description_label = QLabel("Sunny", self)

        # Initialize UI
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle("Weather App")

        # Set up layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.temperature_label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.emoji_label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.description_label, alignment=Qt.AlignCenter)
        vbox.setSpacing(15)
        vbox.setContentsMargins(20, 20, 20, 20)
        
         # Assigning object names for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Apply the layout
        self.setLayout(vbox)

        # Styling
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 30px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #45a049;
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: "Segoe UI Emoji";
            }
            QLabel#description_label {
                font-size: 50px;
            }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)   
     
        # Connect the button to the function     
    def get_weather(self):
        api_key="71e6763f3d3e6a966fc3df847e0639ef"
        city= self.city_input.text()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data=response.json()
        
            #print(data)
            if data["cod"] == 200:
                self.display_weather(data)
                
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input.")
                    #print("Bad request\nPlease check your input.") 
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key.")
                    #print("Unauthorized\nInvalid API Key.") 
                case 403:
                    self.display_error("Forbidden:\nAccess is denied.")
                    #print("Forbidden\nAccess is denied.") 
                case 404:
                    self.display_error("Not found:\nCity not found.")
                    #print("Not found\nCity not found.") 
                case 500:
                    self.display_error("Internal server error:\nTry again later.")
                    #print("Internal server error\nTry again later.") 
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server.")
                    #print("Bad Gateway\nInvalid response from the server.") 
                case 503:
                    self.display_error("Service unavailble:\nServer is down.")
                    #print("Service unavailble\nServer is down.") 
                case 504:
                    self.display_error("Gateway timeout:\nNo response from the server.") 
                    #print("Gateway timeout\nNo response from the server.") 
                case _:
                    self.display_error("HTTP Error occurred")   
                     #print(f"HTTP Error occurred:\n{http_error}")
         
        except requests.exceptions.ConnectionError:
            self.display_error("A connection error occurred:\nPlease check your internet connection.")
            #print("A connection error occurred\nPlease check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("The request timed out:\nPlease try again.")
            #print("The request timed out\nPlease try again:")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the url.")
            #print("Too many redirects\n Check the url.")   
        except requests.exceptions.RequestException as req_error:
            self.display_error("An error occurred")
            #print(f"An error occurred:\n{req_error}")
        
            # self.display_error("HTTP Error occurred")
    
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        

    def display_weather(self, data):
        #print (data)
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        #print(temperature_k)
        temperature_c = temperature_k - 273.15
        temperature_f = temperature_k * 9/5 - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description=data["weather"][0]["description"]
        #print(temperature_c)
        #print(data)
        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        #print(data["weather"])

    @staticmethod
    def get_weather_emoji(weather_id):
    
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🌬️"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
