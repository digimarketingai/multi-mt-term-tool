"""
🔤 Multi-MT Term Comparison Tool 多引擎術語翻譯比較工具
Compare terminology translations across multiple MT engines.
"""

import warnings
warnings.filterwarnings('ignore')

import time
import json
from typing import List, Generator
from dataclasses import dataclass

# ============================================================
# IMPORTS
# ============================================================

DEEP_TRANSLATOR_AVAILABLE = False
TRANSLATORS_AVAILABLE = False
GRADIO_AVAILABLE = False

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
    DEEP_TRANSLATOR_AVAILABLE = True
except ImportError:
    pass

try:
    import translators as ts
    TRANSLATORS_AVAILABLE = True
except ImportError:
    pass

try:
    import gradio as gr
    GRADIO_AVAILABLE = True
except ImportError:
    pass

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class TranslationResult:
    """Single translation result from one engine."""
    engine: str
    engine_zh: str
    source_lang: str
    target_lang: str
    source_text: str
    translated_text: str
    success: bool
    error_message: str = ""
    translation_time: float = 0.0
    status: str = "pending"

# ============================================================
# LANGUAGE CONFIGS
# ============================================================

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'zh-CN': '简体中文 (Simplified Chinese)',
    'zh-TW': '繁體中文 (Traditional Chinese)',
    'ja': '日本語 (Japanese)',
    'ko': '한국어 (Korean)',
    'es': 'Español (Spanish)',
    'fr': 'Français (French)',
    'de': 'Deutsch (German)',
    'it': 'Italiano (Italian)',
    'pt': 'Português (Portuguese)',
    'ru': 'Русский (Russian)',
    'ar': 'العربية (Arabic)',
    'hi': 'हिन्दी (Hindi)',
    'th': 'ไทย (Thai)',
    'vi': 'Tiếng Việt (Vietnamese)',
}

TRANSLATORS_LANG_MAP = {
    'zh-CN': 'zh', 'zh-TW': 'zh-TW', 'ja': 'ja', 'ko': 'ko', 'en': 'en',
    'es': 'es', 'fr': 'fr', 'de': 'de', 'it': 'it', 'pt': 'pt',
    'ru': 'ru', 'ar': 'ar', 'hi': 'hi', 'th': 'th', 'vi': 'vi',
}

MYMEMORY_LANG_MAP = {
    'en': 'en-GB', 'zh-TW': 'zh-TW', 'zh-CN': 'zh-CN', 'ja': 'ja-JP',
    'ko': 'ko-KR', 'es': 'es-ES', 'fr': 'fr-FR', 'de': 'de-DE',
    'it': 'it-IT', 'pt': 'pt-PT', 'ru': 'ru-RU', 'ar': 'ar-SA',
    'hi': 'hi-IN', 'th': 'th-TH', 'vi': 'vi-VN',
}

