"""
สร้างฐานข้อมูลข้อมูลการดูแลสุนัข 96 สายพันธุ์
"""
import json

# ข้อมูลการดูแลสายพันธุ์สุนัข (สั้นๆ กระชับ)
breed_care_data = {
    "Chihuahua": {
        "personality": "กระตือรือร้น ภักดี ชอบเจ้าของคนเดียว",
        "exercise": "น้อย - เดินเล่น 20-30 นาที/วัน",
        "nutrition": "อาหารเม็ดขนาดเล็ก 1/4-1/2 ถ้วย/วัน",
        "health_care": "ระวังฟันผุ ข้อเข่าเคล็ด อุณหภูมิต่ำ",
        "grooming": "แปรงขนสัปดาห์ละ 2-3 ครั้ง"
    },
    "Japanese spaniel": {
        "personality": "สง่างาม เป็นมิตร ชอบความสนใจ",
        "exercise": "น้อย - เดินเล่นสั้นๆ ภายในบ้าน",
        "nutrition": "อาหารคุณภาพสูง 1/2-1 ถ้วย/วัน",
        "health_care": "ระวังปัญหาหัวใจ ตาแห้ง",
        "grooming": "แปรงขนทุกวัน หวีขนยาว"
    },
    "Maltese dog": {
        "personality": "ร่าเริง เป็นมิตร ชอบเล่น",
        "exercise": "น้อย-ปานกลาง เดินเล่น 30 นาที/วัน",
        "nutrition": "อาหารเม็ดเล็ก 1/4-1/2 ถ้วย/วัน",
        "health_care": "ระวังฟันผุ ข้อเข่าเคล็ด ตาน้ำตา",
        "grooming": "แปรงทุกวัน อาบน้ำสัปดาห์ละครั้ง"
    },
    "Shih-Tzu": {
        "personality": "เป็นมิตร รักครอบครัว ไม่ดุ",
        "exercise": "น้อย เดินเล่นสั้นๆ ภายในบ้าน",
        "nutrition": "อาหารคุณภาพดี 1/2-1 ถ้วย/วัน",
        "health_care": "ระวังทางเดินหายใจ ตา หู",
        "grooming": "แปรงทุกวัน ตัดขนเดือนละครั้ง"
    },
    "pug": {
        "personality": "ขี้เล่น รักเจ้าของ ตลก",
        "exercise": "น้อย ระวังออกกำลังกายหนัก",
        "nutrition": "ควบคุมปริมาณ 1-1.5 ถ้วย/วัน",
        "health_care": "ระวังทางเดินหายใจ อ้วน ตา",
        "grooming": "แปรงสัปดาห์ละ 2-3 ครั้ง ทำความสะอาดรอยพับ"
    },
    "beagle": {
        "personality": "ร่าเริง เป็นมิตร ชอบติดตาม",
        "exercise": "สูง วิ่งเล่น 1-2 ชม./วัน",
        "nutrition": "อาหารคุณภาพดี 1-1.5 ถ้วย/วัน",
        "health_care": "ระวังอ้วน หูอักเสบ",
        "grooming": "แปรงสัปดาห์ละ 2-3 ครั้ง"
    },
    "golden retriever": {
        "personality": "เป็นมิตร ฉลาด ภักดี",
        "exercise": "สูง วิ่งเล่น 1-2 ชม./วัน",
        "nutrition": "อาหารคุณภาพดี 3-4 ถ้วย/วัน",
        "health_care": "ระวังข้อสะโพก มะเร็ง หัวใจ",
        "grooming": "แปรงทุกวัน อาบน้ำเดือนละ 1-2 ครั้ง"
    },
    "Labrador retriever": {
        "personality": "เป็นมิตร กระตือรือร้น ฉลาด",
        "exercise": "สูงมาก วิ่งเล่น ว่ายน้ำ 2 ชม./วัน",
        "nutrition": "อาหารคุณภาพดี 2.5-3 ถ้วย/วัน",
        "health_care": "ระวังอ้วน ข้อสะโพก ข้อศอก",
        "grooming": "แปรงสัปดาห์ละ 2-3 ครั้ง"
    },
    "German shepherd": {
        "personality": "ฉลาด ภักดี กล้าหาญ",
        "exercise": "สูงมาก วิ่งเล่น ฝึกซ้อม 2 ชม./วัน",
        "nutrition": "อาหารโปรตีนสูง 3-4 ถ้วย/วัน",
        "health_care": "ระวังข้อสะโพก ข้อศอก ท้องอืด",
        "grooming": "แปรงทุกวัน ผลัดขนมาก"
    },
    "Siberian husky": {
        "personality": "เป็นมิตร กระตือรือร้น ดื้อ",
        "exercise": "สูงมาก วิ่งเล่น 2+ ชม./วัน",
        "nutrition": "อาหารโปรตีนสูง 2-3 ถ้วย/วัน",
        "health_care": "ระวังตา ข้อสะโพก ผิวหนัง",
        "grooming": "แปรงทุกวัน ผลัดขนมากปีละ 2 ครั้ง"
    },
    "Samoyed": {
        "personality": "เป็นมิตร ร่าเริง ชอบความสนใจ",
        "exercise": "สูง วิ่งเล่น 1-2 ชม./วัน",
        "nutrition": "อาหารคุณภาพดี 2.5-3 ถ้วย/วัน",
        "health_care": "ระวังข้อสะโพก ตา หัวใจ",
        "grooming": "แปรงทุกวัน ผลัดขนมาก"
    },
    "Pomeranian": {
        "personality": "กระตือรือร้น ฉลาด ชอบเห่า",
        "exercise": "น้อย เดินเล่น 30 นาที/วัน",
        "nutrition": "อาหารเม็ดเล็ก 1/4-1/2 ถ้วย/วัน",
        "health_care": "ระวังข้อเข่า ฟัน ผิวหนัง",
        "grooming": "แปรงทุกวัน ตัดขนเดือนละครั้ง"
    },
    "Yorkshire terrier": {
        "personality": "กล้าหาญ ภักดี ชอบเจ้าของ",
        "exercise": "น้อย เดินเล่นสั้นๆ",
        "nutrition": "อาหารเม็ดเล็ก 1/4-1/2 ถ้วย/วัน",
        "health_care": "ระวังฟัน ข้อเข่า ตับ",
        "grooming": "แปรงทุกวัน ตัดขนเดือนละครั้ง"
    },
    "boxer": {
        "personality": "ขี้เล่น กระตือรือร้น ภักดี",
        "exercise": "สูง วิ่งเล่น 1-2 ชม./วัน",
        "nutrition": "อาหารคุณภาพดี 2-3 ถ้วย/วัน",
        "health_care": "ระวังหัวใจ มะเร็ง ท้องอืด",
        "grooming": "แปรงสัปดาห์ละ 2-3 ครั้ง"
    },
    "Rottweiler": {
        "personality": "มั่นใจ ภักดี ป้องกันดี",
        "exercise": "สูง วิ่งเล่น ฝึกซ้อม 1-2 ชม./วัน",
        "nutrition": "อาหารโปรตีนสูง 4-6 ถ้วย/วัน",
        "health_care": "ระวังข้อสะโพก ข้อศอก หัวใจ",
        "grooming": "แปรงสัปดาห์ละ 2-3 ครั้ง"
    },
    "Doberman": {
        "personality": "ฉลาด ภักดี กล้าหาญ",
        "exercise": "สูงมาก วิ่งเล่น ฝึกซ้อม 2 ชม./วัน",
        "nutrition": "อาหารโปรตีนสูง 2.5-3.5 ถ้วย/วัน",
        "health_care": "ระวังหัวใจ ข้อสะโพก ท้องอืด",
        "grooming": "แปรงสัปดาห์ละ 2-3 ครั้ง"
    },
    "dalmatian": {
        "personality": "กระตือรือร้น เป็นมิตร ชอบวิ่ง",
        "exercise": "สูงมาก วิ่งเล่น 2+ ชม./วัน",
        "nutrition": "อาหารโปรตีนปานกลาง 2-2.5 ถ้วย/วัน",
        "health_care": "ระวังหูหนวก นิ่วในไต ผิวหนัง",
        "grooming": "แปรงทุกวัน ผลัดขนมาก"
    },
    "French bulldog": {
        "personality": "ขี้เล่น เป็นมิตร ไม่ชอบอยู่คนเดียว",
        "exercise": "น้อย ระวังออกกำลังกายหนัก",
        "nutrition": "อาหารคุณภาพดี 1-1.5 ถ้วย/วัน",
        "health_care": "ระวังทางเดินหายใจ กระดูกสันหลัง ตา",
        "grooming": "แปรงสัปดาห์ละ 2-3 ครั้ง ทำความสะอาดรอยพับ"
    },
    "Boston bull": {
        "personality": "เป็นมิตร ฉลาด ขี้เล่น",
        "exercise": "ปานกลาง เดินเล่น 30-60 นาที/วัน",
        "nutrition": "อาหารคุณภาพดี 1-2 ถ้วย/วัน",
        "health_care": "ระวังทางเดินหายใจ ตา ข้อเข่า",
        "grooming": "แปรงสัปดาห์ละ 2-3 ครั้ง"
    },
    "chow": {
        "personality": "เป็นกลาง ภักดีเจ้าของ ห่างเหิน",
        "exercise": "ปานกลาง เดินเล่น 1 ชม./วัน",
        "nutrition": "อาหารคุณภาพดี 2-2.75 ถ้วย/วัน",
        "health_care": "ระวังข้อสะโพก ข้อศอก ตา",
        "grooming": "แปรงทุกวัน ผลัดขนมาก"
    }
}

