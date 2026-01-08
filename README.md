# 🔤 Multi-MT Term Comparison Tool
# 多引擎術語翻譯比較工具

Compare how different machine translation engines translate **terminology** across languages. See streaming results as each engine completes its translation.

比較不同機器翻譯引擎如何翻譯**專業術語**。即時串流顯示每個引擎的翻譯結果。

> 📚 **Designed for Terminology Management Courses 專為術語管理課程設計**

---

## ✨ Features 功能特色

- **🔄 8 MT Engines** - Compare translations from Google, Bing, Alibaba, Sogou, Youdao, Tencent, Lingvanex, and MyMemory
- **⚡ Streaming Results** - See translations appear in real-time as each engine completes
- **🌍 15+ Languages** - Support for English, Chinese (Simplified/Traditional), Japanese, Korean, and more
- **📊 Side-by-Side Comparison** - Visual comparison of all translations in one view
- **🏷️ Terminology Focus** - Pre-loaded examples from Medical, Legal, Finance, Tech, Environment, and Education domains
- **💻 Easy Setup** - One command to install and run

---

## 🚀 Quick Start 快速開始

### Option 1: Google Colab (Recommended 推薦)

No installation needed! Just run these 3 lines in a Colab notebook:

無需安裝！只需在 Colab 筆記本中運行以下 3 行：

```python
!git clone https://github.com/digimarketingai/multi-mt-term-tool.git
%cd multi-mt-term-tool
!python run.py
```

A public URL will be generated automatically. Click it to open the web interface.

系統將自動生成公開網址。點擊即可開啟網頁介面。

### Option 2: Local Installation 本地安裝

```bash
# Clone the repository 複製儲存庫
git clone https://github.com/digimarketingai/multi-mt-term-tool.git

# Enter the directory 進入目錄
cd multi-mt-term-tool

# Run the tool (auto-installs dependencies) 運行工具（自動安裝依賴）
python run.py
```

### Command Line Options 命令列選項

```bash
python run.py              # Start with public shareable link (default)
python run.py --local      # Local only (127.0.0.1, no public link)
python run.py --share      # Force public shareable link
python run.py --no-install # Skip automatic package installation
```

---

## 🔧 Available MT Engines 可用翻譯引擎

| Engine 引擎 | Provider 提供者 | Strengths 優勢 |
|-------------|----------------|----------------|
| 🔵 **Google Translate** 谷歌翻譯 | Google | Wide language coverage, general quality |
| 🟦 **Microsoft Bing** 微軟必應 | Microsoft | Good for European languages |
| 🟠 **Alibaba Translate** 阿里翻譯 | Alibaba | Strong for Chinese e-commerce terms |
| 🟡 **Sogou Translate** 搜狗翻譯 | Sogou/Tencent | Good for Chinese web content |
| 🔴 **Youdao Translate** 有道翻譯 | NetEase | Popular in China, good dictionaries |
| 🟢 **Tencent Translate** 騰訊翻譯 | Tencent | Strong for Chinese social media terms |
| 🟣 **Lingvanex** | Lingvanex | Alternative engine, good coverage |
| ⚪ **MyMemory** | MyMemory | Translation memory database |

---

## 🌍 Supported Languages 支援語言

| Code | Language 語言 |
|------|---------------|
| `en` | English |
| `zh-CN` | 简体中文 (Simplified Chinese) |
| `zh-TW` | 繁體中文 (Traditional Chinese) |
| `ja` | 日本語 (Japanese) |
| `ko` | 한국어 (Korean) |
| `es` | Español (Spanish) |
| `fr` | Français (French) |
| `de` | Deutsch (German) |
| `it` | Italiano (Italian) |
| `pt` | Português (Portuguese) |
| `ru` | Русский (Russian) |
| `ar` | العربية (Arabic) |
| `hi` | हिन्दी (Hindi) |
| `th` | ไทย (Thai) |
| `vi` | Tiếng Việt (Vietnamese) |

---

## 📚 Terminology Examples 術語範例

The tool includes pre-loaded examples from various domains. Click any term to instantly load it for comparison.

工具包含各領域的預設範例。點擊任意術語即可載入比較。

### 🏥 Medical & Health 醫療健康
| Chinese 中文 | English |
|--------------|---------|
| 衞生署衞生防護中心 | Centre for Health Protection |
| 基孔肯雅熱 | Chikungunya fever |
| 流行性感冒 | Influenza |
| 新型冠狀病毒 | Novel coronavirus |
| 世界衛生組織 | World Health Organization |

