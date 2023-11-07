from credentials import auth_key
import deepl

backbone = deepl.Translator(auth_key)

languages = [
    'BG', 'CS', 'DA', 'DE', 'EL', 'EN', 'ES',
    'ET', 'FI', 'FR', 'HU', 'ID', 'IT', 'JA',
    'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT',
    'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK',
    'ZH'
]
# ^^ source: https://www.deepl.com/docs-api/translate-text