# เพิ่มข้อมูลพื้นฐานสำหรับสายพันธุ์ที่เหลือ (ข้อมูลทั่วไป)
default_info = {
    "personality": "เป็นมิตร ภักดี เหมาะกับครอบครัว",
    "exercise": "ปานกลาง เดินเล่น 30-60 นาที/วัน",
    "nutrition": "อาหารคุณภาพดี ปริมาณตามขนาดตัว",
    "health_care": "ตรวจสุขภาพประจำปี ฉีดวัคซีนครบ",
    "grooming": "แปรงขนสัปดาห์ละ 2-3 ครั้ง"
}

# โหลดรายชื่อสายพันธุ์ทั้งหมด
with open('models/resnet34_dog_breeds.json', 'r', encoding='utf-8') as f:
    all_breeds = json.load(f)

# สร้างข้อมูลสำหรับทุกสายพันธุ์
complete_breed_info = {}

for class_id, breed_name in all_breeds.items():
    # ทำความสะอาดชื่อสายพันธุ์ (เอาเฉพาะชื่อหลัก)
    clean_name = breed_name.split(',')[0].strip()
    
    # ใช้ข้อมูลที่มีอยู่ หรือข้อมูลพื้นฐาน
    if clean_name in breed_care_data:
        complete_breed_info[class_id] = {
            "breed_name": breed_name,
            "care_info": breed_care_data[clean_name]
        }
    else:
        # ใช้ข้อมูลพื้นฐาน
        complete_breed_info[class_id] = {
            "breed_name": breed_name,
            "care_info": default_info.copy()
        }

# บันทึกไฟล์
with open('models/breed_care_info.json', 'w', encoding='utf-8') as f:
    json.dump(complete_breed_info, f, indent=2, ensure_ascii=False)

print(f"✅ สร้างข้อมูล {len(complete_breed_info)} สายพันธุ์เรียบร้อย")
print(f"📊 มีข้อมูลละเอียด: {len(breed_care_data)} สายพันธุ์")
print(f"📊 ใช้ข้อมูลพื้นฐาน: {len(complete_breed_info) - len(breed_care_data)} สายพันธุ์")
