from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet

# DỮ LIỆU NGÀNH (Cấu trúc: Mô tả - Thời gian - Học phí, Chương trình đào tạo)
MAJOR_DB = {
    # 1. KHỐI SỨC KHỎE (Health Sciences)
    "y khoa": {
        "desc": "Ngành Y khoa đào tạo Bác sĩ đa khoa có y đức, kiến thức khoa học cơ bản và y học cơ sở vững chắc.",
        "time": "6 năm (Bác sĩ)",
        "fee": "44.280.000 VNĐ/năm",
        "skills": """
        - Chẩn đoán, điều trị và phòng bệnh cho cá nhân và cộng đồng.
        - Kỹ năng ra quyết định lâm sàng và xử lý tình huống cấp cứu.
        - Kỹ năng giao tiếp y khoa, tư vấn sức khỏe cho người bệnh.
        - Sử dụng thành thạo các thiết bị y tế chẩn đoán cơ bản.
        """,
        "career": """
        - Bác sĩ điều trị tại các bệnh viện công lập và tư nhân, trung tâm y tế.
        - Giảng viên tại các trường Đại học, Cao đẳng Y Dược.
        - Chuyên viên tại các Sở Y tế, phòng khám đa khoa.
        - Nghiên cứu viên tại các viện nghiên cứu y học.
        """
    },
    "răng hàm mặt": {
        "desc": "Đào tạo Bác sĩ Răng Hàm Mặt chuyên sâu về chẩn đoán, điều trị các bệnh lý và thẩm mỹ răng miệng.",
        "time": "6 năm (Bác sĩ)",
        "fee": "47.500.000 VNĐ/năm",
        "skills": """
        - Chẩn đoán và điều trị sâu răng, nha chu, phẫu thuật hàm mặt.
        - Kỹ năng phục hình răng, chỉnh nha và thẩm mỹ nha khoa.
        - Sử dụng các thiết bị nha khoa công nghệ cao.
        - Quản lý phòng khám nha khoa tư nhân.
        """,
        "career": """
        - Bác sĩ tại khoa Răng Hàm Mặt các bệnh viện.
        - Làm việc tại các phòng khám nha khoa, trung tâm thẩm mỹ.
        - Mở phòng khám nha khoa tư nhân.
        - Giảng dạy và nghiên cứu về nha khoa.
        """
    },
    "dược học": {
        "desc": "Đào tạo Dược sĩ đại học am hiểu về thuốc, quy trình sản xuất, kiểm nghiệm và tư vấn sử dụng thuốc.",
        "time": "5 năm (Dược sĩ)",
        "fee": "38.500.000 VNĐ/năm",
        "skills": """
        - Bào chế, sản xuất và kiểm nghiệm chất lượng thuốc.
        - Tư vấn hướng dẫn sử dụng thuốc an toàn, hợp lý (Dược lâm sàng).
        - Quản lý, kinh doanh và cung ứng dược phẩm.
        """,
        "career": """
        - Dược sĩ lâm sàng tại bệnh viện.
        - Làm việc tại các nhà máy sản xuất dược phẩm, công ty phân phối thuốc.
        - Quản lý nhà thuốc, chuỗi bán lẻ dược phẩm (Long Châu, Pharmacity...).
        - Chuyên viên kiểm nghiệm thuốc, mỹ phẩm.
        """
    },
    "điều dưỡng": {
        "desc": "Đào tạo Cử nhân Điều dưỡng có khả năng chăm sóc, theo dõi sức khỏe và hỗ trợ điều trị cho bệnh nhân.",
        "time": "4 năm (Cử nhân)",
        "fee": "34.200.000 VNĐ/năm",
        "skills": """
        - Thực hiện các quy trình chăm sóc điều dưỡng cơ bản và nâng cao.
        - Theo dõi diễn biến bệnh, sơ cấp cứu ban đầu.
        - Tư vấn, giáo dục sức khỏe cho người bệnh và cộng đồng.
        """,
        "career": """
        - Điều dưỡng viên tại các bệnh viện, trung tâm y tế, trạm y tế.
        - Điều dưỡng trưởng quản lý khoa/phòng.
        - Chăm sóc sức khỏe tại gia đình, viện dưỡng lão (cơ hội đi Đức, Nhật rất lớn).
        """
    },
    "kỹ thuật xét nghiệm y học": {
        "desc": "Đào tạo Kỹ thuật viên xét nghiệm thực hiện các kỹ thuật phân tích mẫu bệnh phẩm hỗ trợ chẩn đoán.",
        "time": "4 năm (Cử nhân)",
        "fee": "36.500.000 VNĐ/năm",
        "skills": """
        - Vận hành trang thiết bị xét nghiệm huyết học, sinh hóa, vi sinh.
        - Pha chế hóa chất, kiểm tra chất lượng xét nghiệm.
        - Phân tích và quản lý dữ liệu kết quả xét nghiệm.
        """,
        "career": """
        - Kỹ thuật viên tại khoa xét nghiệm bệnh viện, trung tâm y tế dự phòng.
        - Chuyên viên ứng dụng sản phẩm tại các công ty thiết bị y tế.
        - Làm việc tại các phòng Lab, viện nghiên cứu.
        """
    },
    "y học dự phòng": {
        "desc": "Đào tạo Bác sĩ Y học dự phòng tập trung vào kiểm soát dịch bệnh và nâng cao sức khỏe cộng đồng.",
        "time": "6 năm (Bác sĩ)",
        "fee": "40.600.000 VNĐ/năm",
        "skills": """
        - Giám sát, phát hiện và kiểm soát dịch bệnh truyền nhiễm.
        - Lập kế hoạch và triển khai các chương trình y tế quốc gia.
        - Truyền thông giáo dục sức khỏe cộng đồng.
        """,
        "career": """
        - Làm việc tại Trung tâm kiểm soát bệnh tật (CDC), Trung tâm y tế dự phòng.
        - Bác sĩ tại các trạm y tế, trung tâm y tế huyện.
        - Chuyên viên các dự án y tế phi chính phủ (NGOs).
        """
    },
    "y tế công cộng": {
        "desc": "Chuyên ngành quản lý hệ thống y tế, chính sách sức khỏe và môi trường.",
        "time": "4 năm (Cử nhân)",
        "fee": "34.200.000 VNĐ/năm",
        "skills": """
        - Phân tích tình hình sức khỏe cộng đồng và các yếu tố nguy cơ.
        - Quản lý dự án y tế, quản lý bệnh viện.
        - Điều tra dịch tễ học và thống kê y tế.
        """,
        "career": """
        - Cán bộ quản lý tại Sở Y tế, Bệnh viện.
        - Chuyên viên an toàn vệ sinh lao động, vệ sinh môi trường.
        - Làm việc tại các tổ chức y tế quốc tế (WHO, UNICEF).
        """
    },
    "kỹ thuật hình ảnh y học": {
        "desc": "Sử dụng máy móc hiện đại (X-Quang, CT, MRI) để chụp và chẩn đoán hình ảnh cơ thể người.",
        "time": "4 năm (Cử nhân)",
        "fee": "36.500.000 VNĐ/năm",
        "skills": """
        - Vận hành máy X-Quang, Cắt lớp vi tính (CT), Cộng hưởng từ (MRI), Siêu âm.
        - Kỹ năng an toàn bức xạ và xử lý hình ảnh y tế.
        """,
        "career": """
        - Kỹ thuật viên chẩn đoán hình ảnh tại bệnh viện, phòng khám.
        - Chuyên viên kỹ thuật ứng dụng tại các hãng thiết bị (GE, Siemens, Philips).
        """
    },
    "kỹ thuật phục hồi chức năng": {
        "desc": "Đào tạo chuyên gia Vật lý trị liệu giúp bệnh nhân phục hồi chức năng vận động sau chấn thương/tai biến.",
        "time": "4 năm (Cử nhân)",
        "fee": "34.200.000 VNĐ/năm",
        "skills": """
        - Thực hiện các kỹ thuật vật lý trị liệu, vận động trị liệu.
        - Sử dụng thiết bị phục hồi chức năng (điện xung, siêu âm trị liệu).
        - Lập kế hoạch phục hồi cho bệnh nhân tai biến, chấn thương thể thao.
        """,
        "career": """
        - Làm việc tại khoa Phục hồi chức năng các bệnh viện.
        - Trung tâm chăm sóc sức khỏe, spa trị liệu, đội thể thao.
        - Bệnh viện chỉnh hình và phục hồi chức năng.
        """
    },
    "dinh dưỡng": {
        "desc": "Đào tạo chuyên gia tư vấn chế độ ăn uống, dinh dưỡng lâm sàng cho người bệnh và cộng đồng.",
        "time": "4 năm (Cử nhân)",
        "fee": "34.200.000 VNĐ/năm",
        "skills": """
        - Xây dựng thực đơn dinh dưỡng cho từng đối tượng (trẻ em, người già, người bệnh).
        - Tư vấn dinh dưỡng và an toàn thực phẩm.
        - Kiểm soát chế độ ăn tại bếp ăn công nghiệp, bệnh viện.
        """,
        "career": """
        - Chuyên gia dinh dưỡng tại bệnh viện, trường học, trung tâm thể thao.
        - Tư vấn viên tại các trung tâm dinh dưỡng.
        - Làm việc tại các công ty thực phẩm, sữa (Vinamilk, Nutifood).
        """
    },
    "hóa dược": {
        "desc": "Ngành giao thoa giữa Hóa học và Dược học, chuyên về nghiên cứu phát triển và sản xuất nguyên liệu thuốc.",
        "time": "4 năm (Cử nhân)",
        "fee": "27.000.000 VNĐ/năm",
        "skills": """
        - Tổng hợp hóa dược, chiết xuất dược liệu.
        - Phân tích kiểm nghiệm mỹ phẩm, dược phẩm.
        - Kỹ thuật bào chế các dạng thuốc mới.
        """,
        "career": """
        - Kỹ sư R&D (nghiên cứu phát triển) tại công ty dược.
        - Kiểm nghiệm viên tại các trung tâm kiểm nghiệm thuốc.
        - Làm việc trong lĩnh vực hóa mỹ phẩm, thực phẩm chức năng.
        """
    },
    # 2. KHỐI KỸ THUẬT & CÔNG NGHỆ (Engineering & Technology)
    "công nghệ thông tin": {
        "desc": "Ngành CNTT đào tạo kỹ sư phần mềm, hệ thống thông tin, mạng máy tính (Kiểm định quốc tế ABET).",
        "time": "3,5 - 4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Vận dụng tri thức khoa học máy tính, quản lý dự án để giải quyết vấn đề kỹ thuật.
        - Nắm vững vai trò hệ thống thông tin trong các tổ chức.
        - Phân tích và mô hình hóa quy trình dữ liệu.
        - Vận dụng các công cụ trong việc đặc tả, phân tích, xây dựng và bảo trì hệ thống.
        - Lập trình (Web, Mobile, AI) và quản trị cơ sở dữ liệu.
        """,
        "career": """
        - Lập trình viên (Developer) tại các công ty phần mềm (FPT, Viettel...).
        - Chuyên viên quản trị mạng, an ninh mạng.
        - Chuyên viên phân tích thiết kế hệ thống (BA).
        - Giảng dạy tin học hoặc Khởi nghiệp công nghệ (Startup).
        """
    },
    "trí tuệ nhân tạo": {
        "desc": "Đào tạo chuyên sâu về AI, Học máy (Machine Learning) và Khoa học dữ liệu (Data Science).",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Xây dựng các mô hình học máy, học sâu (Deep Learning).
        - Xử lý ngôn ngữ tự nhiên (NLP) và thị giác máy tính (Computer Vision).
        - Khai phá dữ liệu lớn (Big Data).
        """,
        "career": """
        - Kỹ sư AI/Machine Learning tại các tập đoàn công nghệ.
        - Chuyên gia phân tích dữ liệu (Data Scientist).
        - Phát triển ứng dụng thông minh (chatbot, nhận diện khuôn mặt, xe tự lái).
        """
    },
    "công nghệ kỹ thuật ô tô": {
        "desc": "Đào tạo kỹ sư thiết kế, chế tạo, khai thác và sửa chữa ô tô (Có xưởng thực hành hiện đại).",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Chẩn đoán, bảo dưỡng và sửa chữa động cơ, hệ thống điện ô tô.
        - Kiểm định kỹ thuật và dịch vụ ô tô.
        - Thiết kế và cải tiến các hệ thống trên ô tô.
        """,
        "career": """
        - Kỹ sư vận hành tại các nhà máy lắp ráp (VinFast, Toyota, Hyundai).
        - Cố vấn dịch vụ, Kỹ thuật viên tại các Showroom/Garage 4S.
        - Đăng kiểm viên tại các trung tâm đăng kiểm xe cơ giới.
        """
    },
    "công nghệ kỹ thuật cơ khí": {
        "desc": "Trang bị kiến thức về thiết kế máy, gia công chế tạo và cơ khí chính xác.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Thiết kế máy trên phần mềm 3D (CAD/CAM/CNC).
        - Vận hành máy tiện, phay, bào và máy CNC hiện đại.
        - Bảo trì hệ thống dây chuyền sản xuất công nghiệp.
        """,
        "career": """
        - Kỹ sư thiết kế cơ khí, kỹ sư chế tạo máy.
        - Quản lý kỹ thuật tại các nhà máy sản xuất, khu công nghiệp.
        - Kỹ sư bảo trì hệ thống cơ điện.
        """
    },
    "công nghệ kỹ thuật điện điện tử": {
        "desc": "Đào tạo về hệ thống điện công nghiệp, điện tử viễn thông và năng lượng tái tạo.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Thiết kế, lắp đặt hệ thống cung cấp điện tòa nhà, nhà máy.
        - Vận hành hệ thống điện tử công suất, vi mạch.
        - Kỹ năng về năng lượng mặt trời, năng lượng gió.
        """,
        "career": """
        - Kỹ sư điện tại các nhà máy, công ty điện lực (EVN).
        - Kỹ sư thiết kế mạch điện tử, viễn thông.
        - Quản lý vận hành hệ thống điện tòa nhà (M&E).
        """
    },
    "công nghệ kỹ thuật điều khiển và tự động hóa": {
        "desc": "Chuyên ngành về Robot, dây chuyền sản xuất tự động và hệ thống điều khiển thông minh.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Lập trình PLC, vi điều khiển, cánh tay Robot công nghiệp.
        - Thiết kế hệ thống điều khiển tự động hóa (SCADA, BMS).
        - Tích hợp hệ thống đo lường và cảm biến.
        """,
        "career": """
        - Kỹ sư lập trình Robot, vận hành dây chuyền sản xuất tự động.
        - Kỹ sư thiết kế hệ thống điều khiển tại các nhà máy.
        - Làm việc tại các công ty giải pháp tự động hóa (Siemens, Rockwell).
        """
    },
    "công nghệ kỹ thuật công trình xây dựng": {
        "desc": "Đào tạo Kỹ sư xây dựng dân dụng và công nghiệp (nhà ở, nhà xưởng, cao ốc).",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Tính toán kết cấu, thiết kế bản vẽ thi công.
        - Tổ chức thi công, giám sát và quản lý dự án xây dựng.
        - Sử dụng phần mềm xây dựng (AutoCAD, Revit, Etabs).
        """,
        "career": """
        - Kỹ sư thiết kế kết cấu, kiến trúc sư công trình.
        - Chỉ huy trưởng công trường, giám sát thi công.
        - Làm việc tại các Ban quản lý dự án, Sở Xây dựng.
        """
    },
    "kỹ thuật xây dựng công trình giao thông": {
        "desc": "Chuyên về thiết kế, thi công cầu, đường bộ, đường cao tốc và hạ tầng giao thông.",
        "time": "4.5 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Khảo sát địa hình, thiết kế trắc dọc, trắc ngang cầu đường.
        - Kỹ thuật thi công đường nhựa, cầu bê tông cốt thép.
        - Kiểm định chất lượng công trình giao thông.
        """,
        "career": """
        - Kỹ sư cầu đường tại các công ty tư vấn thiết kế, thi công giao thông.
        - Cán bộ kỹ thuật tại các Ban quản lý dự án giao thông.
        - Làm việc tại Sở Giao thông vận tải.
        """
    },
    "công nghệ kỹ thuật hóa học": {
        "desc": "Nghiên cứu công nghệ sản xuất hóa chất, phân bón, vật liệu mới và lọc hóa dầu.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Vận hành quy trình sản xuất hóa chất, thực phẩm, dược phẩm.
        - Phân tích hóa lý, kiểm tra chất lượng sản phẩm.
        - Thiết kế thiết bị phản ứng hóa học.
        """,
        "career": """
        - Kỹ sư vận hành tại nhà máy đạm, lọc hóa dầu, xi măng.
        - Chuyên viên phòng thí nghiệm phân tích.
        - Kinh doanh hóa chất và thiết bị khoa học kỹ thuật.
        """
    },
    # 3. KHỐI NÔNG NGHIỆP - THỦY SẢN - MÔI TRƯỜNG
    "nông nghiệp": {
        "desc": "Ngành Nông nghiệp (Kiểm định AUN-QA) đào tạo kỹ sư nông học, trồng trọt công nghệ cao.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Kỹ thuật trồng trọt, nhân giống cây trồng (nuôi cấy mô).
        - Ứng dụng công nghệ cao (nhà màng, thủy canh) vào sản xuất.
        - Quản lý trang trại và kinh doanh nông nghiệp.
        """,
        "career": """
        - Kỹ sư nông nghiệp tại các nông trường, công ty giống cây trồng.
        - Cán bộ khuyến nông, phòng Nông nghiệp địa phương.
        - Làm chủ trang trại (Farm) hoặc khởi nghiệp nông nghiệp sạch.
        """
    },
    "thú y": {
        "desc": "Đào tạo Bác sĩ thú y chuyên về chẩn đoán, phòng trị bệnh động vật và kiểm soát dịch bệnh.",
        "time": "5 năm (Bác sĩ)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Chẩn đoán lâm sàng, phẫu thuật ngoại khoa trên thú nhỏ và gia súc.
        - Kiểm nghiệm thú sản, vệ sinh an toàn thực phẩm.
        - Kinh doanh thuốc thú y và thức ăn chăn nuôi.
        """,
        "career": """
        - Bác sĩ tại phòng khám thú y (Pet clinic), bệnh viện thú y.
        - Làm việc tại chi cục Thú y, trạm kiểm dịch động vật.
        - Kỹ thuật tại các trại chăn nuôi quy mô lớn (CP, Japfa).
        """
    },
    "nuôi trồng thủy sản": {
        "desc": "Ngành mũi nhọn vùng ĐBSCL (Kiểm định AUN-QA), chuyên sâu về nuôi tôm, cá công nghệ cao.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Kỹ thuật sản xuất giống và nuôi thương phẩm tôm, cá, cua...
        - Quản lý môi trường nước và phòng trị bệnh thủy sản.
        - Thiết kế hệ thống nuôi thủy sản tuần hoàn.
        """,
        "career": """
        - Kỹ sư trại giống, trại nuôi của các tập đoàn lớn (Việt Úc, Minh Phú).
        - Kinh doanh thức ăn, thuốc thủy sản.
        - Cán bộ quản lý thủy sản tại địa phương.
        """
    },
    "bảo vệ thực vật": {
        "desc": "Chuyên về bác sĩ cây trồng, phòng trừ sâu bệnh hại và bảo vệ mùa màng.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Nhận diện và chẩn đoán bệnh hại trên cây trồng.
        - Sử dụng thuốc bảo vệ thực vật an toàn, hiệu quả.
        - Quy trình kiểm dịch thực vật xuất nhập khẩu.
        """,
        "career": """
        - Cán bộ Chi cục Bảo vệ thực vật, Trạm kiểm dịch.
        - Kỹ sư kỹ thuật tại các công ty thuốc BVTV (Lộc Trời, Syngenta).
        - Tư vấn kỹ thuật cho nông dân và trang trại.
        """
    },
    "công nghệ thực phẩm": {
        "desc": "Nghiên cứu quy trình chế biến, bảo quản nông sản và phát triển sản phẩm thực phẩm mới.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Vận hành dây chuyền sản xuất thực phẩm (sữa, đồ hộp, thủy sản đông lạnh).
        - Kiểm soát chất lượng thực phẩm (QA/QC), HACCP, ISO.
        - Nghiên cứu phát triển sản phẩm mới (R&D).
        """,
        "career": """
        - Kỹ sư công nghệ tại các nhà máy chế biến thực phẩm.
        - Chuyên viên kiểm định vệ sinh an toàn thực phẩm.
        - Quản lý bếp ăn công nghiệp hoặc suất ăn hàng không.
        """
    },
    "công nghệ sinh học": {
        "desc": "Ứng dụng sinh học vào đời sống: Lai tạo giống, chế phẩm sinh học, xét nghiệm ADN.",
        "time": "4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Kỹ thuật di truyền, nuôi cấy mô tế bào.
        - Sản xuất chế phẩm sinh học phục vụ nông nghiệp, xử lý môi trường.
        - Kiểm nghiệm vi sinh vật.
        """,
        "career": """
        - Nghiên cứu viên tại các viện công nghệ sinh học.
        - Làm việc tại các trung tâm xét nghiệm, thụ tinh nhân tạo.
        - Công ty sản xuất giống cây trồng, nấm, vắc-xin.
        """
    },
    "kỹ thuật môi trường": {
        "desc": "Đào tạo kỹ sư chuyên xử lý ô nhiễm nước, khí thải, rác thải và quản lý môi trường.",
        "time": "4 năm (Kỹ sư)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Thiết kế hệ thống xử lý nước thải, khí thải.
        - Đánh giá tác động môi trường (ĐTM).
        - Quan trắc và phân tích chỉ tiêu môi trường.
        """,
        "career": """
        - Kỹ sư vận hành trạm xử lý nước thải khu công nghiệp.
        - Chuyên viên Sở Tài nguyên Môi trường, Cảnh sát môi trường.
        - Tư vấn giải pháp môi trường cho doanh nghiệp.
        """
    },
    "quản lý tài nguyên và môi trường": {
        "desc": "Chuyên về quản lý đất đai, tài nguyên nước và ứng phó biến đổi khí hậu.",
        "time": "4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Quy hoạch sử dụng đất, cấp giấy chứng nhận quyền sử dụng đất.
        - Ứng dụng GIS và viễn thám trong quản lý tài nguyên.
        - Quản lý tài nguyên nước và khoáng sản.
        """,
        "career": """
        - Cán bộ địa chính xã/phường, Phòng Tài nguyên Môi trường.
        - Làm việc tại các Trung tâm kỹ thuật tài nguyên đất, Văn phòng đăng ký đất đai.
        - Công ty đo đạc bản đồ, bất động sản.
        """
    },
    # 4. KHỐI KINH TẾ - LUẬT - LOGISTICS
    "quản trị kinh doanh": {
        "desc": "Cung cấp kiến thức toàn diện về quản trị doanh nghiệp, marketing, nhân sự và chiến lược.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "17.700.000 VNĐ/năm",
        "skills": """
        - Lập kế hoạch kinh doanh, xây dựng chiến lược phát triển.
        - Kỹ năng lãnh đạo, quản lý nhân sự và đàm phán.
        - Marketing căn bản và bán hàng.
        """,
        "career": """
        - Nhân viên kinh doanh, Sale Manager.
        - Chuyên viên Marketing, PR, Nhân sự.
        - Tự khởi nghiệp (Startup) hoặc tiếp quản doanh nghiệp gia đình.
        - CEO, Giám đốc điều hành tương lai.
        """
    },
    "tài chính ngân hàng": {
        "desc": "Đào tạo chuyên sâu về thị trường tài chính, hoạt động ngân hàng và đầu tư.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "17.700.000 VNĐ/năm",
        "skills": """
        - Phân tích báo cáo tài chính, thẩm định tín dụng.
        - Giao dịch ngân hàng, thanh toán quốc tế.
        - Tư vấn đầu tư chứng khoán, bảo hiểm.
        """,
        "career": """
        - Giao dịch viên, Chuyên viên tín dụng tại các Ngân hàng.
        - Chuyên viên tài chính doanh nghiệp.
        - Môi giới chứng khoán, tư vấn bảo hiểm.
        """
    },
    "kế toán": {
        "desc": "Đào tạo Kế toán viên nắm vững chuẩn mực kế toán, thuế và kiểm toán.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "17.700.000 VNĐ/năm",
        "skills": """
        - Lập và phân tích báo cáo tài chính.
        - Kê khai thuế, quyết toán thuế.
        - Sử dụng phần mềm kế toán (MISA, Fast...).
        """,
        "career": """
        - Kế toán viên, Kế toán trưởng tại mọi loại hình doanh nghiệp.
        - Kiểm toán viên tại các công ty kiểm toán.
        - Chuyên viên tư vấn thuế.
        """
    },
    "kinh tế": {
        "desc": "Nghiên cứu về kinh tế học, phân tích vĩ mô/vi mô và kinh tế phát triển.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Phân tích dữ liệu kinh tế, dự báo xu hướng thị trường.
        - Hoạch định chính sách kinh tế.
        - Thẩm định dự án đầu tư.
        """,
        "career": """
        - Chuyên viên phân tích kinh tế tại các cơ quan nhà nước, viện nghiên cứu.
        - Làm việc tại các quỹ đầu tư, ngân hàng.
        - Giảng dạy các môn kinh tế.
        """
    },
    "luật": {
        "desc": "Trang bị tư duy pháp lý, kiến thức về Luật Dân sự, Hình sự, Thương mại, Hành chính.",
        "time": "4 năm (Cử nhân)",
        "fee": "17.700.000 VNĐ/năm",
        "skills": """
        - Tư vấn pháp luật, soạn thảo hợp đồng.
        - Tranh tụng và giải quyết tranh chấp.
        - Nghiên cứu hồ sơ vụ án.
        """,
        "career": """
        - Luật sư, Thẩm phán, Kiểm sát viên (sau khi học thêm nghiệp vụ).
        - Chuyên viên pháp chế tại các doanh nghiệp (In-house Counsel).
        - Công chứng viên, Thừa phát lại.
        - Cán bộ tư pháp hộ tịch.
        """
    },
    "logistics và quản lý chuỗi cung ứng": {
        "desc": "Ngành 'hot' về quản lý dòng chảy hàng hóa, vận tải, kho bãi và xuất nhập khẩu.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Quản trị kho hàng, vận tải và phân phối.
        - Nghiệp vụ xuất nhập khẩu, khai báo hải quan.
        - Tối ưu hóa chuỗi cung ứng.
        """,
        "career": """
        - Nhân viên xuất nhập khẩu, chứng từ (Docs), hiện trường (Ops).
        - Quản lý kho, điều phối vận tải.
        - Làm việc tại các cảng biển, công ty Logistics (DHL, Fedex...).
        """
    },
    "thương mại điện tử": {
        "desc": "Kết hợp giữa Kinh doanh và Công nghệ, tập trung vào bán hàng trực tuyến và Marketing số.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "17.700.000 VNĐ/năm",
        "skills": """
        - Xây dựng và quản lý website bán hàng, gian hàng trên sàn TMĐT (Shopee, Amazon).
        - Digital Marketing (SEO, chạy quảng cáo FB/Google/TikTok).
        - Thanh toán điện tử.
        """,
        "career": """
        - Chuyên viên kinh doanh online, phát triển sàn TMĐT.
        - Digital Marketer.
        - Khởi nghiệp kinh doanh trên nền tảng số.
        """
    },
    "quản trị văn phòng": {
        "desc": "Đào tạo nghiệp vụ hành chính, thư ký và quản trị thông tin trong tổ chức.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "17.700.000 VNĐ/năm",
        "skills": """
        - Soạn thảo văn bản, lưu trữ hồ sơ.
        - Tổ chức sự kiện, hội nghị, lễ tân văn phòng.
        - Kỹ năng thư ký tổng hợp.
        """,
        "career": """
        - Thư ký, Trợ lý giám đốc.
        - Nhân viên hành chính - nhân sự.
        - Cán bộ văn thư lưu trữ tại các cơ quan nhà nước.
        """
    },
    # 5. KHỐI DU LỊCH - KHÁCH SẠN
    "quản trị dịch vụ du lịch và lữ hành": {
        "desc": "Đào tạo chuyên sâu về tổ chức, điều hành tour và hướng dẫn du lịch.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Thiết kế và điều hành chương trình du lịch.
        - Kỹ năng hướng dẫn viên du lịch (thuyết minh, hoạt náo).
        - Sales và Marketing du lịch.
        """,
        "career": """
        - Hướng dẫn viên du lịch (Nội địa & Quốc tế).
        - Nhân viên điều hành tour (Operator), Sale Tour.
        - Làm việc tại Sở Văn hóa Thể thao Du lịch.
        """
    },
    "quản trị khách sạn": {
        "desc": "Chuyên về quản lý vận hành khách sạn, resort theo tiêu chuẩn quốc tế.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Nghiệp vụ Lễ tân, Buồng phòng, Bàn.
        - Quản lý tiền sảnh, quản lý doanh thu khách sạn.
        - Kỹ năng giao tiếp khách hàng chuyên nghiệp.
        """,
        "career": """
        - Quản lý khách sạn, Resort, Homestay.
        - Giám sát bộ phận Lễ tân, Buồng phòng.
        - Làm việc trên các du thuyền 5 sao.
        """
    },
    "quản trị nhà hàng và dịch vụ ăn uống": {
        "desc": "Tập trung vào quản lý F&B, nghệ thuật ẩm thực và dịch vụ yến tiệc.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Quản lý vận hành nhà hàng, bar, cafe.
        - Kiến thức về ẩm thực, pha chế đồ uống (Bartender/Barista).
        - Tổ chức sự kiện, tiệc cưới.
        """,
        "career": """
        - Quản lý nhà hàng, chuỗi cửa hàng ăn uống (F&B Manager).
        - Chuyên gia pha chế hoặc Bếp trưởng.
        - Khởi nghiệp kinh doanh quán Cafe, Nhà hàng.
        """
    },
    # 6. KHỐI NGÔN NGỮ - VĂN HÓA - NGHỆ THUẬT
    "ngôn ngữ anh": {
        "desc": "Trang bị tiếng Anh thành thạo (C1-C2) và kiến thức văn hóa Anh-Mỹ.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Kỹ năng Nghe - Nói - Đọc - Viết thành thạo.
        - Biên phiên dịch (Dịch viết và Dịch cabin).
        - Tiếng Anh thương mại và phương pháp giảng dạy.
        """,
        "career": """
        - Biên dịch viên, Phiên dịch viên.
        - Giáo viên tiếng Anh tại các trung tâm, trường học.
        - Thư ký, trợ lý cho công ty nước ngoài.
        - Hướng dẫn viên du lịch quốc tế.
        """
    },
    "ngôn ngữ trung quốc": {
        "desc": "Đào tạo tiếng Trung phục vụ giao thương kinh tế và giao lưu văn hóa.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Giao tiếp tiếng Trung lưu loát.
        - Biên phiên dịch Hoa - Việt.
        - Nghiệp vụ thương mại, xuất nhập khẩu với Trung Quốc/Đài Loan.
        """,
        "career": """
        - Phiên dịch viên tại các khu công nghiệp có vốn Trung Quốc/Đài Loan.
        - Nhân viên kinh doanh, mua hàng (Purchasing) tiếng Trung.
        - Giáo viên dạy tiếng Trung.
        """
    },
    "ngôn ngữ khmer": {
        "desc": "Ngành đặc thù cấp khu vực, đào tạo chuyên gia về ngôn ngữ, văn hóa Khmer Nam Bộ.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Thành thạo tiếng Khmer (nghe, nói, đọc, viết).
        - Kiến thức sâu rộng về văn hóa, tôn giáo, lịch sử Khmer.
        - Kỹ năng biên phiên dịch Việt - Khmer.
        """,
        "career": """
        - Cán bộ tại các cơ quan nhà nước vùng có đông đồng bào Khmer (Trà Vinh, Sóc Trăng...).
        - Biên tập viên, phóng viên đài phát thanh/truyền hình tiếng Khmer.
        - Phiên dịch viên cho các doanh nghiệp làm việc tại Campuchia.
        """
    },
    "văn hóa học": {
        "desc": "Nghiên cứu văn hóa Việt Nam và thế giới, ứng dụng trong truyền thông và du lịch.",
        "time": "3.5 - 4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Phân tích và quản lý di sản văn hóa.
        - Tổ chức sự kiện văn hóa, lễ hội.
        - Kỹ năng truyền thông văn hóa.
        """,
        "career": """
        - Cán bộ Sở Văn hóa, Trung tâm văn hóa.
        - Chuyên viên tổ chức sự kiện (Event Planner).
        - Nghiên cứu văn hóa, làm việc tại bảo tàng.
        """
    },
    "âm nhạc học": {
        "desc": "Đào tạo kiến thức chuyên sâu về lý luận âm nhạc, phê bình và dàn dựng.",
        "time": "4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Phân tích tác phẩm âm nhạc, ký xướng âm.
        - Dàn dựng chương trình nghệ thuật.
        - Kỹ năng sư phạm âm nhạc.
        """,
        "career": """
        - Giảng viên âm nhạc, giáo viên nhạc.
        - Biên tập viên âm nhạc tại đài truyền hình.
        - Nhà phê bình, nghiên cứu âm nhạc.
        """
    },
    "biểu diễn nhạc cụ truyền thống": {
        "desc": "Đào tạo nghệ sĩ chuyên nghiệp biểu diễn nhạc cụ dân tộc (Đàn Tranh, Bầu, Kìm...).",
        "time": "4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Kỹ thuật diễn tấu điêu luyện nhạc cụ chuyên ngành.
        - Biểu diễn hòa tấu và độc tấu.
        - Dàn dựng tiết mục dân nhạc.
        """,
        "career": """
        - Nghệ sĩ biểu diễn tại các đoàn nghệ thuật, nhà hát.
        - Giảng viên dạy nhạc cụ dân tộc.
        - Nhạc công chuyên nghiệp.
        """
    },
    # 7. KHỐI SƯ PHẠM & XÃ HỘI (Miễn học phí theo quy định)
    "giáo dục mầm non": {
        "desc": "Đào tạo giáo viên Mầm non yêu trẻ, có kỹ năng chăm sóc và giáo dục trẻ toàn diện.",
        "time": "3 - 4 năm (Cử nhân)",
        "fee": "✅ **MIỄN HỌC PHÍ** & Hỗ trợ sinh hoạt phí (NĐ 116)",
        "skills": """
        - Chăm sóc vệ sinh, dinh dưỡng cho trẻ.
        - Tổ chức hoạt động vui chơi, giáo dục âm nhạc, mỹ thuật cho trẻ.
        - Quản lý nhóm lớp mầm non.
        """,
        "career": """
        - Giáo viên tại các trường Mầm non công lập, tư thục, quốc tế.
        - Quản lý trường mầm non.
        - Chuyên viên giáo dục mầm non tại Phòng GD&ĐT.
        """
    },
    "giáo dục tiểu học": {
        "desc": "Đào tạo giáo viên dạy các môn văn hóa ở bậc Tiểu học.",
        "time": "4 năm (Cử nhân)",
        "fee": "✅ **MIỄN HỌC PHÍ** & Hỗ trợ sinh hoạt phí (NĐ 116)",
        "skills": """
        - Phương pháp dạy học các môn Toán, Tiếng Việt, Tự nhiên xã hội...
        - Kỹ năng chủ nhiệm lớp và tâm lý lứa tuổi học sinh tiểu học.
        - Ứng dụng CNTT trong dạy học.
        """,
        "career": """
        - Giáo viên dạy trường Tiểu học.
        - Cán bộ quản lý giáo dục tiểu học.
        """
    },
    "sư phạm ngữ văn": {
        "desc": "Đào tạo giáo viên dạy môn Ngữ văn cho trường THCS, THPT.",
        "time": "4 năm (Cử nhân)",
        "fee": "✅ **MIỄN HỌC PHÍ** & Hỗ trợ sinh hoạt phí (NĐ 116)",
        "skills": """
        - Phương pháp giảng dạy Văn học và Tiếng Việt.
        - Phân tích tác phẩm văn học.
        - Kỹ năng viết và biên tập văn bản.
        """,
        "career": """
        - Giáo viên Ngữ văn trường cấp 2, cấp 3.
        - Phóng viên, biên tập viên báo chí, truyền thông.
        - Nghiên cứu văn học.
        """
    },
    "sư phạm tiếng khmer": {
        "desc": "Đào tạo giáo viên dạy tiếng Khmer cho các trường phổ thông dân tộc nội trú.",
        "time": "4 năm (Cử nhân)",
        "fee": "✅ **MIỄN HỌC PHÍ** & Hỗ trợ sinh hoạt phí (NĐ 116)",
        "skills": """
        - Phương pháp dạy tiếng Khmer như ngôn ngữ thứ hai/tiếng mẹ đẻ.
        - Kiến thức ngữ văn Khmer.
        """,
        "career": """
        - Giáo viên dạy tiếng Khmer tại các trường vùng ĐBSCL.
        - Cán bộ nghiên cứu giáo dục dân tộc.
        """
    },
    "công tác xã hội": {
        "desc": "Đào tạo nhân viên xã hội chuyên nghiệp hỗ trợ giải quyết vấn đề xã hội.",
        "time": "4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Tham vấn tâm lý, hỗ trợ cộng đồng.
        - Quản lý ca (Case management).
        - Tổ chức phát triển cộng đồng và an sinh xã hội.
        """,
        "career": """
        - Nhân viên xã hội tại các bệnh viện, trường học, mái ấm.
        - Cán bộ Hội phụ nữ, Đoàn thanh niên, Lao động thương binh xã hội.
        - Làm việc tại các tổ chức phi chính phủ (NGOs).
        """
    },
    "chính trị học": {
        "desc": "Nghiên cứu các vấn đề lý luận và thực tiễn về chính trị, xây dựng Đảng.",
        "time": "4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Phân tích chính sách, tình hình chính trị.
        - Công tác tổ chức, xây dựng Đảng và chính quyền.
        - Tuyên truyền, vận động quần chúng.
        """,
        "career": """
        - Cán bộ làm công tác Đảng, Đoàn thể trong cơ quan nhà nước.
        - Giảng viên lý luận chính trị.
        - Làm việc tại các cơ quan báo chí, tuyên giáo.
        """
    },
    "quản lý nhà nước": {
        "desc": "Đào tạo cán bộ hành chính chuyên nghiệp cho khu vực công.",
        "time": "4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Quản lý hành chính công, nhân sự khu vực công.
        - Hoạch định và thực thi chính sách công.
        - Soạn thảo văn bản quản lý nhà nước.
        """,
        "career": """
        - Cán bộ, công chức tại UBND các cấp, các Sở, Ban, Ngành.
        - Làm việc tại các đơn vị sự nghiệp công lập.
        """
    },
    "quản lý thể dục thể thao": {
        "desc": "Đào tạo chuyên gia tổ chức, quản lý và kinh doanh trong lĩnh vực thể thao.",
        "time": "4 năm (Cử nhân)",
        "fee": "20.000.000 VNĐ/năm",
        "skills": """
        - Tổ chức sự kiện thể thao, giải đấu.
        - Quản lý câu lạc bộ, phòng Gym, hồ bơi.
        - Marketing thể thao.
        """,
        "career": """
        - Cán bộ Trung tâm Thể dục thể thao, Sở Văn hóa Thể thao.
        - Quản lý phòng tập Gym, CLB thể thao chuyên nghiệp.
        - Kinh doanh dụng cụ thể dục thể thao.
        """
    }
}

#DATABASE ĐIỂM CHUẨN ĐẦY ĐỦ (Dữ liệu từ TB 466/TB-HĐTS năm 2025)
#pt_100:điểm THPT | pt_200:điểm học bạ
DIEM_CHUAN_DB = {
    # === KHỐI SỨC KHỎE ===
    "y khoa": {"pt_100": 21.25, "pt_200": None}, # Không xét học bạ
    "răng hàm mặt": {"pt_100": 20.75, "pt_200": None}, # Không xét học bạ
    "dược học": {"pt_100": 19.0, "pt_200": None}, # Không xét học bạ
    "điều dưỡng": {"pt_100": 17.25, "pt_200": 21.48},
    "y học dự phòng": {"pt_100": 17.0, "pt_200": 20.48},
    "kỹ thuật hình ảnh y học": {"pt_100": 17.25, "pt_200": 23.48},
    "kỹ thuật phục hồi chức năng": {"pt_100": 17.25, "pt_200": 23.0},
    "kỹ thuật xét nghiệm y học": {"pt_100": 21.5, "pt_200": 25.5},
    "y tế công cộng": {"pt_100": 15.0, "pt_200": 18.48},
    "hóa dược": {"pt_100": 14.0, "pt_200": 18.51},

    # === KHỐI KỸ THUẬT & CÔNG NGHỆ ===
    "công nghệ thông tin": {"pt_100": 15.0, "pt_200": 19.51},
    "trí tuệ nhân tạo": {"pt_100": 15.0, "pt_200": 19.51},
    "công nghệ kỹ thuật ô tô": {"pt_100": 15.0, "pt_200": 18.83},
    "công nghệ kỹ thuật cơ khí": {"pt_100": 15.0, "pt_200": 18.83},
    "công nghệ kỹ thuật cơ điện tử": {"pt_100": 15.0, "pt_200": 18.83},
    "công nghệ kỹ thuật điện, điện tử": {"pt_100": 15.0, "pt_200": 18.0}, # Gộp tên
    "công nghệ kỹ thuật điều khiển và tự động hóa": {"pt_100": 15.0, "pt_200": 18.83},
    "công nghệ kỹ thuật công trình xây dựng": {"pt_100": 15.0, "pt_200": 18.35},
    "kỹ thuật xây dựng công trình giao thông": {"pt_100": 15.0, "pt_200": 18.83},
    "công nghệ kỹ thuật hóa học": {"pt_100": 15.0, "pt_200": 18.0},
    "kỹ thuật môi trường": {"pt_100": 14.0, "pt_200": 18.0},
    "quản lý tài nguyên và môi trường": {"pt_100": 14.0, "pt_200": 18.33},

    # === KHỐI NÔNG NGHIỆP - THỦY SẢN ===
    "nông nghiệp": {"pt_100": 14.0, "pt_200": 18.0},
    "thú y": {"pt_100": 14.0, "pt_200": 18.0},
    "nuôi trồng thủy sản": {"pt_100": 14.0, "pt_200": 18.0},
    "bảo vệ thực vật": {"pt_100": 14.0, "pt_200": 18.0},
    "công nghệ thực phẩm": {"pt_100": 14.0, "pt_200": 18.0},
    "công nghệ sinh học": {"pt_100": 14.0, "pt_200": 18.33},

    # === KHỐI KINH TẾ - LUẬT - XÃ HỘI ===
    "quản trị kinh doanh": {"pt_100": 15.0, "pt_200": 18.45},
    "tài chính - ngân hàng": {"pt_100": 15.0, "pt_200": 18.45},
    "kế toán": {"pt_100": 15.0, "pt_200": 18.45},
    "kinh tế": {"pt_100": 15.0, "pt_200": 18.45},
    "luật": {"pt_100": 16.77, "pt_200": 20.22},
    "logistics và quản lý chuỗi cung ứng": {"pt_100": 19.25, "pt_200": 24.18},
    "thương mại điện tử": {"pt_100": 15.0, "pt_200": 18.13},
    "quản trị văn phòng": {"pt_100": 15.0, "pt_200": 18.0},
    "quản lý nhà nước": {"pt_100": 16.0, "pt_200": 18.0},
    "chính trị học": {"pt_100": 16.52, "pt_200": 18.7},
    "công tác xã hội": {"pt_100": 16.52, "pt_200": 19.29},
    "quản lý thể dục thể thao": {"pt_100": 22.0, "pt_200": 25.15},

    # === KHỐI DU LỊCH - VĂN HÓA ===
    "quản trị dịch vụ du lịch và lữ hành": {"pt_100": 15.0, "pt_200": 18.0},
    "văn hóa học": {"pt_100": 15.0, "pt_200": 18.0},

    # === KHỐI NGÔN NGỮ & NGHỆ THUẬT ===
    "ngôn ngữ anh": {"pt_100": 15.0, "pt_200": 18.0},
    "ngôn ngữ trung quốc": {"pt_100": 22.5, "pt_200": 25.03},
    "ngôn ngữ khmer": {"pt_100": 15.0, "pt_200": 18.0},
    "âm nhạc học": {"pt_100": 17.62, "pt_200": 18.0},
    "biểu diễn nhạc cụ truyền thống": {"pt_100": 17.62, "pt_200": 18.0},
}



# 2. HÀM TÌM KIẾM CHUNG (Helper Function)

def find_major_data(major_raw):
    if not major_raw: return None, None
    major_clean = major_raw.lower().strip()
    
    # Tìm chính xác
    if major_clean in MAJOR_DB:
        return major_clean, MAJOR_DB[major_clean]
    
    # Tìm gần đúng
    for key, data in MAJOR_DB.items():
        if key in major_clean or major_clean in key:
            return key, data
    return major_raw, None

# 3. CÁC ACTION CLASS

# ACTION 1: TRẢ LỜI THÔNG TIN CHUNG
class ActionProvideMajorInfo(Action):
    def name(self) -> Text:
        return "action_provide_major_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # 1. Bộ lọc chuyển hướng
        if "học bổng" in user_message or "ưu đãi" in user_message:
            return [FollowupAction("utter_ask_scholarship")]
        if "xét tuyển" in user_message or "phương thức" in user_message:
            return [FollowupAction("utter_tra_loi_xet_tuyen")]

        # 2. Xử lý Ngành học
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        if not major_entity:
            major_entity = tracker.get_slot("major")

        if not major_entity:
            dispatcher.utter_message(text="⚠️ Mình chưa rõ bạn muốn hỏi về ngành nào. Bạn vui lòng nhập đầy đủ tên ngành nhé (Ví dụ: Ngành Công nghệ thông tin).")
            return []

        major_name, data = find_major_data(major_entity)

        if data:
            msg = f"📚 **Thông tin ngành {major_name.upper()}:**\n{data['desc']}\n\nBạn muốn xem thêm thông tin gì?"
            
            #NÚT BẤM (Có nút Việc làm)
            buttons = [
                {"title": "💼 Việc làm & Kỹ năng", "payload": f'/ask_program_career'},
                {"title": "⏳ Thời gian đào tạo", "payload": f'/ask_training_duration'},
                {"title": "💰 Xem Học phí", "payload": f'/ask_tuition'},
                {"title": "📊 Điểm chuẩn", "payload": f'/tra_cuu_diem_chuan'}
            ]
            dispatcher.utter_message(text=msg, buttons=buttons)
            return [SlotSet("major", major_name)]
        else:
            dispatcher.utter_message(text=f"Xin lỗi, mình chưa tìm thấy thông tin ngành '{major_name}'.")
            return []

# ACTION 2: TRẢ LỜI CHI TIẾT CHƯƠNG TRÌNH & VIỆC LÀM
class ActionProvideProgramDetails(Action):
    def name(self) -> Text:
        return "action_provide_program_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # 1. Lấy từ Entity
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        
        # 2. Lấy từ Slot MỚI (Form)
        if not major_entity:
            major_entity = tracker.get_slot("program_major")

        # 3. Lấy từ Slot CŨ
        if not major_entity:
            major_entity = tracker.get_slot("major")

        if not major_entity:
            dispatcher.utter_message(text="Bạn muốn tìm hiểu chương trình đào tạo của ngành nào?")
            return []

        major_name, data = find_major_data(major_entity)

        if data:
            skills = data.get("skills", "Đang cập nhật...")
            career = data.get("career", "Đang cập nhật...")
            
            msg = f"🎓 **CHƯƠNG TRÌNH ĐÀO TẠO & VIỆC LÀM CHI TIẾT:**\n"
            msg += f"🔥 Ngành: **{major_name.upper()}**\n"
            msg += f"-----------------------------------\n"
            msg += f"🛠️ **KỸ NĂNG NGHỀ NGHIỆP:**\n{skills}\n"
            msg += f"-----------------------------------\n"
            msg += f"💼 **CƠ HỘI VIỆC LÀM:**\n{career}"
            
            dispatcher.utter_message(text=msg)
            
            # Reset slot program_major
            return [SlotSet("major", major_name), SlotSet("program_major", None)]
        else:
            dispatcher.utter_message(text=f"Xin lỗi, mình chưa tìm thấy thông tin chi tiết cho ngành '{major_name}'.")
            return [SlotSet("program_major", None)]

# ACTION 3: TRẢ LỜI THỜI GIAN
class ActionProvideDuration(Action):
    def name(self) -> Text:
        return "action_provide_duration"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        if not major_entity: major_entity = tracker.get_slot("major")
        
        if not major_entity:
             dispatcher.utter_message(text="Bạn muốn hỏi thời gian đào tạo của ngành nào?")
             return []

        major_name, data = find_major_data(major_entity)
        if data:
            dispatcher.utter_message(text=f"⏳ Thời gian đào tạo ngành **{major_name.upper()}** là: **{data['time']}**.")
            
            return [SlotSet("major", major_name)] 
        else:
            dispatcher.utter_message(text="Xin lỗi, mình chưa tìm thấy thông tin ngành này.")
        return []

# ACTION 4: TRẢ LỜI HỌC PHÍ
class ActionProvideTuition(Action):
    def name(self) -> Text:
        return "action_provide_tuition"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        if not major_entity: major_entity = tracker.get_slot("major")

        if not major_entity:
             dispatcher.utter_message(text="Bạn muốn hỏi học phí của ngành nào?")
             return []

        major_name, data = find_major_data(major_entity)
        if data:
            dispatcher.utter_message(text=f"💰 Học phí tham khảo ngành **{major_name.upper()}** là: **{data['fee']}**.")
            
            return [SlotSet("major", major_name)]
        else:
            dispatcher.utter_message(text="Xin lỗi, mình chưa tìm thấy thông tin ngành này.")
        return []

# ACTION 5: TÍNH ĐIỂM XÉT TUYỂN
class ActionTinhKetQuaXetTuyen(Action):
    def name(self) -> Text:
        return "action_tinh_ket_qua_xet_tuyen"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nganh_raw = tracker.get_slot("major")
        d1_val = tracker.get_slot("diem_mon_1")
        d2_val = tracker.get_slot("diem_mon_2")
        d3_val = tracker.get_slot("diem_mon_3")

        if d1_val is None or d2_val is None or d3_val is None:
            dispatcher.utter_message(text="⚠️ Hệ thống chưa nhận đủ điểm. Vui lòng nhập lại từ đầu.")
            return [SlotSet("diem_mon_1", None), SlotSet("diem_mon_2", None), SlotSet("diem_mon_3", None), SlotSet("diem_uu_tien", None)]

        try:
            d1 = float(d1_val)
            d2 = float(d2_val)
            d3 = float(d3_val)
            uu_tien_raw = tracker.get_slot("diem_uu_tien")
            d_uu_tien = float(uu_tien_raw) if uu_tien_raw else 0.0     
        except (ValueError, TypeError):
            dispatcher.utter_message(text="⚠️ Điểm nhập vào không phải là số.")
            return [SlotSet("diem_mon_1", None), SlotSet("diem_mon_2", None), SlotSet("diem_mon_3", None), SlotSet("diem_uu_tien", None)]

        tong_diem_xet_tuyen = d1 + d2 + d3 + d_uu_tien
        
        # Tìm ngành
        nganh_key = nganh_raw.lower().strip() if nganh_raw else ""
        found_key = None
        for key in DIEM_CHUAN_DB:
            if key in nganh_key or nganh_key in key:
                found_key = key
                break
        
        msg = f"📊 **KẾT QUẢ XÉT TUYỂN DỰ KIẾN:**\nNgành: **{nganh_raw}**\nTổng điểm: **{tong_diem_xet_tuyen:.2f}**\n"
        
        if found_key:
            data = DIEM_CHUAN_DB[found_key]
            # Logic đơn giản: Nếu > 24 coi như xét học bạ, ngược lại xét điểm thi (Demo)
            is_xet_hoc_ba = tong_diem_xet_tuyen > 24
            diem_chuan = data["pt_200"] if is_xet_hoc_ba else data["pt_100"]
            
            if diem_chuan:
                msg += f"Điểm chuẩn tham khảo: **{diem_chuan}**\n"
                if tong_diem_xet_tuyen >= diem_chuan:
                    msg += "🎉 **KẾT QUẢ: ĐẬU**"
                else:
                    msg += "😢 **KẾT QUẢ: TRƯỢT**"
            else:
                msg += "⚠️ Ngành này chưa có dữ liệu điểm chuẩn cho phương thức này."
        else:
            msg += "⚠️ Chưa tìm thấy dữ liệu điểm chuẩn ngành này."

        dispatcher.utter_message(text=msg)
        return [
            SlotSet("diem_mon_1", None), 
            SlotSet("diem_mon_2", None), 
            SlotSet("diem_mon_3", None),
            SlotSet("diem_uu_tien", None)
        ]