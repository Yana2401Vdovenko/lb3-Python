import asyncio
import time
from googletrans import Translator, LANGUAGES
import os

translator = Translator()

# ---------------------------
# Функції асинхронного перекладу
# ---------------------------
async def TransLate(text, lang):
    try:
        code = CodeLang(lang)
        if not code:
            return f"Помилка: невірна мова '{lang}'"
        translated = await translator.translate(text, dest=code)
        return translated.text
    except Exception as e:
        return f"Помилка перекладу: {str(e)}"

async def LangDetect(txt):
    try:
        detected = await translator.detect(txt)
        return detected.lang, detected.confidence
    except Exception as e:
        return None, 0

def CodeLang(lang):
    lang = lang.lower()
    # Якщо переданий код мови
    if lang in LANGUAGES:
        return lang
    # Якщо передана назва мови
    for code, name in LANGUAGES.items():
        if lang == name.lower():
            return code
    return None

# ---------------------------
# Переклад всього тексту
# ---------------------------
async def process_text_file(file_path, target_lang):
    if not os.path.exists(file_path):
        print(f"Файл '{file_path}' не знайдено!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        txt = f.read()

    print(f"Файл: {file_path}")
    print(f"Кількість символів: {len(txt)}")
    sentences = txt.split('.')
    print(f"Кількість речень: {len(sentences)}")

    start_time = time.time()
    orig_lang, confidence = await LangDetect(txt)
    translated_text = await TransLate(txt, target_lang)
    end_time = time.time()

    target_code = CodeLang(target_lang)

    print(f"Оригінальна мова: {orig_lang}, confidence: {confidence}")
    print("Оригінальний текст:\n", txt)
    print(f"Мова перекладу: {target_lang}, код: {target_code}")
    print("Переклад:\n", translated_text)
    print(f"Час перекладу: {end_time - start_time:.2f} секунд\n")

# ---------------------------
# Асинхронний переклад кожного речення
# ---------------------------
async def async_translate_sentences(file_path, target_lang):
    if not os.path.exists(file_path):
        print(f"Файл '{file_path}' не знайдено!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        txt = f.read()

    sentences = [s.strip() for s in txt.split('.') if s.strip()]
    start_time = time.time()

    orig_lang, confidence = await LangDetect(txt)
    tasks = [TransLate(s, target_lang) for s in sentences]
    translated_sentences = await asyncio.gather(*tasks)

    end_time = time.time()
    translated_text = '. '.join(translated_sentences) + '.'

    target_code = CodeLang(target_lang)

    print("=== Асинхронний переклад ===")
    print(f"Оригінальна мова: {orig_lang}, confidence: {confidence}")
    print(f"Мова перекладу: {target_lang}, код: {target_code}")
    print("Переклад:\n", translated_text)
    print(f"Час асинхронного перекладу: {end_time - start_time:.2f} секунд\n")

# ---------------------------
# Основна програма
# ---------------------------
if __name__ == "__main__":
    file_path = "Steve_Jobs.txt"
    target_language = "en"

    asyncio.run(process_text_file(file_path, target_language))
    asyncio.run(async_translate_sentences(file_path, target_language))