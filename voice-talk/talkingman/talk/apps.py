from googletrans import Translator

translator = Translator()
translated = translator.translate("வணக்கம்", dest='ta')
print(translated.text)