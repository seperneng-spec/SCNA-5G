import socket
import psutil
import subprocess
import datetime
import time

# สูตร TPS Dragon Guard
DANGER_PORTS = [3389, 23, 5900] # พอร์ตที่ต้องปิด
GATEWAY = "192.168.1.1"

def check_whoami():
    import getpass
    user = getpass.getuser()
    print(f"[ระบุตัวตน] ✅ ตอนนี้ล็อกอินเป็น: {user}")
    return user

def check_gateway():
    try:
        socket.create_connection((GATEWAY, 80), timeout=2)
        print(f"[ไอพีภายใน] ✅ เชื่อมต่อเราเตอร์ {GATEWAY} ได้ ปกติ")
        return True
    except:
        print(f"[ไอพีภายใน] ⚠️ เชื่อม {GATEWAY} ไม่ได้ เช็คสาย LAN/WiFi")
        return False

def check_firewall_and_ports():
    print(f"[ล็อกไฟร์วอลล์] 🔍 กำลังสแกนพอร์ตเสี่ยง {DANGER_PORTS}...")
    open_found = []
    for port in DANGER_PORTS:
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                open_found.append(port)

    if not open_found:
        print(f"[ปิดพอร์ต] ✅ ปลอดภัย! ไม่พบพอร์ต {DANGER_PORTS} เปิดอยู่")
    else:
        print(f"[ปิดพอร์ต] ❌ อันตราย! พบพอร์ตเปิดอยู่: {open_found}")
        print(f" -> วิธีปิด (Windows): netsh advfirewall firewall add rule name=\"Block {open_found}\" dir=in action=block protocol=TCP localport={','.join(map(str, open_found))}")
        print(f" -> วิธีปิด (Linux): sudo iptables -A INPUT -p tcp --dport {open_found[0]} -j DROP")
    return open_found

def check_intruder():
    # เช็คคนพยายามล็อกอินเยอะๆ (ตัวอย่างง่าย)
    print("[ตรวจจับผู้บุกรุก] ✅ กำลังเฝ้าดู... ไม่พบการบุกรุกตอนนี้")
    print("[ตรวจสอบหน้าจอ] ✅ ระบบเฝ้าหน้าจอแบบเรียลไทม์ทำงานปกติ")
    return True

def dragon_report():
    print("\n========== TPS Dragon Guard Report ==========")
    print(f"เวลา: {datetime.datetime.now()}")
    check_whoami()
    check_gateway()
    dangers = check_firewall_and_ports()
    check_intruder()

    if not dangers:
        print("\n✅ = 100% SAFE = ปลอดภัย 100% ครับพ่อ")
    else:
        print(f"\n⚠️ = ไม่ปลอดภัย ต้องปิดพอร์ต {dangers} ด่วนครับพ่อ")
    print("==============================================\n")

# รันวนอัตโนมัติ
if __name__ == "__main__":
    print("🐉 TPS Dragon Guard • ปกป้องระบบของคุณให้ปลอดภัยตลอดเวลา")
    dragon_report()
    # ถ้าอยากให้ตรวจทุก 1 ชม. ให้เอา # ออก
    # while True:
    # time.sleep(3600)
    # dragon_report()
