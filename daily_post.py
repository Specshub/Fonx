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
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    # تعديل البرومبت ليكون أكثر دقة وتجنب الفلاتر
    prompt = "اكتب قصة أدبية درامية مشوقة باللغة العربية حول حكاية خيالية مستوحاة من الأجواء التركية. اجعلها طويلة (أكثر من 700 كلمة) بأسلوب روائي مشوق، وفي النهاية أضف فقرة 'تأملات قانونية' تربط الأحداث بمبادئ العدل."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "safetySettings": [ # تقليل قيود الفلاتر لضمان النشر
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    res = requests.post(url, json=payload)
    response_data = res.json()
    
    # التحقق مما إذا كان هناك رد صحيح
    if 'candidates' in response_data:
        return response_data['candidates'][0]['content']['parts'][0]['text']
    else:
        print("❌ فشل Gemini في توليد النص. الرد كان:")
        print(response_data) # سيطبع لنا الخطأ الحقيقي في Actions
        return None

def post_to_blogger(content):
    if not content: return
    token = get_new_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    title = f"حكاية أدبية: {content[:40]}..." 
    data = {"kind": "blogger#post", "title": title, "content": content, "labels": ["قصص درامية"]}
    requests.post(url, headers=headers, json=data)

# التنفيذ
story = write_story()
if story:
    post_to_blogger(story)
    print("✅ تم النشر بنجاح!")
