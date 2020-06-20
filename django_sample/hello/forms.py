# -*- coding: utf-8 -*-

from django import forms
from hello.models import Friend, Message

# 値 → ラベル
pulldown_menu = [
        ("1", "北海道"),
        ("2", "東京都"),
        ("3", "大阪"),
        ("4", "福岡"),
     ]


# 6
class HelloForm(forms.Form):

    name = forms.CharField(label="名前")

    mail = forms.EmailField(label="メールアドレス")

    age = forms.IntegerField(label="年齢")

    birthday = forms.DateField(label="誕生日")

    check = forms.BooleanField(label="チェックボックス", required=False)

    check_other = forms.NullBooleanField(label="チェックボックス_3択")

    pulldown = forms.ChoiceField(label="プルダウン", \
                choices=pulldown_menu)

    radio_button = forms.ChoiceField(label="ラジオボタン", \
                choices=pulldown_menu, widget=forms.RadioSelect())

    select_list = forms.ChoiceField(label="セレクトリスト", \
                choices=pulldown_menu, widget=forms.Select(attrs={"size":4}))

    multi_select_list = forms.MultipleChoiceField(label="多数セレクトリスト", \
                choices=pulldown_menu, widget=forms.SelectMultiple(attrs={"size":4}))


# Friend検索Form
class HelloSearchForm(forms.Form):

    id = forms.IntegerField(label="ID", required=False)


# Friend作成Form(個別に都度登録する場合のForm)
class HelloInsertForm(forms.Form):

    # 名前
    name = forms.CharField(label="名前")
    # メールアドレス
    mail = forms.EmailField(label="メールアドレス")
    # 年齢
    age = forms.IntegerField(label="年齢")
    # 性別
    gender = forms.BooleanField(label="性別")
    # 誕生日
    birthday = forms.DateField(label="誕生日")


# Friend作成Form(DB登録する際の処理をかんたんにするForm)
class HelloModelMapper(forms.ModelForm):

    class Meta:
        model = Friend
        fields = ["name", "mail", "age", "gender", "birthday"]


# Friend検索フォーム
class HelloFindForm(forms.Form):

    name = forms.CharField(label='名前', required=False)
    mail = forms.CharField(label='メールアドレス', required=False)
    age = forms.IntegerField(label='年齢', required=False)


class ValidForm(forms.Form):

    req_char = forms.CharField(label='必須文字')
    min_len = forms.CharField(label="最小入力文字数=5", min_length=5)
    max_len = forms.CharField(label="最大入力文字数=5", max_length=5)

    req_number = forms.IntegerField(label='必須数値')
    min_val = forms.IntegerField(label="最小値=5", min_value=5)
    max_val = forms.FloatField(label="最大値=5", max_value=5)

    req_date = forms.DateField(label="必須日付", input_formats=['%d'], required=False)
    req_time = forms.TimeField(label="必須時刻", required=False)
    req_datetime = forms.DateTimeField(label="必須日時と時刻", required=False)

    def clean(self):
        cleaned_data = super().clean()
        min_len = cleaned_data["min_len"]
        max_len = cleaned_data["max_len"]
        print("min_len=" + min_len)
        print("max_len=" + max_len)
        if (min_len == max_len):
            raise forms.ValidationError("最小入力文字数と最大入力文字数が同一の値")

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["title", "content", "friend"]
