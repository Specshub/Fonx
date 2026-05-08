import requests
import os

# --- جلب البيانات السرية من GitHub Secrets ---
GEMINI_KEY = os.getenv('GEMINI_KEY')
BLOG_ID = os.getenv('BLOG_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# رابط النفق السري الجديد الخاص بك
GAS_URL = "https://script.google.com/macros/s/AKfycbzsccYHLA1LbDzo3jAFsDodqY7yKlXmPd7G0fRM9F3ubdxIrG6TMxhVsavK8FL3TwVk5g/exec"

# بيانات الهوية (ثابتة)
CLIENT_ID = "644474811808-67jn32susumuth7iar9fk6bfq9ir6ndn.apps.googleusercontent.com"

def get_new_access_token():
    """توليد تصريح دخول جديد لمدونة Blogger"""
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    try:
        res = requests.post(url, data=data)
        return res.json().get('access_token')
    except Exception as e:
        print(f"❌ خطأ في الـ Access Token: {e}")
        return None

def write_story():
    """تأليف القصة عبر النفق السري لتجنب الحظر (429)"""
    print("🚀 جاري عبور النفق السري إلى Gemini...")
    
    # البرومبت الذي يجمع بين الدراما وخلفيتك في دراسة القانون
    prompt = """
    اكتب قصة أدبية درامية مشوقة باللغة العربية (أكثر من 900 كلمة).
    الأسلوب: روائي بلمسة المسلسلات التركية، يركز على صراع حول الحقوق أو الميراث أو العدالة.
    الخاتمة: أضف فقرة رصينة بعنوان 'تحليل قانوني للأحداث' تربط القصة بالمواد القانونية أو روح العدالة بأسلوب أكاديمي.
    """
    
    payload = {
        "apiKey": GEMINI_KEY,
        "prompt": prompt
    }
    
    try:
        # إرسال الطلب لـ Apps Script
        res = requests.post(GAS_URL, json=payload, timeout=120)
        
        if res.status_code == 200:
            data = res.json()
            if 'candidates' in data:
                print("✅ تم استلام القصة بنجاح من داخل خوادم جوجل!")
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"⚠️ رد غير مكتمل من النفق: {data}")
        else:
            print(f"❌ النفق لا يزال مغلقاً (Status: {res.status_code})")
    except Exception as e:
        print(f"❌ عطل في النفق: {e}")
        
    return None

def post_to_blogger(content):
    """نشر المحتوى في مدونة Mixa TV"""
    if not content: return
    
    token = get_new_access_token()
    if not token: return
    
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # عنوان احترافي للمقال
    title = f"قصص وقوانين: {content[:40].strip()}..."
    
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": ["دراما واقعية", "ثقافة قانونية"]
    }
    
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            print("🎉 مبروك يا بطل! تم النشر بنجاح في مدونة Mixa TV.")
        else:
            print(f"❌ فشل النشر في Blogger: {res.text}")
    except Exception as e:
        print(f"❌ خطأ تقني أثناء النشر: {e}")

# --- نقطة الانطلاق ---
story_text = write_story()
if story_text:
    post_to_blogger(story_text)
else:
    print("🚩 فشلت المهمة في مرحلة التأليف. تفقد إعدادات الـ Web App.")
