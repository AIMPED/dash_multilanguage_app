import uuid
import dash
from dash import html, dcc, Input, Output, State
from my_cache import cache, CACHE_CONFIG
import translator
from dataclasses import dataclass


# simple dataclass
@dataclass
class Translatable:
    id: str
    prop: str
    text: str

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, json):
        return cls(**json)


# create some instances
title = Translatable('title', 'children', 'Just a title to translate.')
body = Translatable('content', 'children', 'What if this content would be translatable to 31 languages?')
btn = Translatable('button_1', 'children', 'click to change language')

# group instances into list
list_to_translate = [title, body, btn]

# initiate app
app = dash.Dash(
    __name__
)

# initialize caching.
# Caching is used for decreasing the number of calls to the deepl translator API
# the free version is limited to 500.000 characters / month
cache.init_app(app.server, config=CACHE_CONFIG)

app.layout = html.Div(
    [
        html.H2(
            children=title.text,
            id=title.id,
        ),
        html.Div(
            [
                html.Button(
                    children=btn.text,
                    id=btn.id,
                ),
                html.Div(
                    dcc.Dropdown(
                        options=translator.languages,
                        # ^^ languages supported by deepl (November 2023)
                        id='language_selector',
                        placeholder='choose language...'
                    ),
                    style={'width': '40%'}
                )
            ],
            style={'display': 'flex'}
        ),
        html.Div(
            children=body.text,
            id=body.id,
            style={'margin-top': '20px'}
        )
    ]
)


@app.callback(
    [Output(obj.id, obj.prop) for obj in list_to_translate],
    Input(btn.id, 'n_clicks'),
    State('language_selector', 'value'),
    prevent_initial_call=True
)
def do(_, language):
    if language == 'EN':
        return [obj.text for obj in list_to_translate]

    # ^^ base language is english (EN)

    @cache.memoize()
    def language_check(arg: str):
        print('got cached: ', arg)
        return translator.backbone.translate_text(
            text=[obj.text for obj in list_to_translate],
            target_lang=arg
        ), uuid.uuid4()
        # ^^ I added a for debugging the memoize function

    translated, _uuid = language_check(language)
    print('language: ', language, ' | id:', _uuid)

    return [item.text for item in translated]


if __name__ == '__main__':
    app.run(debug=True)
