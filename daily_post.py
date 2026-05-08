import requests
import os
import time

# الكنوز (تأكد من وجودها في GitHub Secrets)
GEMINI_KEY = os.getenv('GEMINI_KEY')
BLOG_ID = os.getenv('BLOG_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = "644474811808-67jn32susumuth7iar9fk6bfq9ir6ndn.apps.googleusercontent.com"

def get_new_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN, "grant_type": "refresh_token"
    }
    return requests.post(url, data=data).json().get('access_token')

def write_story():
    # سنركز على الموديل الذي أعطى استجابة (حتى لو كانت زحاماً)
    model = "gemini-2.0-flash" 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
    
    prompt = "اكتب قصة درامية أدبية مشوقة باللغة العربية (أكثر من 800 كلمة) بأسلوب روائي حصري، وفي النهاية أضف حكمة قانونية عميقة تناسب الأحداث."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    # محاولة لثلاث مرات في حال وجود زحام (خطأ 429)
    for attempt in range(3):
        print(f"🔄 محاولة التأليف (المحاولة {attempt + 1})...")
        res = requests.post(url, json=payload)
        
        if res.status_code == 200:
            print(f"✅ نجح التأليف أخيراً!")
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        elif res.status_code == 429:
            print("⚠️ السيرفر مزدحم (429).. سأنتظر 30 ثانية ثم أحاول مجدداً.")
            time.sleep(30) # انتظار نصف دقيقة
        else:
            print(f"❌ خطأ غير متوقع: {res.status_code}")
            break
            
    return None

def post_to_blogger(content):
    if not content: return
    token = get_new_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = {
        "kind": "blogger#post",
        "title": f"حكاية وتأمل: {content[:35].strip()}...",
        "content": content,
        "labels": ["دراما 2026", "فكر قانوني"]
    }
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ مبروك يا قبطان! تم النشر في Mixa TV بنجاح ساحق.")
    else:
        print(f"❌ فشل النشر: {res.text}")

# الإقلاع
story = write_story()
if story:
    post_to_blogger(story)
else:
    print("❌ للأسف لم نتمكن من تجاوز زحام السيرفر اليوم. جرب تشغيله يدوياً بعد قليل.")
