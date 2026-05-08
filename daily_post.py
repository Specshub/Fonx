import requests
import os
import time
import random

# الكنوز (تأكد أنها في GitHub Secrets)
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
    # استخدام الإصدار v1beta مع موديل 2.0 فلاش (الأكثر استجابة حالياً)
    model = "gemini-2.0-flash" 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
    
    prompt = "اكتب قصة درامية أدبية مشوقة باللغة العربية (أكثر من 800 كلمة) بأسلوب روائي حصري، وفي النهاية أضف حكمة قانونية عميقة تناسب الأحداث."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    # نظام المحاولات "المراوغ"
    for attempt in range(5): # رفعنا عدد المحاولات لـ 5
        # انتظار عشوائي في البداية لتجنب "تزامن" السيرفرات
        wait_time = random.randint(30, 90) 
        print(f"🔄 المحاولة {attempt + 1}: سأنتظر {wait_time} ثانية قبل الهجوم...")
        time.sleep(wait_time)
        
        res = requests.post(url, json=payload)
        
        if res.status_code == 200:
            print(f"✅ نجح الاختراق! تم تأليف القصة.")
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        elif res.status_code == 429:
            print("⚠️ السيرفر لا يزال مزدحماً.. سأنسحب مؤقتاً.")
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
        "title": f"تأملات اليوم: {content[:35].strip()}...",
        "content": content,
        "labels": ["دراما 2026", "ثقافة قانونية"]
    }
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ مبروك يا قبطان! تم النشر في مدونة Mixa TV.")
    else:
        print(f"❌ فشل النشر في بلوجر.")

# التنفيذ
story = write_story()
if story:
    post_to_blogger(story)
