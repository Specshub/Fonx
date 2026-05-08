import requests
import os

# جلب البيانات من أسرار GitHub
GEMINI_KEY = os.getenv('GEMINI_KEY')
BLOG_ID = os.getenv('BLOG_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = "644474811808-67jn32susumuth7iar9fk6bfq9ir6ndn.apps.googleusercontent.com"

def get_new_access_token():
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
    # تحديث المحرك إلى Gemini 3 Flash (موديل 2026)
    # نستخدم الإصدار v1 المستقر
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-3-flash:generateContent?key={GEMINI_KEY}"
    
    prompt = """
    اكتب قصة أدبية درامية مشوقة باللغة العربية بأسلوب المسلسلات التركية الراقية.
    المواصفات:
    1. طول المقال يتجاوز 800 كلمة.
    2. صراع درامي نفسي قوي.
    3. في النهاية، أضف فقرة 'رؤية قانونية' تحلل أحداث القصة من منظور الحقوق والواجبات (بما يتناسب مع خبرتك في القانون).
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    res = requests.post(url, json=payload)
    response_data = res.json()
    
    # فحص الرد للتأكد من نجاح العملية
    if 'candidates' in response_data:
        return response_data['candidates'][0]['content']['parts'][0]['text']
    else:
        print("❌ فشل الاتصال بمحرك 2026. الرد:")
        print(response_data)
        return None

def post_to_blogger(content):
    if not content: return
    token = get_new_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # عنوان جذاب للمقال
    title = f"قصص وأحكام: {content[:45].strip()}..." 
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": ["دراما واقعية", "فلسفة قانونية"]
    }
    
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ مبروك يا قبطان! تم النشر في مدونة Mixa TV بنجاح ساحق.")
    else:
        print(f"❌ فشل النشر في بلوجر. السبب: {res.text}")

# التنفيذ النهائي
story_text = write_story()
if story_text:
    post_to_blogger(story_text)
