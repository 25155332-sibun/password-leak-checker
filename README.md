# 🔒 Password Leak Checker & Strength Analyzer

A secure, privacy-focused web application built with **Python**, **Flask**, and **SQLite** that allows users to check if their passwords have been exposed in data breaches without ever risking their plain-text credentials[cite: 1].

## 🚀 Key Features
* **k-Anonymity Privacy Model**: Uses the HaveIBeenPwned range API, hashing passwords with SHA-1 and sending only the first 5 characters so the actual password is never transmitted or exposed.
* **Advanced Password Strength Analyzer**: Evaluates length and character complexity (uppercase, lowercase, numbers, symbols) to score passwords accurately.
* **Secure Search History**: Logs past lookups in a local SQLite database with automatic privacy masking.
* **Modern UI**: Clean, responsive frontend styled with Bootstrap 5.

## 🛠️ Tech Stack
* **Backend**: Python, Flask[cite: 1]
* **Database**: SQLite[cite: 1]
* **API**: HaveIBeenPwned Passwords Range API[cite: 1]
* **Frontend**: HTML5, Bootstrap 5

## ⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/password-leak-checker.git](https://github.com/your-username/password-leak-checker.git)
   cd password-leak-checker