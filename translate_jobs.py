import asyncio
import time
from googletrans import Translator, LANGUAGES
import os

translator = Translator()

# --------------------------------------------
# Визначення коду мови
# --------------------------------------------
def CodeLang(lang):
    lang = lang.lower()

    if lang in LANGUAGES:
        return lang

    for code, name in LANGUAGES.items():
        if lang == name.lower():
            return code

    return None


# --------------------------------------------
# ПОСЛІДОВНИЙ переклад (без gather)
# --------------------------------------------
async def process_text_file(file_path, target_lang):

    print("=== ПОСЛІДОВНИЙ ПЕРЕКЛАД ===")

    with open(file_path, "r", encoding="utf-8") as f:
        txt = f.read()

    print(f"Файл: {file_path}")
    print(f"Кількість символів: {len(txt)}")

    sentences = [s.strip() for s in txt.split('.') if s.strip()]
    print(f"Кількість речень: {len(sentences)}")

    start_time = time.time()

    detected = await translator.detect(txt)
    orig_lang = detected.lang
    confidence = detected.confidence

    translated_sentences = []

    for sentence in sentences:
        result = await translator.translate(sentence, dest=CodeLang(target_lang))
        translated_sentences.append(result.text)

    translated_text = '. '.join(translated_sentences) + '.'

    end_time = time.time()

    print(f"Оригінальна мова: {orig_lang}, confidence: {confidence}")
    print(f"Мова перекладу: {target_lang}, код: {CodeLang(target_lang)}")
    print("Переклад:\n", translated_text)
    print(f"Час послідовного перекладу: {end_time - start_time:.2f} секунд\n")


# --------------------------------------------
# АСИНХРОННИЙ переклад (через gather)
# --------------------------------------------
async def async_translate_sentences(file_path, target_lang):

    print("=== АСИНХРОННИЙ ПЕРЕКЛАД ===")

    with open(file_path, "r", encoding="utf-8") as f:
        txt = f.read()

    sentences = [s.strip() for s in txt.split('.') if s.strip()]

    start_time = time.time()

    detected = await translator.detect(txt)
    orig_lang = detected.lang
    confidence = detected.confidence

    tasks = [
        translator.translate(sentence, dest=CodeLang(target_lang))
        for sentence in sentences
    ]

    results = await asyncio.gather(*tasks)

    translated_text = '. '.join([r.text for r in results]) + '.'

    end_time = time.time()

    print(f"Оригінальна мова: {orig_lang}, confidence: {confidence}")
    print(f"Мова перекладу: {target_lang}, код: {CodeLang(target_lang)}")
    print("Переклад:\n", translated_text)
    print(f"Час асинхронного перекладу: {end_time - start_time:.2f} секунд\n")


# --------------------------------------------
# ГОЛОВНА async-функція
# --------------------------------------------
async def main():

    file_path = "Steve_Jobs.txt"
    target_language = "en"

    if not os.path.exists(file_path):
        print("Файл не знайдено!")
        return

    await process_text_file(file_path, target_language)
    await async_translate_sentences(file_path, target_language)


# --------------------------------------------
# Запуск
# --------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())