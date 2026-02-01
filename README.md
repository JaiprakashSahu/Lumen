# Lumen - Personal Finance Management System

A comprehensive personal finance management system built with Flask that helps you track expenses, analyze spending patterns, and get AI-powered financial insights.

## Features

- 📧 **Gmail Integration**: Automatically sync and extract transaction data from emails
- 📸 **Receipt OCR**: Upload and process receipts using NVIDIA OCR API
- 📊 **Analytics Dashboard**: Interactive charts and spending analysis
- 🤖 **AI-Powered Insights**: Get intelligent financial advice and anomaly detection
- 🛍️ **Smart Wishlist**: AI advisor for purchase decisions
- 🔍 **Transaction Search**: Advanced filtering and categorization
- 📱 **Responsive Design**: Modern, mobile-friendly interface

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **AI/ML**: NVIDIA OCR API, Groq LLM, Local LLM support
- **Database**: SQLite (easily configurable for other databases)
- **APIs**: Gmail API, NVIDIA API, Groq API

## Setup

### Prerequisites

- Python 3.8+
- Gmail API credentials (for email sync)
- NVIDIA API key (for OCR)
- Groq API key (for AI features)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jaiprakashsahu058-blip/Lumen.git
cd Lumen
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
cd project
pip install -r requirements.txt
pip install -r requirements_analytics.txt  # For advanced analytics
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Set up Google Gmail API:
   - Go to Google Cloud Console
   - Create a new project or select existing
   - Enable Gmail API
   - Create credentials (OAuth 2.0)
   - Download the credentials file as `client_secret.json`

6. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Configuration

Create a `.env` file in the `project/` directory with the following variables:

```env
FLASK_SECRET_KEY=your_secret_key_here
GOOGLE_CLIENT_SECRET_FILE=client_secret.json
GOOGLE_SCOPES=https://www.googleapis.com/auth/gmail.readonly
NVIDIA_API_KEY=your_nvidia_api_key
GROQ_API_KEY=your_groq_api_key
AI_PROVIDER=groq
LLM_PROVIDER=groq
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TIMEOUT=30
```

## Project Structure

```
Lumen/
├── project/
│   ├── app.py              # Main Flask application
│   ├── modules/            # Core modules
│   │   ├── analytics/      # Analytics and insights
│   │   ├── database/       # Database models and repositories
│   │   ├── llm/           # LLM integrations
│   │   ├── llm_extraction/ # Transaction extraction
│   │   ├── mcp/           # MCP server functionality
│   │   └── wishlist/      # AI wishlist advisor
│   ├── static/            # CSS, JS, images
│   ├── templates/         # HTML templates
│   └── uploads/           # File uploads (receipts)
├── .gitignore
└── README.md
```

## Usage

### Adding Transactions

1. **Manual Entry**: Use the dashboard to add transactions manually
2. **Gmail Sync**: Connect your Gmail account to automatically import transaction emails
3. **Receipt Upload**: Upload receipt images for automatic OCR extraction

### Analytics

- View spending patterns by category, time period
- Identify unusual transactions and potential anomalies
- Get AI-powered insights and recommendations

### Wishlist Management

- Add items to your wishlist
- Get AI advice on whether to make purchases
- Track price trends and deals

## API Keys Setup

### NVIDIA OCR API
1. Visit [NVIDIA NGC](https://ngc.nvidia.com/)
2. Create an account and generate an API key
3. Add to your `.env` file

### Groq API
1. Visit [Groq](https://groq.com/)
2. Sign up and get your API key
3. Add to your `.env` file

### Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Download the JSON file as `client_secret.json`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NVIDIA for OCR API
- Groq for LLM services
- Google for Gmail API
- Chart.js for beautiful charts
- Flask community for the amazing framework