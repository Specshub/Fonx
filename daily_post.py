import requests
import os

# --- الكنوز المستخرجة من أسرار GitHub ---
GEMINI_KEY = os.getenv('GEMINI_KEY')
BLOG_ID = os.getenv('BLOG_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
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
    return requests.post(url, data=data).json().get('access_token')

def write_story():
    """تأليف القصة باستخدام أفضل موديل متاح حالياً"""
    # قائمة الموديلات المتاحة في 2026 حسب الأولوية
    models_to_try = [
        "gemini-1.5-flash", 
        "gemini-2.0-flash", 
        "gemini-pro"
    ]
    
    prompt = """
    اكتب قصة أدبية درامية مشوقة باللغة العربية بأسلوب المسلسلات التركية الراقية.
    المواصفات:
    1. طول المقال يتجاوز 800 كلمة.
    2. ركز على الصراعات النفسية والاجتماعية.
    3. في النهاية، أضف فقرة 'رؤية قانونية' تحلل أحداث القصة من منظور الحقوق والواجبات بأسلوب أكاديمي رصين.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    for model in models_to_try:
        print(f"🔄 محاولة إرسال الطلب عبر موديل: {model}...")
        # نستخدم v1 المستقرة لأنها الأكثر أماناً في 2026
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GEMINI_KEY}"
        res = requests.post(url, json=payload)
        
        if res.status_code == 200:
            print(f"✅ نجح الاتصال بموديل {model}!")
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"⚠️ الموديل {model} أعاد خطأ: {res.status_code}")

    print("❌ للأسف، فشلت جميع محاولات الاتصال بالموديلات.")
    return None

def post_to_blogger(content):
    """نشر القصة في مدونة Mixa TV"""
    if not content: return
    token = get_new_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # تنسيق العنوان ليكون جذاباً في محركات البحث
    title = f"حكايات درامية: {content[:40].strip()}..."
    
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": ["دراما واقعية", "ثقافة قانونية"]
    }
    
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ مبروك! تم النشر في مدونة Mixa TV بنجاح.")
    else:
        print(f"❌ فشل النشر في بلوجر. الرد: {res.text}")

# --- إطلاق المحرك ---
story = write_story()
if story:
    post_to_blogger(story)
