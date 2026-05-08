import requests
import os
import json

# جلب البيانات من "أسرار GitHub" (للحماية)
GEMINI_KEY = os.getenv('GEMINI_KEY')
BLOG_ID = os.getenv('BLOG_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
CLIENT_ID = "407408718192.apps.googleusercontent.com" # ثابت من Playground
CLIENT_SECRET = os.getenv('CLIENT_SECRET') # سنستخرجه الآن

def get_new_access_token():
    """توليد تصريح دخول جديد باستخدام المفتاح الدائم"""
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    res = requests.post(url, data=data)
    return res.json().get('access_token')

def write_story():
    """تأليف القصة باستخدام ذكاء Gemini"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    prompt = "اكتب قصة درامية أدبية مشوقة باللغة العربية حول مسلسل تركي مشهور (اختر مسلسلاً مختلفاً في كل مرة). اجعل المقال طويلاً (700 كلمة) وبأسلوب روائي حصري، وفي النهاية أضف حكمة قانونية."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    res = requests.post(url, json=payload)
    return res.json()['candidates'][0]['content']['parts'][0]['text']

def post_to_blogger(content):
    token = get_new_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    # سنستخدم عنواناً عشوائياً جذاباً
    title = f"حكاية من صلب الواقع: {content[:30]}..." 
    data = {"kind": "blogger#post", "title": title, "content": content, "labels": ["قصص درامية"]}
    requests.post(url, headers=headers, json=data)

# التنفيذ
story = write_story()
post_to_blogger(story)
print("✅ تم النشر الآلي بنجاح!")
