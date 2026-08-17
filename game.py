import json
import os
import random
import time

def load_story():
    try:
        with open('story.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ ไม่พบไฟล์ story.json กรุณาสร้างไฟล์ก่อนรันโปรแกรม")
        exit()

def write_to_obs(text):
    """ส่งข้อมูลข้อความออกไปยังไฟล์ display.txt ให้ OBS ดึงไปใช้"""
    with open('display.txt', 'w', encoding='utf-8') as f:
        f.write(text)

def trigger_random_event():
    """สุ่มเหตุการณ์พิเศษระหว่างเปลี่ยนฉากเพื่อความตื่นเต้นในไลฟ์"""
    events = [
        "⚡ [เหตุการณ์สุ่ม]: ไฟฟ้าในคฤหาสน์ดับลงชั่วขณะ! เสียงกรีดร้องดังขึ้น!",
        "🌧️ [เหตุการณ์สุ่ม]: ฝนตกหนักขึ้น ลบรอยเท้าบางส่วนข้างนอก!",
        "🔍 [เหตุการณ์สุ่ม]: คนดูในแชทตาดี! สังเกตเห็นเงาลึกลับผ่านหน้าต่าง!",
        None, None
    ]
    return random.choice(events)

def run_game():
    story = load_story()
    current_node = "start"
    total_evidence = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        node_data = story.get(current_node)

        if not node_data:
            print("ไม่พบข้อมูลฉากนี้")
            break

        # อัปเดตคะแนนหลักฐาน
        total_evidence += node_data.get("evidence_gain", 0)
        if total_evidence > 100:
            total_evidence = 100

        # สุ่มเหตุการณ์พิเศษ
        event_text = trigger_random_event()

        # ฟอร์แมตข้อความที่จะโชว์บนจอ OBS
        display_lines = []
        display_lines.append("🔍 === รายการสืบสวนคดีปริศนา (LIVE) ===")
        display_lines.append(f"📊 ระดับความคลี่คลายคดี: {total_evidence}%\n")
        
        if event_text:
            display_lines.append(f"{event_text}\n")

        display_lines.append(f"{node_data['text']}\n")

        choices = node_data.get("choices", {})
        if choices:
            display_lines.append("------------------------------------------")
            display_lines.append("💬 [ให้แชทพิมพ์โหวตเลือกทางเลือกด้านล่าง]")
            for key, choice in choices.items():
                display_lines.append(f"   {choice['text']}")
            display_lines.append("------------------------------------------")
        else:
            display_lines.append("\n==========================================")
            display_lines.append("🏁 จบการสืบสวนคดีนี้")

        full_display_text = "\n".join(display_lines)

        # บันทึกลงไฟล์ให้ OBS
        write_to_obs(full_display_text)

        # แสดงหน้าจอควบคุมของสตรีมเมอร์
        print("==========================================")
        print("🖥️  [กำลังส่งออกข้อความไปยัง OBS Studio]")
        print("==========================================")
        print(full_display_text)
        print("==========================================")

        if not choices:
            input("\n🎯 จบเกมเรียบร้อย กด Enter เพื่อปิดโปรแกรม...")
            break

        # รับตัวเลือกจากสตรีมเมอร์ (ที่ดูผลโหวตมาจากแชท)
        user_choice = input("\n👉 พิมพ์ตัวเลือกตามผลโหวตแชท (1/2/3): ").strip()

        if user_choice in choices:
            current_node = choices[user_choice]["next"]
        else:
            print("⚠️ กรุณาพิมพ์ตัวเลขที่มีในตัวเลือกเท่านั้น!")
            time.sleep(1)

if __name__ == "__main__":
    run_game()
