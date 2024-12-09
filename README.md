# K-RealEstate AI Assistant 🏠

An intelligent real estate data analysis platform that leverages AI to provide insights from Korean property market data. This project combines web crawling, natural language processing, and interactive data visualization to make property data more accessible and understandable.

## 🎯 Features

### 1. Data Collection
- Automated crawling from Naver Real Estate using Crawl4AI
- Real-time data updates
- Multiple data source integration

### 2. AI-Powered Analysis
- Natural language processing using OpenAI API
- Structured data processing with PandasAI
- Intelligent query interpretation and response

### 3. Interactive Visualization
- Raw data visualization with multiple chart types:
  - Bar charts
  - Scatter plots
  - Pie charts
  - Donut charts
- Customizable preprocessing options
- User-friendly interface built with Streamlit

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.8
pip
virtualenv (recommended)
```

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/k-realestate-ai-assistant.git
cd k-realestate-ai-assistant
```

2. Create and activate virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

3. Install required packages
```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_api_key_here
CRAWL4AI_API_KEY=your_api_key_here
```

2. Update the configuration in `config.py` if needed

### Running the Application

```bash
streamlit run Home.py
```

## 📁 Project Structure

```
k-realestate-ai-assistant/
├── Home.py                 # Main landing page
├── pages/
│   ├── property_search.py    # Property search interface
│   └── data_visualization.py # Data visualization tools
├── utils/
│   ├── crawling.py          # Crawling utilities
│   ├── preprocessing.py     # Data preprocessing functions
│   └── visualization.py     # Visualization helpers
├── config.py              # Configuration settings
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## 🛠 Technology Stack

- **Frontend**: Streamlit
- **Data Collection**: Crawl4AI
- **AI Processing**: OpenAI API
- **Data Analysis**: PandasAI, Pandas, Numpy
- **Visualization**: Plotly
- **Data Storage**: CSV, Excel support

## 📊 Data Sources

- Naver Real Estate
- Public Property Records
- Market Analysis Reports
- Regional Development Plans

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Your Name - youremail@example.com

Project Link: [https://github.com/yourusername/k-realestate-ai-assistant](https://github.com/yourusername/k-realestate-ai-assistant)

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Streamlit for the amazing web framework
- Crawl4AI for the crawling capabilities
- All contributors and users of this project