GOOGLE_LANG_MAP = {
    'zh-CN': 'zh-CN', 'zh-TW': 'zh-TW', 'ja': 'ja', 'ko': 'ko', 'en': 'en',
    'es': 'es', 'fr': 'fr', 'de': 'de', 'it': 'it', 'pt': 'pt',
    'ru': 'ru', 'ar': 'ar', 'hi': 'hi', 'th': 'th', 'vi': 'vi',
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def detect_language_simple(text: str) -> str:
    """Simple language detection based on character ranges."""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    japanese_chars = sum(1 for c in text if '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff')
    korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7af')
    
    total = len(text)
    if total == 0:
        return 'en'
    if japanese_chars > 0:
        return 'ja'
    if korean_chars / total > 0.1:
        return 'ko'
    if chinese_chars / total > 0.1:
        return 'zh-CN'
    return 'en'


def create_status_html(results: List[TranslationResult], current_engine: str = "") -> str:
    """Create HTML showing translation progress."""
    html = """
    <style>
        .mt-container { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        .mt-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 20px; border-radius: 10px 10px 0 0; margin-bottom: 0; }
        .mt-header h3 { margin: 0; font-size: 18px; }
        .mt-item { border: 1px solid #e0e0e0; border-top: none; padding: 15px 20px; background: white; transition: all 0.3s ease; }
        .mt-item:last-child { border-radius: 0 0 10px 10px; }
        .mt-item:hover { background: #f8f9fa; }
        .mt-item.running { background: #fff8e1; border-left: 4px solid #ffc107; animation: pulse 1.5s infinite; }
        .mt-item.success { background: #e8f5e9; border-left: 4px solid #4caf50; }
        .mt-item.error { background: #ffebee; border-left: 4px solid #f44336; }
        .mt-item.pending { background: #fafafa; border-left: 4px solid #9e9e9e; opacity: 0.7; }
        .engine-name { font-weight: 600; font-size: 15px; color: #333; display: flex; align-items: center; gap: 8px; }
        .engine-zh { color: #666; font-weight: normal; font-size: 13px; }
        .translation { margin-top: 10px; font-size: 15px; color: #1a1a1a; line-height: 1.6; padding: 10px; background: #f5f5f5; border-radius: 6px; }
        .translation.empty { color: #999; font-style: italic; }
        .meta { margin-top: 8px; font-size: 12px; color: #888; display: flex; gap: 15px; }
        .status-icon { font-size: 18px; }
        .spinner { display: inline-block; width: 18px; height: 18px; border: 2px solid #ffc107; border-radius: 50%; border-top-color: transparent; animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        .loading-banner { background: linear-gradient(90deg, #667eea, #764ba2, #667eea); background-size: 200% 100%; animation: shimmer 2s infinite; color: white; padding: 15px 20px; border-radius: 10px; margin-bottom: 15px; text-align: center; font-size: 16px; }
        @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
        .progress-text { font-size: 14px; margin-top: 5px; opacity: 0.9; }
    </style>
    """
    
    completed = sum(1 for r in results if r.status in ['success', 'error'])
    total = len(results)
    success_count = sum(1 for r in results if r.status == 'success')
    
    if current_engine:
        html += f"""
        <div class="loading-banner">
            <div>🔄 <strong>Translating Term... 術語翻譯中...</strong></div>
            <div class="progress-text">Processing: {current_engine} ({completed}/{total} completed)</div>
        </div>
        """
    elif completed > 0 and completed == total:
        html += f"""
        <div style="background: #4caf50; color: white; padding: 12px 20px; border-radius: 10px; margin-bottom: 15px; text-align: center;">
            ✅ <strong>Complete! 完成!</strong> {success_count}/{total} engines successful
        </div>
        """
    
    html += '<div class="mt-container">'
    html += '<div class="mt-header"><h3>📊 Term Translation Results 術語翻譯結果</h3></div>'
    
    for result in results:
        status_class = result.status
        if result.status == 'running':
            status_icon = '<span class="spinner"></span>'
        elif result.status == 'success':
            status_icon = '<span class="status-icon">✅</span>'
        elif result.status == 'error':
            status_icon = '<span class="status-icon">❌</span>'
        else:
            status_icon = '<span class="status-icon">⏳</span>'
        
        html += f'<div class="mt-item {status_class}">'
        html += f'<div class="engine-name">{status_icon} {result.engine} <span class="engine-zh">({result.engine_zh})</span></div>'
        
        if result.status == 'running':
            html += '<div class="translation empty">⏳ Translating... 翻譯中...</div>'
        elif result.status == 'success':
            html += f'<div class="translation">{result.translated_text}</div>'
            html += f'<div class="meta"><span>⏱️ {result.translation_time:.2f}s</span></div>'
        elif result.status == 'error':
            error_msg = result.error_message if result.error_message else "Service unavailable 服務暫時無法使用"
            html += f'<div class="translation empty">⚠️ {error_msg}</div>'
        else:
            html += '<div class="translation empty">Waiting... 等待中...</div>'
        
        html += '</div>'
    
    html += '</div>'
    return html

# ============================================================
# MAIN TRANSLATOR CLASS
# ============================================================

class MultiMTTranslator:
    """Multi-engine Machine Translation for Term Comparison."""
    
    def __init__(self, verbose: bool = True):
        self.engines = {}
        self.verbose = verbose
        self._init_engines()
    
    def _init_engines(self):
        """Initialize available translation engines."""
        if self.verbose:
            print("\n🔍 Initializing translation engines...")
        
        if DEEP_TRANSLATOR_AVAILABLE:
            self.engines["google"] = {
                "name": "Google Translate", "name_zh": "谷歌翻譯",
                "type": "deep_translator", "class": GoogleTranslator, "priority": 1
            }
            self.engines["mymemory"] = {
                "name": "MyMemory", "name_zh": "MyMemory 翻譯記憶庫",
                "type": "deep_translator", "class": MyMemoryTranslator, "priority": 8
            }
            if self.verbose:
                print("   ✅ Google Translate, MyMemory")
        
        if TRANSLATORS_AVAILABLE:
            engines_config = [
                ("bing", "Microsoft Bing", "微軟必應翻譯", "bing", 2),
                ("alibaba", "Alibaba Translate", "阿里翻譯", "alibaba", 3),
                ("sogou", "Sogou Translate", "搜狗翻譯", "sogou", 4),
                ("youdao", "Youdao Translate", "有道翻譯", "youdao", 5),
                ("tencent", "Tencent Translate", "騰訊翻譯", "qqTranSmart", 6),
                ("lingvanex", "Lingvanex", "Lingvanex 翻譯", "lingvanex", 7),
            ]
            for key, name, name_zh, engine_name, priority in engines_config:
                self.engines[key] = {
                    "name": name, "name_zh": name_zh,
                    "type": "translators", "engine_name": engine_name, "priority": priority
                }
            if self.verbose:
                print("   ✅ Bing, Alibaba, Sogou, Youdao, Tencent, Lingvanex")
        
        if self.verbose:
            print(f"\n📊 Total engines available: {len(self.engines)}")
    
    def get_available_engines(self) -> List[str]:
        return sorted(self.engines.keys(), key=lambda x: self.engines[x].get('priority', 99))
    
    def _translate_single(self, text: str, source: str, target: str, engine_name: str) -> TranslationResult:
        if engine_name not in self.engines:
            return TranslationResult(
                engine=engine_name, engine_zh=engine_name, source_lang=source,
                target_lang=target, source_text=text, translated_text="",
                success=False, error_message="Engine not found", status="error"
            )
        
        engine_info = self.engines[engine_name]
        start_time = time.time()
        
        try:
            if engine_info["type"] == "deep_translator":
                result = self._translate_deep_translator(text, source, target, engine_info)
            else:
                result = self._translate_translators(text, source, target, engine_info)
            
            result.translation_time = time.time() - start_time
            result.status = "success" if result.success else "error"
            return result
        except Exception as e:
            return TranslationResult(
                engine=engine_info["name"], engine_zh=engine_info["name_zh"],
                source_lang=source, target_lang=target, source_text=text,
                translated_text="", success=False, error_message=str(e)[:80],
                translation_time=time.time() - start_time, status="error"
            )
    
    def _translate_deep_translator(self, text: str, source: str, target: str, engine_info: dict) -> TranslationResult:
        engine_class = engine_info["class"]
        detected_source = detect_language_simple(text) if source == 'auto' else source
        
        if engine_class == MyMemoryTranslator:
            src = MYMEMORY_LANG_MAP.get(detected_source, detected_source)
            tgt = MYMEMORY_LANG_MAP.get(target, target)
            translator = engine_class(source=src, target=tgt)
        elif engine_class == GoogleTranslator:
            src = GOOGLE_LANG_MAP.get(detected_source, detected_source)
            tgt = GOOGLE_LANG_MAP.get(target, target)
            if source == 'auto' and detected_source.startswith('zh'):
                translator = GoogleTranslator(source=src, target=tgt)
            else:
                translator = GoogleTranslator(source=src if source != 'auto' else 'auto', target=tgt)
        else:
            translator = engine_class(source='auto' if source == 'auto' else source, target=target)
        
        result = translator.translate(text)
        
        if result and result.strip() == text.strip():
            if any('\u4e00' <= c <= '\u9fff' for c in text) and target == 'en':
                return TranslationResult(
                    engine=engine_info["name"], engine_zh=engine_info["name_zh"],
                    source_lang=source, target_lang=target, source_text=text,
                    translated_text="", success=False,
                    error_message="Translation returned unchanged source text", status="error"
                )
        
        return TranslationResult(
            engine=engine_info["name"], engine_zh=engine_info["name_zh"],
            source_lang=source, target_lang=target, source_text=text,
            translated_text=result if result else "", success=bool(result),
            status="success" if result else "error"
        )
    
    def _translate_translators(self, text: str, source: str, target: str, engine_info: dict) -> TranslationResult:
        engine_name = engine_info["engine_name"]
        detected_source = detect_language_simple(text) if source == 'auto' else source
        
        src = TRANSLATORS_LANG_MAP.get(detected_source, detected_source) if source != 'auto' else 'auto'
        if source == 'auto' and detected_source.startswith('zh'):
            src = TRANSLATORS_LANG_MAP.get(detected_source, 'zh')
        tgt = TRANSLATORS_LANG_MAP.get(target, target)
        
        result = ts.translate_text(
            query_text=text, translator=engine_name,
            from_language=src, to_language=tgt, timeout=15
        )
        translated = str(result) if result else ""
        
        if translated.strip() == text.strip():
            if any('\u4e00' <= c <= '\u9fff' for c in text) and target == 'en':
                return TranslationResult(
                    engine=engine_info["name"], engine_zh=engine_info["name_zh"],
                    source_lang=source, target_lang=target, source_text=text,
                    translated_text="", success=False,
                    error_message="Translation returned unchanged source text", status="error"
                )
        
        return TranslationResult(
            engine=engine_info["name"], engine_zh=engine_info["name_zh"],
            source_lang=source, target_lang=target, source_text=text,
            translated_text=translated, success=bool(translated),
            status="success" if translated else "error"
        )
    
    def translate_streaming(self, text: str, source_lang: str, target_lang: str, engine_names: List[str]) -> Generator:
        if not text or not text.strip():
            yield "<p>❌ Please enter a term to translate. 請輸入要翻譯的術語。</p>", ""
            return
        
        text = text.strip()
        results = []
        for engine_name in engine_names:
            if engine_name in self.engines:
                info = self.engines[engine_name]
                results.append(TranslationResult(
                    engine=info["name"], engine_zh=info["name_zh"],
                    source_lang=source_lang, target_lang=target_lang,
                    source_text=text, translated_text="", success=False, status="pending"
                ))
        
        yield create_status_html(results, "Starting... 開始翻譯..."), ""
        
        for i, engine_name in enumerate(engine_names):
            if engine_name not in self.engines:
                continue
            
            info = self.engines[engine_name]
            results[i].status = "running"
            yield create_status_html(results, f"{info['name']} ({info['name_zh']})"), ""
            
            try:
                results[i] = self._translate_single(text, source_lang, target_lang, engine_name)
            except Exception as e:
                results[i].success = False
                results[i].status = "error"
                results[i].error_message = str(e)[:80]
            
            current = f"{info['name']}" if i < len(engine_names) - 1 else ""
            yield create_status_html(results, current), self._to_json(results)
            time.sleep(0.3)
        
        yield create_status_html(results, ""), self._to_json(results)
    
    def _to_json(self, results: List[TranslationResult]) -> str:
        data = [{"engine": r.engine, "engine_zh": r.engine_zh, "translation": r.translated_text, "time": f"{r.translation_time:.2f}s"} for r in results if r.success]
        return json.dumps(data, ensure_ascii=False, indent=2)

# ============================================================
# GRADIO INTERFACE
# ============================================================

def create_gradio_interface(translator: MultiMTTranslator):
    if not GRADIO_AVAILABLE:
        print("❌ Gradio not available")
        return None
    
    lang_choices = [f"{code} - {name}" for code, name in SUPPORTED_LANGUAGES.items()]
    
    with gr.Blocks(title="🔤 Multi-MT Term Comparison Tool", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🔤 Multi-MT Term Comparison Tool
        # 多引擎術語翻譯比較工具
        
        Compare how different MT engines translate **terminology** across languages.
        比較不同機器翻譯引擎如何翻譯**專業術語**。
        
        > 📚 **Designed for Terminology Management Courses 專為術語管理課程設計**
        ---
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                input_text = gr.Textbox(
                    label="🔤 Term / Phrase to Translate 要翻譯的術語/詞組",
                    placeholder="Enter a term here... 在此輸入術語...\n\nExamples: 衞生署衞生防護中心, blockchain, 碳中和",
                    lines=3, max_lines=6
                )
            with gr.Column(scale=1):
                source_lang = gr.Dropdown(choices=["auto - Auto Detect"] + lang_choices, value="auto - Auto Detect", label="🌍 Source Language 源語言")
                target_lang = gr.Dropdown(choices=lang_choices, value="en - English", label="🎯 Target Language 目標語言")
        
        gr.Markdown("### 🔧 Select MT Engines 選擇翻譯引擎")
        with gr.Row():
            use_google = gr.Checkbox(label="Google 谷歌", value=True)
            use_bing = gr.Checkbox(label="Bing 必應", value=True)
            use_alibaba = gr.Checkbox(label="Alibaba 阿里", value=True)
            use_sogou = gr.Checkbox(label="Sogou 搜狗", value=True)
        with gr.Row():
            use_youdao = gr.Checkbox(label="Youdao 有道", value=True)
            use_tencent = gr.Checkbox(label="Tencent 騰訊", value=True)
            use_lingvanex = gr.Checkbox(label="Lingvanex", value=False)
            use_mymemory = gr.Checkbox(label="MyMemory", value=False)
        
        translate_btn = gr.Button("🚀 Compare Translations! 比較翻譯結果!", variant="primary", size="lg")
        
        gr.Markdown("---")
        results_html = gr.HTML(value="<p style='text-align:center; color:#888; padding:40px;'>👆 Enter a term and click Compare 輸入術語並點擊比較</p>")
        
        with gr.Accordion("📋 JSON Output (for developers)", open=False):
            results_json = gr.Code(language="json", label="JSON")
        
        def do_translate_streaming(text, source, target, g, b, a, s, y, t, l, m):
            if not text.strip():
                yield "<p style='text-align:center; color:#f44336;'>❌ Please enter a term! 請輸入術語！</p>", ""
                return
            
            src = source.split(" - ")[0] if " - " in source else source
            tgt = target.split(" - ")[0] if " - " in target else target
            
            engines = []
            if g and "google" in translator.engines: engines.append("google")
            if b and "bing" in translator.engines: engines.append("bing")
            if a and "alibaba" in translator.engines: engines.append("alibaba")
            if s and "sogou" in translator.engines: engines.append("sogou")
            if y and "youdao" in translator.engines: engines.append("youdao")
            if t and "tencent" in translator.engines: engines.append("tencent")
            if l and "lingvanex" in translator.engines: engines.append("lingvanex")
            if m and "mymemory" in translator.engines: engines.append("mymemory")
            
            if not engines:
                yield "<p style='color:#f44336;'>❌ Please select at least one engine! 請選擇至少一個引擎！</p>", ""
                return
            
            for html, json_out in translator.translate_streaming(text, src, tgt, engines):
                yield html, json_out
        
        translate_btn.click(
            fn=do_translate_streaming,
            inputs=[input_text, source_lang, target_lang, use_google, use_bing, use_alibaba, use_sogou, use_youdao, use_tencent, use_lingvanex, use_mymemory],
            outputs=[results_html, results_json]
        )
        
        # Examples Section
        gr.Markdown("---\n## 📚 Terminology Examples 術語範例\nClick on any term below to load it for comparison.\n點擊下方任意術語即可載入比較。")
        
        gr.Markdown("### 🏥 Medical & Health 醫療健康")
        gr.Examples(examples=[
            ["衞生署衞生防護中心", "auto - Auto Detect", "en - English"],
            ["基孔肯雅熱", "auto - Auto Detect", "en - English"],
            ["polymerase chain reaction", "en - English", "zh-TW - 繁體中文 (Traditional Chinese)"],
        ], inputs=[input_text, source_lang, target_lang], label="")
        
        gr.Markdown("### ⚖️ Legal & Government 法律政府")
        gr.Examples(examples=[
            ["立法會", "auto - Auto Detect", "en - English"],
            ["司法覆核", "auto - Auto Detect", "en - English"],
            ["habeas corpus", "en - English", "zh-TW - 繁體中文 (Traditional Chinese)"],
        ], inputs=[input_text, source_lang, target_lang], label="")
        
        gr.Markdown("### 💰 Finance & Business 財經商業")
        gr.Examples(examples=[
            ["恒生指數", "auto - Auto Detect", "en - English"],
            ["量化寬鬆", "auto - Auto Detect", "en - English"],
            ["blockchain", "en - English", "zh-TW - 繁體中文 (Traditional Chinese)"],
        ], inputs=[input_text, source_lang, target_lang], label="")
        
        gr.Markdown("### 💻 Technology 科技")
        gr.Examples(examples=[
            ["人工智能", "auto - Auto Detect", "en - English"],
            ["機器學習", "auto - Auto Detect", "en - English"],
            ["natural language processing", "en - English", "zh-TW - 繁體中文 (Traditional Chinese)"],
        ], inputs=[input_text, source_lang, target_lang], label="")
        
        gr.Markdown("### 🌍 Environment 環境")
        gr.Examples(examples=[
            ["碳中和", "auto - Auto Detect", "en - English"],
            ["可再生能源", "auto - Auto Detect", "en - English"],
            ["carbon footprint", "en - English", "zh-TW - 繁體中文 (Traditional Chinese)"],
        ], inputs=[input_text, source_lang, target_lang], label="")
        
        gr.Markdown("### 📚 Education 教育")
        gr.Examples(examples=[
            ["通識教育", "auto - Auto Detect", "en - English"],
            ["持續進修", "auto - Auto Detect", "en - English"],
            ["blended learning", "en - English", "zh-TW - 繁體中文 (Traditional Chinese)"],
        ], inputs=[input_text, source_lang, target_lang], label="")
        
        gr.Markdown("""
        ---
        ### 💡 Tips for Terminology Comparison 術語比較小貼士
        1. **Observe variations 觀察差異**: Different engines may produce different translations
        2. **Context matters 語境很重要**: Some terms have multiple valid translations
        3. **Consistency 一致性**: For terminology management, consistency is key
        ---
        🔤 **Multi-MT Term Comparison Tool** | 多引擎術語翻譯比較工具
        *Built for Terminology Management Education 專為術語管理教育而設*
        """)
    
    return demo
