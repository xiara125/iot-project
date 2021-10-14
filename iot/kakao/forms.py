from django import forms
import json
import requests

class KaKaoTalkForm(forms.Form):
    # CahrField -> input type="text" 와 같음
    text = forms.CharField(label='전송할 Talk', max_length=300)
    web_url = forms.CharField(label='Web URL', max_length=300,
            initial='http://192.168.35.71:8000/mjpeg/?mode=stream')
    mobile_web_url = forms.CharField(label='Mobile Url', max_length=300,
            initial='http://192.168.35.71:8000/mjpeg/?mode=stream')
    
    def send_talk(self):
        # 카톡 메시지 전송용 URL    
        talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        with open("access_token.txt", "r") as f:
            token = f.read()
        header = {"Authorization": f"Bearer {token}"}
        
        # 카톡 메시지 템플릿
        text_template = {
            'object_type': 'text',  # 템플릿 종류
            'text': self.cleaned_data['text'],
            'link': {
                'web_url': self.cleaned_data['web_url'],
                'mobile_web_url': self.cleaned_data['mobile_web_url']
            },
            'button_title': '카메라 보기'
        }

        print(text_template)
        payload = {'template_object': json.dumps(text_template)}
        res = requests.post(talk_url, data=payload, headers=header)
        return res, self.cleaned_data['text']   