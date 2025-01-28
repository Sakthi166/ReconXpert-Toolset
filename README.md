

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
    git clone https://github.com/your-username/ReconXpert-WebTool.git
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

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.



---

Feel free to adjust the content according to your project specifics!
