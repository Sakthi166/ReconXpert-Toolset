

# ReconXpert-Toolset

**ReconXpert-Toolset** is a comprehensive, web-based reconnaissance and penetration testing platform. It integrates multiple cybersecurity tools to help security professionals and enthusiasts assess and test the security of their targets.

## Features

- **Web Interface:** Intuitive interface to interact with various penetration testing tools.
- **Tool Integration:** Supports tools like Nmap, Hydra, WPScan, Gobuster, Nikto, and more.
- **Scan Options:** Perform reconnaissance, scanning, enumeration, vulnerability testing, and more.
- **Results Reporting:** Automatically generates detailed reports in PDF format.
- **Secure Login:** User authentication with OTP verification for secure access.

## Tools Included

- **Nmap**
- **Hydra**
- **WPScan**
- **Gobuster**
- **Nikto**
- **Sublist3r**
- **TheHarvester**
- **And more...**

## Installation

### Prerequisites

1. Python 3.x
2. Flask
3. Firebase Admin SDK
4. ReportLab

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/Sakthi166/ReconXpert-Toolset.git
    cd ReconXpert-WebTool
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Firebase:
   - Create a Firebase project and download the credentials file.
   - Initialize Firebase in your app with the credentials.

4. Run the application:
    ```bash
    python app.py
    ```

5. Access the application at `http://127.0.0.1:5000`.

## Usage

- **Registration:** Users can register by providing their email and password.
- **Login:** Secure login using email and OTP.
- **Scanning & Analysis:** Choose a tool from the list, provide the target URL, and initiate the scan.
- **Report Generation:** After scanning, download a PDF report of the results.

## Remember

- In index.js you need to replace the Firebase configuration in your code with your own config details:
  ```bash
  const firebaseConfig = {
  apiKey: "<YOUR_API_KEY>",
  authDomain: "<YOUR_AUTH_DOMAIN>",
  databaseURL: "<YOUR_DATABASE_URL>",
  projectId: "<YOUR_PROJECT_ID>",
  storageBucket: "<YOUR_STORAGE_BUCKET>",
  messagingSenderId: "<YOUR_MESSAGING_SENDER_ID>",
  appId: "<YOUR_APP_ID>" };
    ```
- In contact.html you need to replace the w3forms access-key configuration in:
 ```bash
  name="access_key" value="<your_access_key>">
  ```

