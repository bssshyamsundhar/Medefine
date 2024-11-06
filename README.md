# Medefine

The **Medefine** web application is a comprehensive and interactive tool designed to help users quickly search for and understand medical terms. With an intuitive search function, users can find definitions, view related terms, pronunciations with audio,  and manage a favorites list for easy reference. This project uses the Merriam-Webster API to fetch more than 60000 medical terms and their definitions and is built with Flask and includes a simple and clean user interface.



## Features

- **Search Functionality**: Type any medical term to get a quick, clear definition.
- **Favorites Management**: Save frequently used terms to a favorites list for easy access.
- **Interactive Design**: Responsive search input with icons, making it easy to navigate.
- **Term Pronunciation**:Users can hear the correct pronunciation, making it easier for them to understand and remember the terms.
- **Comprehensive Dictionary**: Contains a large number of medical terms and definitions for user reference.


## Technologies Used

- **Frontend**: HTML, CSS . 
- **Backend**: Flask,Python,Merriam-Webster API


## Screenshots

### Home Page
![Home Page Screenshot](https://raw.githubusercontent.com/bssshyamsundhar/Medefine/master/screenshots/home_page.png)

### Search Functionality
![Result Page Screenshot](https://github.com/bssshyamsundhar/Medefine/blob/master/screenshots/result_page.png)

### Favorites Page
![Favorites Page Screenshot](https://github.com/bssshyamsundhar/Medefine/blob/master/screenshots/favorites_page.png)


## Installation and Running the App

To get started, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bssshyamsundhar/Medefine.git
   cd Medefine

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
    python3 -m venv venv
    source venv\Scripts\activate # On Linux, use `venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Run the app**:
   ```bash
   py -m app.py

5. **Access the app: Open a browser and go to http://127.0.0.1:5000 to start using the Medical Dictionary app.**


## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. All contributions are welcome!


## License
This project is open-source and available under the MIT License.
