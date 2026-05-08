import requests
import os

# --- البيانات السرية (تأكد من وجودها في GitHub Secrets) ---
GEMINI_KEY = os.getenv('GEMINI_KEY')
BLOG_ID = os.getenv('BLOG_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# رابط النفق السري الذي قمت بإنشائه (تم تحديثه)
GAS_URL = "https://script.google.com/macros/s/AKfycbyAZPAkBzx2SWUV8_gY7TtYPNv1NRJ3u7ovofb4YJzqwknoyyC6PwDTXsthNu2nUK8KSw/exec"

# الهوية الخاصة بك (لا تتغير)
CLIENT_ID = "644474811808-67jn32susumuth7iar9fk6bfq9ir6ndn.apps.googleusercontent.com"

def get_new_access_token():
    """توليد تصريح دخول جديد لمدونة Mixa TV"""
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
        print(f"❌ خطأ في جلب Access Token: {e}")
        return None

def write_story():
    """تأليف القصة عبر نفق Google Apps Script لتجاوز الحظر"""
    print("🚀 إرسال الطلب عبر 'نفق جوجل السري'...")
    
    # البرومبت المخصص الذي يجمع بين الدراما وخلفيتك القانونية
    prompt = """
    اكتب قصة أدبية درامية مشوقة باللغة العربية بأسلوب روائي حصري (أكثر من 900 كلمة).
    الموضوع: صراع اجتماعي أو عائلي بأسلوب المسلسلات التركية المعاصرة.
    في نهاية المقال، أضف فقرة بعنوان 'الخلاصة القانونية' تحلل فيها الأحداث من منظور القانون والحقوق (بصفتك طالب قانون).
    """
    
    payload = {
        "apiKey": GEMINI_KEY,
        "prompt": prompt
    }
    
    try:
        # إرسال الطلب للرابط الذي زودتني به
        res = requests.post(GAS_URL, json=payload, timeout=120)
        
        if res.status_code == 200:
            data = res.json()
            if 'candidates' in data:
                print("✅ نجح الاختراق! تم توليد القصة بنجاح.")
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"⚠️ الرد من النفق لا يحتوي على قصة: {data}")
        else:
            print(f"❌ النفق أعاد خطأ: {res.status_code}")
    except Exception as e:
        print(f"❌ عطل في الاتصال بالنفق: {e}")
        
    return None

def post_to_blogger(content):
    """نشر القصة في مدونة Blogger"""
    if not content: return
    
    token = get_new_access_token()
    if not token: return
    
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # صياغة عنوان جذاب
    title = f"حكايات Mixa: {content[:45].strip()}..."
    
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": ["دراما واقعية", "ثقافة قانونية"]
    }
    
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            print("✅ مبروك يا قبطان! أول مقال عبر النفق السري نُشر في مدونة Mixa TV.")
        else:
            print(f"❌ فشل النشر في بلوجر: {res.text}")
    except Exception as e:
        print(f"❌ خطأ أثناء النشر: {e}")

# --- إطلاق العملية ---
story_content = write_story()
if story_content:
    post_to_blogger(story_content)
else:
    print("🚩 فشلت المهمة في مرحلة التأليف. تأكد من تفعيل Web App في جوجل بشكل صحيح.")
