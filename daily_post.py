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
    # تحديث الرابط إلى النسخة المستقرة v1 والموديل الأحدث لعام 2026
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    prompt = "اكتب قصة درامية أدبية مشوقة باللغة العربية بأسلوب المسلسلات التركية. اجعل المقال طويلاً (أكثر من 800 كلمة)، وفي النهاية أضف 'تأملات قانونية' تربط القصة بالحقوق والواجبات بأسلوب رصين."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    res = requests.post(url, json=payload)
    response_data = res.json()
    
    if 'candidates' in response_data:
        return response_data['candidates'][0]['content']['parts'][0]['text']
    else:
        # إذا فشل الرابط الأول، سنجرب الرابط الاحتياطي لضمان الإقلاع
        print("⚠️ الرابط الأول فشل، نجرب الرابط الاحتياطي...")
        url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_KEY}"
        res = requests.post(url_alt, json=payload)
        response_data = res.json()
        if 'candidates' in response_data:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            print("❌ فشل Gemini تماماً. الرد:")
            print(response_data)
            return None

def post_to_blogger(content):
    if not content: return
    token = get_new_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    title = f"حكاية اليوم: {content[:40]}..." 
    data = {"kind": "blogger#post", "title": title, "content": content, "labels": ["قصص درامية", "ثقافة قانونية"]}
    
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ مبروك يا قبطان! تم النشر في بلوجر بنجاح.")
    else:
        print(f"❌ فشل النشر في بلوجر. الرد: {res.text}")

# إطلاق المحرك
story = write_story()
if story:
    post_to_blogger(story)
