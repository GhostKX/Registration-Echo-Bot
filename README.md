# Telegram Registration Bot

A **Python-based Telegram bot** that **registers and manages staff members**. The bot allows users to register new staff members, delete existing ones, and ensures secure user interactions. It is built using the **PyTelegramBotAPI** library and utilizes **environment variables** to store the Telegram Bot API key securely.

## Features

### **Bot Management**
- **Staff Registration**: Users can register new staff members by entering details step by step.
- **Staff Deletion**: Allows users to delete staff members using a unique ID.
- **Environment Configuration**: The bot’s Telegram API key is managed using environment variables for enhanced security.

### **User Interaction**
- **Start Command (`/start`)**: Initiates interaction with the user and provides options for registration or deletion.
- **Step-by-step Registration**: The bot guides the user through entering their **first name, last name, email, and phone number**.
- **Phone Number Validation**: Ensures phone numbers start with `+998` and contain exactly 9 digits.
- **Error Handling**: Provides real-time error messages for incorrect inputs.
- **Secure Data Handling**: Uses a dictionary to store user data temporarily before adding it to the database.

### **Security**
- The bot’s API key is securely stored using environment variables, preventing accidental exposure.
- The bot does not permanently store user data, ensuring privacy.
- All messages unrelated to valid inputs are marked as "trash" and deleted automatically.

## Requirements

- **Python 3.8+**
- **PyTelegramBotAPI** (`pyTelegramBotAPI`)
- **python-dotenv** (to load environment variables)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/GhostKX/Registration-Echo-Bot.git
```

### 2. Navigate to the file
```
cd Registration-Echo-Bot
```

### 3. Install the required dependencies
```
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a .env file in the root directory and add your Telegram Bot API key:
```
API_KEY=Your-Telegram-API-Key
```

### 5. Run the bot
```
python PythonRegistrationEcho_bot.py
```

## Usage

The bot provides the following options:

- **Start Registration**: Press `📝 Register` to begin staff registration.  
- **Delete Staff**: Press `‼️ Delete` and enter a staff member’s unique ID.  
- **Cancel Registration**: Press `❌ Cancel` at any step to stop the process.  
- **Phone Number Entry**: Enter or share a valid phone number starting with `+998`.  


## Example Usage Scenario
```
User: /start

Bot: Hi, John! 

Do you want to register a new staff member, sir?

[📝 Register]  [‼️ Delete]
```

### Registration Process
```
User: 📝 Register
Bot: 💬 Please type in First Name 💬

User: Alex
Bot: 💬 Please type in your Last Name 💬

User: Johnson
Bot: 📩 Please type in Email address 📩

User: alex.johnson@email.com
Bot: 📞 Please share your contact 📞

User: [Shares contact]
Bot: 🎉 Congratulations, Alex Johnson! 🎉
Your registration is complete!
```

### Deleting a Staff Member
```
User: ‼️ Delete
Bot: 💬 Please type in staff unique ID 💬

User: ABC123
Bot: ❕❕Deleting Alex Johnson from database❕❕

[Loading...]
Bot: Successfully deleted ✅
```

### Dependencies

- **PyTelegramBotAPI**: The Python library used to interact with the Telegram Bot API.
- **python-dotenv**: A library to load environment variables from a `.env` file to keep the bot’s API key secure.
- **Database Module** (`database`): Handles storing and retrieving staff data.

## Author

- Developed by **GhostKX**
- GitHub: **[GhostKX](https://github.com/GhostKX/New-Echo-Bot)**


## Acknowledgments

- **PyTelegramBotAPI**: The Python library used to interact with the Telegram Bot API.
- **python-dotenv**: A Python library to load environment variables from a `.env` file.