### ⚖️ Legal & Government 法律政府
| Chinese 中文 | English |
|--------------|---------|
| 立法會 | Legislative Council |
| 終審法院 | Court of Final Appeal |
| 司法覆核 | Judicial review |
| 基本法 | Basic Law |

### 💰 Finance & Business 財經商業
| Chinese 中文 | English |
|--------------|---------|
| 恒生指數 | Hang Seng Index |
| 首次公開募股 | Initial Public Offering (IPO) |
| 量化寬鬆 | Quantitative easing |
| 加密貨幣 | Cryptocurrency |

### 💻 Technology 科技
| Chinese 中文 | English |
|--------------|---------|
| 人工智能 | Artificial intelligence |
| 機器學習 | Machine learning |
| 雲端運算 | Cloud computing |
| 物聯網 | Internet of Things (IoT) |
| 大數據 | Big data |

### 🌍 Environment 環境
| Chinese 中文 | English |
|--------------|---------|
| 碳中和 | Carbon neutrality |
| 可再生能源 | Renewable energy |
| 溫室氣體 | Greenhouse gas |
| 生物多樣性 | Biodiversity |

### 📚 Education 教育
| Chinese 中文 | English |
|--------------|---------|
| 通識教育 | Liberal studies |
| 持續進修 | Continuing education |
| 學分轉移 | Credit transfer |
| 資歷架構 | Qualifications framework |

---

## 🎓 For Educators 教師使用指南

This tool is ideal for teaching terminology management concepts:

此工具非常適合教授術語管理概念：

### Classroom Activities 課堂活動

1. **Translation Variation Analysis 翻譯差異分析**
   - Compare how different engines translate the same term
   - Discuss which translation is most appropriate for specific contexts
   - 比較不同引擎如何翻譯同一術語
   - 討論哪種翻譯最適合特定語境

2. **Domain-Specific Terminology 領域專業術語**
   - Use terms from specific domains (medical, legal, etc.)
   - Analyze which engines perform better for specialized content
   - 使用特定領域的術語（醫療、法律等）
   - 分析哪些引擎對專業內容表現較佳

3. **Consistency Evaluation 一致性評估**
   - Test similar terms to see if engines provide consistent translations
   - Discuss importance of terminology consistency in professional translation
   - 測試相似術語，查看引擎是否提供一致的翻譯
   - 討論術語一致性在專業翻譯中的重要性

4. **Error Analysis 錯誤分析**
   - Identify mistranslations and discuss why they occur
   - Learn to spot common MT errors
   - 識別誤譯並討論其原因
   - 學習辨識常見的機器翻譯錯誤

---

## 📋 Requirements 系統需求

- **Python**: 3.8 or higher
- **Internet**: Required for MT API access
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

### Dependencies 依賴套件

These are installed automatically when you run the tool:

運行工具時會自動安裝：

```
deep-translator>=1.11.4
translators>=5.8.9
gradio>=4.0.0
```

---

## 🔧 Troubleshooting 疑難排解

### Common Issues 常見問題

**❌ "No translation engines available"**
- Check your internet connection
- Some engines may be temporarily unavailable
- Try running again after a few minutes

**❌ "Translation returned unchanged source text"**
- The engine may not support the language pair
- Try a different engine or language combination

**❌ "ModuleNotFoundError"**
- Run with auto-install: `python run.py`
- Or manually install: `pip install -r requirements.txt`

**❌ Gradio interface not loading**
- Check if port 7860 is available
- Try: `python run.py --local`

### For Colab Users Colab 使用者

If you encounter issues:
```python
# Restart runtime and run again
!pip install --upgrade gradio deep-translator translators
!python run.py
```

---

## 📁 Project Structure 專案結構

```
multi-mt-term-tool/
├── README.md           # This file 本文件
├── requirements.txt    # Python dependencies 依賴套件
├── run.py             # Launcher script 啟動腳本
└── mt_term_tool.py    # Main module 主模組
```

---

## 🤝 Contributing 貢獻

Contributions are welcome! Feel free to:

歡迎貢獻！您可以：

- Report bugs 回報錯誤
- Suggest new features 建議新功能
- Add more terminology examples 新增更多術語範例
- Improve documentation 改進文檔

---

## 📄 License 授權

MIT License

---

## 🙏 Acknowledgments 致謝

- [Gradio](https://gradio.app/) - Web interface framework
- [deep-translator](https://github.com/nidhaloff/deep-translator) - Translation library
- [translators](https://github.com/UlionTse/translators) - Multi-engine translation library

---
