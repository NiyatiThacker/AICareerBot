# 🎯 AI-Powered Career Chatbot

An interactive chatbot that helps users discover career paths based on their interests using rule-based NLP and intent detection.

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![NLTK](https://img.shields.io/badge/NLTK-3.9.1-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46.1-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **🧠 Intent Detection**: Identifies career interests from natural language using keyword and fuzzy matching
- **😊 Emotion Recognition**: Detects confusion or uncertainty and provides supportive responses
- **🎨 Fusion Domains**: Supports interdisciplinary careers like "arts + tech" → Creative Technology
- **📊 Career Guidance**: Provides detailed skills, roadmaps, and entry-level requirements for 60+ domains
- **💻 Interactive UI**: Modern Streamlit interface with emojis, dropdowns, and real-time chat
- **🔄 Session Management**: Maintains conversation flow with restart functionality

## 🛠 Tech Stack

- **Python 3.9** - Core application development
- **NLTK** - Text preprocessing, tokenization, and lemmatization
- **Difflib** - Fuzzy string matching for flexible input handling
- **Streamlit** - Web-based user interface
- **Custom Data Structure** - Structured career and domain information

## 📁 Project Structure

```
ai-career-chatbot/
├── app.py                      # Main Streamlit application
├── chat_engine.py              # Chatbot logic and response generation
├── nlp_engine.py              # NLP preprocessing and intent detection
├── intents_data_enhanced.py   # Structured career domain database
├── career_logic.py            # Career recommendation logic
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## 🚀 Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-career-chatbot.git
   cd ai-career-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** at `http://localhost:8501`

## 📸 Screenshots

### Main Interface
<img width="1905" height="921" alt="image" src="https://github.com/user-attachments/assets/1d0a1ee2-969e-43a3-bdd6-7082e697fb35" />


### Career Recommendations
<img width="1640" height="857" alt="image" src="https://github.com/user-attachments/assets/1208f8db-9694-4bd4-bf16-f8bd401be444" />
<img width="1685" height="658" alt="image" src="https://github.com/user-attachments/assets/6e3836f1-f5ac-485d-a4be-93cee0d4b3c4" />
<img width="1674" height="794" alt="image" src="https://github.com/user-attachments/assets/a34d84f9-22e2-4e96-825a-ff3df714fc43" />
<img width="1821" height="855" alt="image" src="https://github.com/user-attachments/assets/3a3e1670-56b3-4406-9625-961432b9c6c8" />


## 💡 Example Use Case

```
User: "I love coding and creating digital art"

Bot: ✅ Based on your interests, I found these domains:
     1. 🧑‍💻 Tech
     2. 🎨 Arts  
     3. ⚡ Creative-Tech (Fusion)

User: "Creative-Tech"

Bot: 🎓 Career paths under Creative-Tech:
     • Creative Technologist
     • Game Developer
     • AR/VR Designer
     • Interactive Media Artist
     
     Choose one for detailed skills and roadmap!
```

## 🔧 How It Works

1. **Input Processing**: User input is tokenized, lemmatized, and cleaned using NLTK
2. **Intent Detection**: Keywords are matched against 60+ predefined career domains using fuzzy matching
3. **Fusion Analysis**: Multiple detected interests are combined into interdisciplinary paths
4. **Career Recommendation**: Relevant careers are suggested with detailed information
5. **Interactive Response**: Users can explore skills, roadmaps, and learning resources

## 🚀 Future Enhancements

- [ ] **ML Integration**: Replace rule-based intent detection with BERT or SVM classifiers
- [ ] **Sentiment Analysis**: Advanced emotion detection using transformer models
- [ ] **Session Memory**: Add conversation history and user preference tracking
- [ ] **Cloud Deployment**: Deploy on Hugging Face Spaces or Streamlit Community Cloud
- [ ] **Multilingual Support**: Expand to regional languages for broader accessibility
- [ ] **Real-time Data**: Integration with job market APIs for current trends

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Niyati Thacker**
- GitHub: [@NiyatiThacker](https://github.com/NiyatiThacker)
- LinkedIn: [Niyati Thacker](https://linkedin.com/in/Niyati-Thacker)

---

⭐ **Star this repository if it helped you!**
