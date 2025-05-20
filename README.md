# Text Summarization Flask Application

A web application for AI-powered text summarization using BART large CNN model.

## Project Structure

```
├── .env
├── config.py
├── init_db.py
├── README.md
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── filters.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── summarizer.py
│   └── templates/
│       ├── about.html
│       ├── base.html
│       ├── history.html
│       ├── index.html
│       ├── login.html
│       ├── profile.html
│       ├── register.html
│       └── summary.html
└── static/
    ├── css/
    │   └── style.css
    ├── img/
    │   └── favicon_instructions.txt
    └── js/
        └── script.js
```

## Features

- Summarize content from URLs or pasted text
- User authentication system
- Save summaries for registered users
- Customizable summary length
- View summary history
- Profile with summarization statistics
- Responsive design

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Transformers
- **Frontend**: Bootstrap 5, Font Awesome, JavaScript
- **AI Model**: BART large CNN (facebook/bart-large-cnn)
- **Database**: SQLite

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/text-summarization.git
   cd text-summarization
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with a secret key
   ```
   SECRET_KEY="your-secret-key"
   ```

5. Initialize the database
   ```bash
   python init_db.py
   ```

6. Run the application
   ```bash
   python run.py
   ```

7. Access the application at http://127.0.0.1:5000

## Usage

1. **Summarize Text**: Enter a URL or paste text directly
2. **Customize Length**: Adjust min/max length parameters
3. **Account**: Register/login to save your summaries
4. **History**: View your past summaries
5. **Profile**: See your summarization statistics

## Screenshots

![image](https://github.com/user-attachments/assets/aeccd8d1-6943-4617-8d02-69c30291d06c)
![image](https://github.com/user-attachments/assets/ac63c1e9-d480-4a6f-8032-756cd12d39c2)
![image](https://github.com/user-attachments/assets/1c627c4e-8ba4-4c21-9ae5-6c8737e4e0c8)
![image](https://github.com/user-attachments/assets/c5dcc148-cc03-4103-a411-9582ccfbf73f)
![image](https://github.com/user-attachments/assets/e8ae12e4-2ff1-4631-af3e-70cf57c591c0)



## AI Model

The application uses the BART large CNN model from Facebook/Meta AI, which was fine-tuned on CNN Daily Mail dataset for abstractive summarization. The model creates coherent, human-like summaries rather than simply extracting key sentences.

## License

MIT License
