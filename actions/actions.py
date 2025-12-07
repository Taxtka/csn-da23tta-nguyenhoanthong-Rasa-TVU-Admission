from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction

# --- DỮ LIỆU NGÀNH CHUẨN (Cấu trúc: Mô tả - Thời gian - Học phí) ---
MAJOR_DB = {

    # === KHỐI SỨC KHỎE ===

    "y khoa": {

        "desc": "Ngành Y khoa (Bác sĩ đa khoa) đào tạo bác sĩ có y đức, kiến thức chuyên sâu về chẩn đoán và điều trị bệnh.",

        "time": "6 năm (Bác sĩ)",

        "fee": "44.280.000 VNĐ/năm"

    },

    "răng hàm mặt": {

        "desc": "Ngành Răng - Hàm - Mặt đào tạo bác sĩ chuyên khoa về nha khoa, chấn thương hàm mặt.",

        "time": "6 năm (Bác sĩ)",

        "fee": "47.500.000 VNĐ/năm"

    },

    "dược học": {

        "desc": "Ngành Dược học đào tạo Dược sĩ đại học, chuyên về quản lý, cung ứng và tư vấn sử dụng thuốc an toàn, hiệu quả.",

        "time": "5 năm (Dược sĩ)",

        "fee": "38.500.000 VNĐ/năm"

    },

    "điều dưỡng": {

        "desc": "Ngành Điều dưỡng trang bị kiến thức chăm sóc sức khỏe, kiểm tra tình trạng bệnh nhân và hỗ trợ bác sĩ trong điều trị.",

        "time": "4 năm (Cử nhân)",

        "fee": "34.200.000 VNĐ/năm"

    },

    "kỹ thuật xét nghiệm y học": {

        "desc": "Ngành Kỹ thuật xét nghiệm y học đào tạo cử nhân có kỹ năng thực hiện các xét nghiệm y khoa phục vụ chẩn đoán bệnh.",

        "time": "4 năm (Cử nhân)",

        "fee": "36.500.000 VNĐ/năm"

    },

    "y học dự phòng": {

        "desc": "Ngành Y học dự phòng tập trung vào việc phòng chống bệnh tật, nâng cao sức khỏe cộng đồng và quản lý y tế.",

        "time": "6 năm (Bác sĩ)",

        "fee": "40.600.000 VNĐ/năm"

    },

    "y tế công cộng": {

        "desc": "Ngành Y tế công cộng đào tạo chuyên gia về quản lý hệ thống y tế, dịch tễ học và sức khỏe môi trường.",

        "time": "4 năm (Cử nhân)",

        "fee": "34.200.000 VNĐ/năm"

    },

    "kỹ thuật hình ảnh y học": {

        "desc": "Ngành này đào tạo kỹ thuật viên sử dụng các thiết bị hiện đại (X-Quang, MRI, CT) để chẩn đoán hình ảnh.",

        "time": "4 năm (Cử nhân)",

        "fee": "36.500.000 VNĐ/năm"

    },

    "kỹ thuật phục hồi chức năng": {

        "desc": "Đào tạo cử nhân Vật lý trị liệu và Phục hồi chức năng, giúp người bệnh hồi phục sau chấn thương hoặc phẫu thuật.",

        "time": "4 năm (Kỹ thuật viên)",

        "fee": "34.200.000 VNĐ/năm"

    },

    "dinh dưỡng": {

        "desc": "Ngành Dinh dưỡng đào tạo chuyên gia tư vấn chế độ ăn uống, dinh dưỡng lâm sàng và an toàn thực phẩm.",

        "time": "4 năm (Cử nhân)",

        "fee": "34.200.000 VNĐ/năm"

    },

    "hóa dược": {

        "desc": "Ngành Hóa dược kết hợp giữa Hóa học và Dược học, chuyên về nghiên cứu phát triển thuốc và kiểm nghiệm dược phẩm.",

        "time": "4 năm (Cử nhân)",

        "fee": "27.000.000 VNĐ/năm"

    },



    # === KHỐI KỸ THUẬT & CÔNG NGHỆ ===

    "công nghệ thông tin": {

        "desc": "Ngành CNTT (đạt chuẩn kiểm định quốc tế ABET) đào tạo kỹ sư phần mềm, an toàn thông tin, mạng máy tính. Cơ hội việc làm rất lớn.",

        "time": "3,5 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "trí tuệ nhân tạo": {

        "desc": "Ngành Trí tuệ nhân tạo (AI) là ngành mũi nhọn mới, đào tạo chuyên sâu về Machine Learning, Deep Learning và Khoa học dữ liệu.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "công nghệ kỹ thuật ô tô": {

        "desc": "Đào tạo kỹ sư có khả năng thiết kế, vận hành, bảo trì và sửa chữa ô tô. Sinh viên được thực hành tại xưởng hiện đại.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "công nghệ kỹ thuật cơ khí": {

        "desc": "Ngành Cơ khí trang bị kiến thức về thiết kế máy, gia công CNC và công nghệ chế tạo máy.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "công nghệ kỹ thuật điện điện tử": {

        "desc": "Đào tạo kỹ sư về hệ thống điện, điện tử công nghiệp và viễn thông.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "công nghệ kỹ thuật điều khiển và tự động hóa": {

        "desc": "Chuyên về các hệ thống điều khiển tự động, robot công nghiệp và PLC.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "công nghệ kỹ thuật công trình xây dựng": {

        "desc": "Đào tạo kỹ sư xây dựng dân dụng và công nghiệp, quản lý dự án xây dựng.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "kỹ thuật xây dựng công trình giao thông": {

        "desc": "Chuyên về thiết kế, thi công cầu đường và hạ tầng giao thông.",

        "time": "4.5 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "công nghệ kỹ thuật hóa học": {

        "desc": "Đào tạo về công nghệ hóa học, hóa dầu, vật liệu mới.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },



    # === KHỐI NÔNG NGHIỆP - THỦY SẢN - MÔI TRƯỜNG ===

    "nông nghiệp": {

        "desc": "Ngành Nông nghiệp (đạt chuẩn AUN-QA) đào tạo kỹ sư nông học, trồng trọt công nghệ cao và phát triển nông thôn.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "thú y": {

        "desc": "Ngành Thú y đào tạo Bác sĩ thú y, chuyên về chẩn đoán và phòng trị bệnh cho động vật, thú cưng.",

        "time": "5 năm (Bác sĩ thú y)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "nuôi trồng thủy sản": {

        "desc": "Ngành Nuôi trồng thủy sản (đạt chuẩn AUN-QA) là thế mạnh của vùng ĐBSCL, đào tạo kỹ thuật nuôi tôm, cá công nghệ cao.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "bảo vệ thực vật": {

        "desc": "Ngành này chuyên về phòng trừ sâu bệnh hại, bảo vệ mùa màng và an toàn nông sản.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "công nghệ thực phẩm": {

        "desc": "Chuyên về quy trình chế biến, bảo quản và kiểm định chất lượng thực phẩm, nông sản.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "công nghệ sinh học": {

        "desc": "Ứng dụng công nghệ sinh học trong y dược, nông nghiệp và môi trường.",

        "time": "4 năm (Cử nhân/Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "kỹ thuật môi trường": {

        "desc": "Đào tạo kỹ sư về xử lý nước thải, rác thải và quản lý tài nguyên môi trường.",

        "time": "4 năm (Kỹ sư)",

        "fee": "20.000.000 VNĐ/năm"

    },



    # === KHỐI KINH TẾ - LUẬT - LOGISTICS ===

    "quản trị kinh doanh": {

        "desc": "Ngành QTKD cung cấp kiến thức toàn diện về quản lý doanh nghiệp, marketing, nhân sự và khởi nghiệp.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "17.700.000 VNĐ/năm"

    },

    "tài chính ngân hàng": {

        "desc": "Đào tạo chuyên viên về tài chính, ngân hàng thương mại, đầu tư và thị trường chứng khoán.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "17.700.000 VNĐ/năm"

    },

    "kế toán": {

        "desc": "Ngành Kế toán đào tạo kế toán viên, kiểm toán viên chuyên nghiệp cho doanh nghiệp và cơ quan nhà nước.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "17.700.000 VNĐ/năm"

    },

    "kinh tế": {

        "desc": "Ngành Kinh tế nghiên cứu về kinh tế học, kinh tế phát triển và kinh tế quốc tế.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm (Quản lý kinh tế)"

    },

    "luật": {

        "desc": "Ngành Luật trang bị kiến thức pháp lý vững chắc (Luật Dân sự, Hình sự, Thương mại) để làm việc tại tòa án, viện kiểm sát hoặc công ty luật.",

        "time": "4 năm (Cử nhân)",

        "fee": "17.700.000 VNĐ/năm"

    },

    "logistics và quản lý chuỗi cung ứng": {

        "desc": "Ngành 'hot' về quản lý vận tải, kho bãi và chuỗi cung ứng toàn cầu.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "thương mại điện tử": {

        "desc": "Đào tạo kinh doanh trực tuyến, marketing số và thanh toán điện tử.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "17.700.000 VNĐ/năm"

    },

    "quản trị văn phòng": {

        "desc": "Đào tạo về nghiệp vụ văn phòng, hành chính, thư ký chuyên nghiệp.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "17.700.000 VNĐ/năm"

    },



    # === KHỐI DU LỊCH - KHÁCH SẠN ===

    "quản trị dịch vụ du lịch và lữ hành": {

        "desc": "Đào tạo chuyên viên quản lý, điều hành tour du lịch và hướng dẫn viên.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "quản trị khách sạn": {

        "desc": "Chuyên về quản lý vận hành khách sạn, resort và dịch vụ lưu trú.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "quản trị nhà hàng và dịch vụ ăn uống": {

        "desc": "Đào tạo kỹ năng quản lý nhà hàng, nghệ thuật ẩm thực và dịch vụ ăn uống.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },



    # === KHỐI NGÔN NGỮ - VĂN HÓA - NGHỆ THUẬT ===

    "ngôn ngữ anh": {

        "desc": "Ngành Ngôn ngữ Anh (Biên-Phiên dịch, Tiếng Anh thương mại) mở ra cơ hội làm việc toàn cầu.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "ngôn ngữ trung quốc": {

        "desc": "Đào tạo thành thạo tiếng Trung, phục vụ giao thương và văn hóa với Trung Quốc.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "ngôn ngữ khmer": {

        "desc": "Ngành đặc thù đào tạo chuyên gia về ngôn ngữ và văn hóa Khmer Nam Bộ.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "văn hóa học": {

        "desc": "Nghiên cứu về văn hóa Việt Nam và thế giới, quản lý văn hóa, tổ chức sự kiện.",

        "time": "3.5 - 4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "âm nhạc học": {

        "desc": "Đào tạo về lý luận âm nhạc, phê bình và nghiên cứu âm nhạc.",

        "time": "4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    "biểu diễn nhạc cụ truyền thống": {

        "desc": "Đào tạo nghệ sĩ biểu diễn các nhạc cụ dân tộc chuyên nghiệp.",

        "time": "4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },



    # === KHỐI SƯ PHẠM & XÃ HỘI (ĐƯỢC MIỄN HỌC PHÍ) ===

    "giáo dục mầm non": {

        "desc": "Đào tạo giáo viên mầm non có kỹ năng chăm sóc và giáo dục trẻ nhỏ.",

        "time": "3 - 4 năm (Cử nhân)",

        "fee": "✅ **Được MIỄN HỌC PHÍ** và hỗ trợ sinh hoạt phí theo Nghị định 116/2020/NĐ-CP."

    },

    "giáo dục tiểu học": {

        "desc": "Đào tạo giáo viên dạy cấp Tiểu học.",

        "time": "4 năm (Cử nhân)",

        "fee": "✅ **Được MIỄN HỌC PHÍ** và hỗ trợ sinh hoạt phí theo Nghị định 116/2020/NĐ-CP."

    },

    "sư phạm ngữ văn": {

        "desc": "Đào tạo giáo viên môn Ngữ văn cho các trường phổ thông.",

        "time": "4 năm (Cử nhân)",

        "fee": "✅ **Được MIỄN HỌC PHÍ** và hỗ trợ sinh hoạt phí theo Nghị định 116/2020/NĐ-CP."

    },

    "sư phạm tiếng khmer": {

        "desc": "Đào tạo giáo viên dạy tiếng Khmer.",

        "time": "4 năm (Cử nhân)",

        "fee": "✅ **Được MIỄN HỌC PHÍ** và hỗ trợ sinh hoạt phí theo Nghị định 116/2020/NĐ-CP."

    },

    "công tác xã hội": {

        "desc": "Ngành CTXH đào tạo nhân viên xã hội chuyên nghiệp, hỗ trợ cộng đồng và các nhóm yếu thế.",

        "time": "4 năm (Cử nhân)",

        "fee": "20.000.000 VNĐ/năm"

    },

    

    # Các ngành khác trong danh sách bạn gửi

    "chính trị học": {

        "desc": "Nghiên cứu các vấn đề về chính trị, xây dựng Đảng và chính quyền nhà nước.",

        "time": "4 năm",

        "fee": "20.000.000 VNĐ/năm"

    },

    "quản lý nhà nước": {

        "desc": "Đào tạo cán bộ quản lý hành chính nhà nước, chính sách công.",

        "time": "4 năm",

        "fee": "20.000.000 VNĐ/năm"

    },

    "quản lý thể dục thể thao": {

        "desc": "Đào tạo về tổ chức, quản lý các hoạt động thể dục thể thao.",

        "time": "4 năm",

        "fee": "20.000.000 VNĐ/năm"

    },

    "quản lý tài nguyên và môi trường": {

        "desc": "Đào tạo về quản lý đất đai, tài nguyên nước và bảo vệ môi trường.",

        "time": "4 năm",

        "fee": "20.000.000 VNĐ/năm"

    }
}

# Hàm tìm kiếm dùng chung
def find_major_data(major_raw):
    if not major_raw: return None, None
    major_clean = major_raw.lower().strip()
    # Tìm chính xác trước
    if major_clean in MAJOR_DB:
        return major_clean, MAJOR_DB[major_clean]
    # Tìm gần đúng
    for key, data in MAJOR_DB.items():
        if key in major_clean or major_clean in key:
            return key, data
    return major_raw, None

# --- ACTION 1: GIỚI THIỆU + HIỆN NÚT BẤM ---
class ActionProvideMajorInfo(Action):
    def name(self) -> Text:
        return "action_provide_major_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # 1. Bộ lọc chuyển hướng (Học bổng/Xét tuyển)
        if "học bổng" in user_message or "ưu đãi" in user_message:
            return [FollowupAction("utter_ask_scholarship")]
        if "xét tuyển" in user_message or "phương thức" in user_message:
            return [FollowupAction("utter_tra_loi_xet_tuyen")]

        # 2. Xử lý Ngành học
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        major_name, data = find_major_data(major_entity)

        if data:
            # Tìm thấy -> Hiện mô tả
            msg = f"📚 **Thông tin ngành {major_name}:**\n{data['desc']}\n\nBạn muốn xem thêm thông tin gì?"
            
            # TẠO 2 NÚT BẤM (Magic Buttons)
            # Chú ý: Dùng {{ }} để tránh lỗi KeyError trong Python
            buttons = [
                {"title": "⏳ Thời gian đào tạo", "payload": f'/ask_training_duration{{"major":"{major_name}"}}'},
                {"title": "💰 Xem Học phí", "payload": f'/ask_tuition{{"major":"{major_name}"}}'}
            ]
            dispatcher.utter_message(text=msg, buttons=buttons)
        else:
            dispatcher.utter_message(text=f"Xin lỗi, mình chưa tìm thấy thông tin ngành '{major_name}'.")
        
        return []

# --- ACTION 2: TRẢ LỜI THỜI GIAN ---
class ActionProvideDuration(Action):
    def name(self) -> Text:
        return "action_provide_duration"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        major_name, data = find_major_data(major_entity)
        
        if data:
            dispatcher.utter_message(text=f"⏳ Thời gian đào tạo ngành **{major_name}** là: **{data['time']}**.")
        else:
            dispatcher.utter_message(text="Bạn vui lòng chọn tên ngành trước nhé.")
        return []

# --- ACTION 3: TRẢ LỜI HỌC PHÍ ---
class ActionProvideTuition(Action):
    def name(self) -> Text:
        return "action_provide_tuition"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        major_name, data = find_major_data(major_entity)
        
        if data:
            dispatcher.utter_message(text=f"💰 Học phí tham khảo ngành **{major_name}** là: **{data['fee']}**.")
        else:
            dispatcher.utter_message(text="Bạn vui lòng chọn tên ngành trước nhé.")
        return []