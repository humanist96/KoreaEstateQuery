# K-RealEstate AI Search System 🏠

An advanced AI-driven platform designed to analyze and present insights from Korean real estate market data. This project integrates web crawling, natural language processing, and interactive data visualization, enabling users to explore property data with ease and precision.

## 🎯 Key Features

### 1. Data Collection
- Automated web crawling from [Naver Real Estate](https://land.naver.com/) using **Crawl4AI**
- Real-time data updates for accurate market insights
- Seamless integration of multiple data sources

### 2. AI-Powered Analysis
- Natural language processing (NLP) with **OpenAI API**
- Structured data handling and processing using **PandasAI**
- Intelligent query interpretation and personalized responses

### 3. Interactive Visualization
- Data visualization with versatile chart types:
  - Bar charts
  - Scatter plots
  - Pie charts
  - Donut charts
- Customizable data preprocessing options
- User-friendly interface powered by **Streamlit**

## 🚀 Getting Started

### Prerequisites
Ensure the following tools are installed:
```bash
python >= 3.9
pip
virtualenv (recommended)
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/tjwodud04/KoreaEstateQuery.git
cd KoreaEstateQuery
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the project root with the following content:
```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### Running the Application

Launch the platform using the following command:
```bash
streamlit run Home.py
```

## 📁 Project Structure

```
k-realestate-ai-assistant/
├── analysis/
│   ├── PandasAI_Analysis.py          # Data Analysis function
├── gathering_data/
│   ├── classes.py
│   ├── data_gatherer.py               # Data Collecting function
│   └── util.py
├── web/
│   ├──pages/
│      ├── Estate_Search.py            # Property search interface
│      └── Raw_Data_Visualization.py # Data visualization tools
│   └──Home.py                         # Main landing page
├── example.env                          # Necessary API Setting
├── requirements.txt                     # Project dependencies
└── README.md                          # Project documentation
```

## 🔧 Technology Stack

- **Web**: Streamlit
- **Data Collection**: Crawl4AI
- **AI Processing**: OpenAI API
- **Data Analysis**: PandasAI
- **Visualization**: Plotly

## 📊 Data Sources

- [Naver Real Estate](https://land.naver.com/)


## 📜 License

This project is licensed under the Apache-2.0 license. See the [LICENSE](LICENSE) file for more information.

## 🙏 Acknowledgments

- **OpenAI API**
- **Streamlit** for the web development framework
- **[Crawl4AI](https://github.com/unclecode/crawl4ai)** for robust data crawling capabilities
- **[NaverRealEstateHavester](https://github.com/ByungJin-Lee/NaverRealEstateHavester/tree/master)** for collecting data
- All contributors and users of this project
