# Nội dung báo cáo và thuyết trình của từng thành viên

Tài liệu này ghi rõ **mỗi người viết gì trong báo cáo và trình bày gì khi bảo vệ**: dàn ý từng mục, các ý chính cần có, bảng và hình nên đưa vào, độ dài, slide và các câu hỏi hay gặp kèm gợi ý trả lời.

- Ai làm phần nào: [04-phan-cong.md](04-phan-cong.md)
- Cách làm phần code: [06-huong-dan-thanh-vien.md](06-huong-dan-thanh-vien.md)
- Mã mục (ví dụ `1.7`) tham chiếu tới [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md)

> Các ý dưới đây là **khung và gợi ý**, không phải bài viết hoàn chỉnh. Mỗi người tự viết lại bằng lời của mình, thêm số liệu thật từ ứng dụng của nhóm và ghi nguồn tham khảo. Số liệu về giá, giấy phép của các nhà cung cấp bản đồ thay đổi theo thời gian, cần kiểm tra lại trên trang chính thức lúc viết.

**Mục lục**

- [0. Khung báo cáo chung](#0-khung-báo-cáo-chung)
- [1. TV1 – Nhóm trưởng](#1-tv1--nhóm-trưởng)
- [2. TV2 – Tổng quan bản đồ số](#2-tv2--tổng-quan-bản-đồ-số)
- [3. TV3 – Mô hình hóa và thuật toán](#3-tv3--mô-hình-hóa-và-thuật-toán)
- [4. TV4 – Hệ thống tìm đường thực tế](#4-tv4--hệ-thống-tìm-đường-thực-tế)
- [5. TV5 – Đánh giá thực nghiệm](#5-tv5--đánh-giá-thực-nghiệm)
- [6. Buổi thuyết trình](#6-buổi-thuyết-trình)
- [7. Checklist nộp phần báo cáo](#7-checklist-nộp-phần-báo-cáo)

---

## 0. Khung báo cáo chung

### 0.1 Bố cục báo cáo cuối

| Chương | Nội dung | Mục trong file 03 | Người viết |
|---|---|---|---|
| Mở đầu | Lý do chọn đề tài, mục tiêu, phạm vi, bố cục báo cáo | | TV1 |
| 1. Tổng quan bản đồ số | Khái niệm, vai trò trong ITS, mô hình dữ liệu, nguồn dữ liệu, hệ tọa độ | `1.1`–`1.4` | TV2 |
| 2. Mô hình hóa và thuật toán tìm đường | Đồ thị giao thông, BFS/DFS, Dijkstra, A\*, Bidirectional, CH/ALT, bảng so sánh | `1.5`–`1.10`, `1.12` | TV3 |
| 3. Các hệ thống tìm đường thực tế | OSRM, GraphHopper, Valhalla, Google | `1.11` | TV4 |
| 4. Xây dựng ứng dụng demo | Kiến trúc, API, dữ liệu, thuật toán, giao diện | | Mỗi người viết phần code của mình, TV1 ghép |
| 5. Đánh giá thực nghiệm | Phương pháp, kết quả, đối chiếu, nhận xét | `1.13`, mục `4` | TV5 |
| 6. Kết luận và hướng phát triển | | `1.14` | TV1 |
| Tài liệu tham khảo | Gộp nguồn của mọi người | | TV1 |

Chương 4 chia nhỏ như sau:

| Mục | Nội dung | Người viết |
|---|---|---|
| 4.1 | Kiến trúc tổng thể, công nghệ, CI | TV1 |
| 4.2 | Định dạng API | TV1 |
| 4.3 | Tải và quản lý dữ liệu bản đồ | TV2 |
| 4.4 | Cài đặt thuật toán và kiểm thử | TV3 |
| 4.5 | Giao diện bản đồ | TV4 |
| 4.6 | Bảng điều khiển, số liệu, so sánh, benchmark | TV5 |

### 0.2 Quy ước viết

- Viết bằng Markdown trong `docs/bao-cao/`, mỗi phần một file đặt tên theo mã mục, ví dụ `1.7-dijkstra.md`. Hình để trong `docs/bao-cao/hinh/`.
- Thuật ngữ tiếng Anh ghi trong ngoặc ở lần đầu xuất hiện, ví dụ "heuristic chấp nhận được (admissible)".
- Đánh số hình và bảng theo chương: "Hình 2.3", "Bảng 1.2". Mỗi hình, bảng đều có chú thích và được nhắc tới trong bài.
- Đơn vị: mét (m), kilômét (km), mili giây (ms). Số thập phân dùng dấu phẩy trong văn bản ("2,5 km"), giữ dấu chấm trong code.
- Nguồn tham khảo đánh số `[1]`, `[2]`... và liệt kê cuối file. Không chép nguyên văn, viết lại bằng lời của mình.
- Số liệu của dự án (số node, số cạnh, thời gian chạy) lấy từ ứng dụng thật của nhóm, ghi rõ lấy ở đâu.

### 0.3 Độ dài gợi ý

| Người | Phần | Số trang (A4) |
|---|---|---|
| TV1 | Mở đầu, 4.1, 4.2, kết luận | 4–5 |
| TV2 | Chương 1, mục 4.3 | 7–9 |
| TV3 | Chương 2, mục 4.4 | 9–12 |
| TV4 | Chương 3, mục 4.5 | 5–7 |
| TV5 | Chương 5, mục 4.6 | 6–8 |

---

## 1. TV1 – Nhóm trưởng

**Viết:** Mở đầu, mục 4.1, 4.2, chương 6 (`1.14`, đã có bản nháp ở [bao-cao/1.14-ket-luan.md](bao-cao/1.14-ket-luan.md)). **Làm thêm:** ghép báo cáo, thống nhất định dạng, gộp tài liệu tham khảo, làm slide chung, điều phối demo.

### Mở đầu

1. **Lý do chọn đề tài:** nhu cầu di chuyển trong đô thị, kẹt xe ở TP.HCM; các ứng dụng dẫn đường, gọi xe, giao hàng đều cần bản đồ số và thuật toán tìm đường; muốn hiểu bên trong các hệ thống này hoạt động thế nào.
2. **Mục tiêu:** lấy từ mục 1 của [02-de-xuat-du-an.md](02-de-xuat-du-an.md): khảo sát bản đồ số, so sánh thuật toán, xây ứng dụng demo, đánh giá thực nghiệm.
3. **Phạm vi:** mạng đường ô tô của Quận 1 từ OpenStreetMap; trọng số là độ dài đoạn đường; 2 thuật toán chính Dijkstra và A\* (cộng phần mở rộng nếu có).
4. **Phương pháp:** khảo sát tài liệu, cài đặt và đo đạc thực nghiệm.
5. **Bố cục báo cáo:** mỗi chương một câu.

### 4.1 Kiến trúc tổng thể

- Sơ đồ 2 khối FE (React, Leaflet, port 5173) và BE (FastAPI, OSMnx, port 8000) giao tiếp qua HTTP/JSON. Có thể vẽ lại sơ đồ "Luồng hoạt động" trong [01-cau-truc-du-an.md](01-cau-truc-du-an.md).
- Bảng công nghệ và lý do chọn (lấy từ mục 3 của file 02).
- **Luồng xử lý một yêu cầu tìm đường** (nên có hình): người dùng click 2 điểm → FE gọi `GET /api/route` → BE kiểm tra tọa độ nằm trong khung bao → bắt mỗi điểm về node gần nhất → chạy thuật toán → đổi id node sang tọa độ → lấy mẫu tối đa 5000 node đã duyệt → trả JSON → FE vẽ đường đi và số liệu.
- Đồ thị nạp **một lần** khi khởi động server và dùng chung cho mọi yêu cầu.
- Quy trình làm việc nhóm: GitHub, nhánh theo chức năng, Pull Request, CI tự chạy `ruff`, `pytest`, `npm run build`.

### 4.2 Định dạng API

Tóm tắt [05-dinh-dang-api.md](05-dinh-dang-api.md): bảng endpoint, ví dụ JSON của `/api/route`, bảng mã lỗi 400/404/422/503. Giải thích vài quyết định thiết kế:

- Tọa độ luôn là `[lat, lng]` cho khớp với Leaflet.
- Chốt định dạng API ngay từ đầu (file `schemas.py`) để FE làm với dữ liệu giả trong khi BE chưa xong.
- Chỉ gửi tối đa 5000 node đã duyệt để trình duyệt không bị đơ, `visited_count` vẫn là tổng thật.

### Chương 6. Kết luận

Hoàn thiện bản nháp `1.14`: điền các chỗ `[...]` bằng số liệu TV5 gửi; mục "Hạn chế" bổ sung theo kết quả thực nghiệm và những gì nhóm chưa làm được.

### Slide của TV1

1. Bìa, thành viên.
2. Lý do, mục tiêu, phạm vi.
3. Kiến trúc hệ thống và luồng một yêu cầu tìm đường.
4. Demo trực tiếp (cùng TV4).
5. Kết luận và hướng phát triển.

### Câu hỏi hay gặp

| Câu hỏi | Gợi ý trả lời |
|---|---|
| Vì sao tách FE và BE? | Mỗi phần làm, chạy, kiểm thử độc lập; FE làm song song bằng dữ liệu giả; sau này đổi giao diện hoặc thuật toán không ảnh hưởng phần kia. |
| Vì sao chọn FastAPI? | Nhẹ, viết bằng Python (cùng ngôn ngữ với OSMnx, NetworkX), tự kiểm tra tham số bằng Pydantic, tự sinh trang tài liệu `/docs`. |
| Người dùng click vào chỗ không có đường thì sao? | BE bắt điểm click về node gần nhất của đồ thị; click ngoài khung bao quận thì trả lỗi 400. |
| Khi nào trả 400, khi nào 404? | 400: dữ liệu vào sai (tọa độ ngoài vùng bản đồ). 404: dữ liệu đúng nhưng không tìm được đường giữa 2 điểm. |
| Bản đồ cả thành phố thì có chạy được không? | Chạy được nhưng chậm hơn nhiều vì số node tăng hàng chục lần; muốn nhanh phải dùng kỹ thuật tiền xử lý như Contraction Hierarchies (chương 2, 3). |
| Nhóm phối hợp thế nào? | Chốt API trước, mỗi người một nhánh, Pull Request có CI và nhóm trưởng review, họp tuần. |

---

## 2. TV2 – Tổng quan bản đồ số

**Viết:** chương 1 (`1.1`–`1.4`) và mục 4.3.

### 1.1 Khái niệm bản đồ số và vai trò trong ITS

**1.1.1 Bản đồ số là gì**
- Bản đồ được lưu và xử lý trên máy tính dưới dạng dữ liệu không gian: **hình học** (điểm, đường, vùng), **thuộc tính** (tên đường, loại đường, tốc độ giới hạn...) và **quan hệ** giữa các đối tượng (đoạn nào nối với đoạn nào).
- So với bản đồ giấy: truy vấn được (tìm địa chỉ, tìm đường), phóng to thu nhỏ nhiều tỉ lệ, cập nhật nhanh, chồng nhiều lớp thông tin, cá nhân hóa theo người dùng.

**1.1.2 Các lớp thông tin của bản đồ số**
- Lớp nền (ảnh tile để hiển thị), lớp mạng đường (dùng cho tìm đường), lớp điểm quan tâm (POI: trường học, bệnh viện, cây xăng), lớp dữ liệu động (tình trạng giao thông, sự cố).
- Hình gợi ý: sơ đồ các lớp chồng lên nhau.

**1.1.3 Hệ thống giao thông thông minh (ITS)**
- Ứng dụng công nghệ thông tin, viễn thông, cảm biến vào quản lý và vận hành giao thông.
- Các nhóm ứng dụng: thông tin cho người tham gia giao thông (ATIS), quản lý giao thông (ATMS), giao thông công cộng (APTS), vận tải hàng hóa và đội xe (CVO), xe kết nối và xe tự hành.

**1.1.4 Vai trò của bản đồ số trong ITS**
- Định vị và khớp vị trí GPS vào đúng con đường (map matching).
- Tìm đường, dẫn đường từng bước, ước tính thời gian đến (ETA).
- Điều phối đội xe: gọi xe, giao hàng, xe cấp cứu.
- Quản lý, quy hoạch giao thông: mô phỏng, phân tích điểm kẹt xe.
- Bản đồ độ chính xác cao (HD map) cho xe tự hành.
- Ví dụ quen thuộc ở Việt Nam: ứng dụng bản đồ, gọi xe, giao hàng, thiết bị giám sát hành trình đều dựa trên bản đồ số.

### 1.2 Mô hình dữ liệu bản đồ

**1.2.1 Dữ liệu vector và raster**: raster là lưới điểm ảnh (ảnh vệ tinh, ảnh tile), vector là tọa độ điểm, đường, vùng. Tìm đường cần dữ liệu vector.

**1.2.2 Mô hình dữ liệu của OpenStreetMap**

| Thành phần | Ý nghĩa | Ví dụ |
|---|---|---|
| Node | Một điểm có id, vĩ độ, kinh độ | Giao lộ, một điểm trên đường cong |
| Way | Dãy node có thứ tự | Một đoạn đường, ranh giới tòa nhà |
| Relation | Nhóm các node, way có vai trò | Lệnh cấm rẽ, tuyến xe buýt |
| Tag | Cặp `khóa=giá trị` gắn vào các thành phần trên | `highway=primary`, `oneway=yes` |

**1.2.3 Thuộc tính đường quan trọng cho tìm đường**: `highway` (loại đường: motorway, trunk, primary, secondary, tertiary, residential, service...), `oneway`, `maxspeed`, `lanes`, `junction=roundabout`, `access`, quan hệ cấm rẽ (`type=restriction`).

**1.2.4 Từ dữ liệu OSM tới đồ thị** (cầu nối sang chương 2)
- OSMnx tải các way có thể đi bằng ô tô (`network_type="drive"`) rồi đơn giản hóa: chỉ giữ node là giao lộ hoặc điểm cuối đường; các điểm trung gian chỉ còn là hình dạng (geometry) của cạnh.
- Mỗi cạnh có `length` (mét). Đường hai chiều thành 2 cạnh ngược chiều, đường một chiều chỉ có 1 cạnh.
- Kết quả là đồ thị có hướng, cho phép nhiều cạnh song song giữa 2 node (MultiDiGraph).
- Đưa số node, số cạnh thật của Quận 1 lấy từ `/api/graph/info`.
- Hình gợi ý: một giao lộ ngoài thực tế và cách nó thành node, cạnh; bảng thuộc tính của 1 cạnh mẫu.

### 1.3 So sánh các nguồn dữ liệu bản đồ

Khung bảng (điền và kiểm tra lại thông tin trên trang chính thức):

| Tiêu chí | OpenStreetMap | Google Maps | HERE | Mapbox | VietMap | Vietbando |
|---|---|---|---|---|---|---|
| Ai xây dựng | Cộng đồng toàn cầu | Google | HERE Technologies | Mapbox (dựa trên OSM và nguồn khác) | Doanh nghiệp Việt Nam | Doanh nghiệp Việt Nam |
| Giấy phép | Mở (ODbL), phải ghi công | Thương mại | Thương mại | Thương mại | Thương mại | Thương mại |
| Chi phí | Miễn phí | Trả theo lượt gọi, có hạn mức miễn phí | Có gói miễn phí giới hạn | Có gói miễn phí giới hạn | Theo gói | Theo gói |
| Tải toàn bộ mạng đường về máy | Được | Không | Không | Không | | |
| Giao thông thời gian thực | Không | Có | Có | Có | | |
| Độ chi tiết ở Việt Nam | Tốt ở đô thị lớn, nông thôn có thể thiếu | Rất tốt | | | Tốt, tên đường và địa chỉ tiếng Việt | |
| API tìm đường | Không có sẵn, dùng OSRM/GraphHopper/Valhalla | Có | Có | Có | Có | |

Kết luận: đề tài chọn OSM vì miễn phí, **tải được toàn bộ mạng đường** để tự chạy thuật toán và đếm node đã duyệt (các dịch vụ thương mại chỉ trả kết quả qua API, không cho lấy đồ thị).

### 1.4 Hệ tọa độ, tile map và vector tile

- **WGS84 (EPSG:4326):** hệ tọa độ của GPS, dùng vĩ độ (lat, −90° đến 90°) và kinh độ (lng, −180° đến 180°). 1 độ vĩ dài khoảng 111 km; 1 độ kinh dài khoảng 111 km × cos(vĩ độ), ở TP.HCM (vĩ độ khoảng 10,8°) là khoảng 109 km.
- **Web Mercator (EPSG:3857):** phép chiếu hình trụ dùng cho hầu hết bản đồ web. Giữ đúng góc (hình dạng nhỏ không méo) nhưng phóng to diện tích khi đi về phía hai cực; chỉ vẽ tới vĩ độ khoảng ±85,05°.
- **Tile raster:** bản đồ cắt thành ô ảnh 256×256 px, đánh địa chỉ `z/x/y`; ở mức zoom `z` có 2^z × 2^z ô. Ví dụ FE dùng `https://tile.openstreetmap.org/{z}/{x}/{y}.png`.
- **Vector tile:** ô chứa dữ liệu hình học thay vì ảnh (phổ biến là định dạng Mapbox Vector Tile), trình duyệt tự vẽ; đổi màu, xoay, nghiêng bản đồ được, dữ liệu nhẹ hơn.
- **Liên hệ với ứng dụng:** BE lưu tọa độ WGS84; Leaflet nhận lat/lng rồi tự chiếu sang Web Mercator để vẽ. Khoảng cách giữa 2 tọa độ tính bằng **công thức Haversine** vì lat/lng là góc trên mặt cầu, không dùng định lý Pytago trực tiếp được:

  a = sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2), d = 2R · arcsin(√a), với φ là vĩ độ, λ là kinh độ (radian), R ≈ 6 371 km.

### 4.3 Tải và quản lý dữ liệu bản đồ trong ứng dụng

- Tải bằng `osmnx.graph_from_place("District 1, Ho Chi Minh City, Vietnam", network_type="drive")`.
- Lưu cache ra file `.graphml`: lần đầu mất bao lâu, lần sau mất bao lâu (đo thật).
- Giữ thành phần liên thông mạnh lớn nhất: số node trước và sau, lý do (bỏ các node chỉ đi vào hoặc chỉ đi ra ở ranh giới quận để luôn có đường giữa 2 điểm).
- `GET /api/graph/info`: các trường trả về.
- `nearest_node`: cách làm, độ phức tạp O(V), thời gian chạy thực tế.
- (Nếu làm) trọng số theo thời gian, giả lập kẹt xe.

### Slide của TV2

1. Bản đồ số là gì, vai trò trong ITS.
2. Dữ liệu OSM và cách chuyển thành đồ thị (hình giao lộ thành node, cạnh).
3. Bảng so sánh nguồn dữ liệu, lý do chọn OSM.
4. Hệ tọa độ, tile và vì sao dùng Haversine.

### Câu hỏi hay gặp

| Câu hỏi | Gợi ý trả lời |
|---|---|
| Vì sao không dùng dữ liệu Google Maps? | Google chỉ trả kết quả tìm đường qua API, không cho tải mạng đường, nên không tự chạy và so sánh thuật toán được; lại tốn phí. |
| ODbL nghĩa là gì? | Giấy phép dữ liệu mở: được dùng, sửa, phân phối miễn phí, phải ghi công OpenStreetMap và chia sẻ lại phần dữ liệu sửa đổi theo cùng giấy phép. |
| Vì sao chỉ giữ thành phần liên thông mạnh lớn nhất? | Đường bị cắt ở ranh giới quận tạo ra node không đi ra (hoặc không đi vào) được; giữ lại thì nhiều cặp điểm không có đường. |
| Vì sao không tính khoảng cách bằng Pytago trên lat/lng? | Lat/lng là góc trên mặt cầu, 1 độ kinh ngắn dần khi ra xa xích đạo; Haversine tính đúng khoảng cách trên mặt cầu. |
| Vì sao bản đồ web làm Greenland to bằng châu Phi? | Web Mercator giữ góc nhưng phóng to diện tích về phía cực. |
| `nearest_node` chạy thế nào, có chậm không? | Duyệt mọi node, chọn node có khoảng cách Haversine nhỏ nhất: O(V), với một quận chỉ vài mili giây. Bản đồ lớn thì dùng cây không gian (KD-tree, Ball tree). |
| MultiDiGraph khác DiGraph ở đâu? | Cho phép nhiều cạnh song song giữa 2 node (2 con đường khác nhau cùng nối 2 giao lộ); thuật toán lấy cạnh ngắn nhất. |
| `network_type="drive"` bỏ những đường nào? | Đường đi bộ, đường xe đạp riêng, đường nội bộ không cho ô tô, đường cấm theo thẻ `access`. |

---

## 3. TV3 – Mô hình hóa và thuật toán

**Viết:** chương 2 (`1.5`–`1.10`, `1.12`) và mục 4.4. Đây là chương trọng tâm của đề tài, nên có ví dụ chạy tay và hình minh họa.

### 1.5 Mô hình hóa mạng giao thông thành đồ thị

- Định nghĩa đồ thị có hướng có trọng số G = (V, E, w), với w: E → ℝ≥0.
- Ánh xạ: node ↔ giao lộ, cạnh ↔ đoạn đường theo một chiều đi, trọng số ↔ độ dài (hoặc thời gian = độ dài / tốc độ, hoặc chi phí có tính kẹt xe).
- Đường một chiều, đường hai chiều, cạnh song song.
- Mạng đường là **đồ thị thưa**: số cạnh chỉ gấp vài lần số node (tính tỉ lệ cạnh/node thật của Quận 1). Vì vậy lưu bằng danh sách kề thay vì ma trận kề (ma trận cần V² ô, gần như toàn số 0).
- Bài toán đường đi ngắn nhất từ một nguồn tới một đích.

### 1.6 BFS và DFS (mốc so sánh)

- BFS duyệt theo từng lớp, O(V + E), cho đường **ít cạnh nhất**, chỉ là đường ngắn nhất khi mọi cạnh dài bằng nhau.
- DFS đi sâu trước, không đảm bảo đường ngắn nhất.
- Hình gợi ý: ví dụ phản chứng, đường 2 cạnh dài 1000 m và đường 3 cạnh tổng 300 m; BFS chọn sai.

### 1.7 Thuật toán Dijkstra

- Nguồn gốc: Edsger W. Dijkstra nghĩ ra năm 1956, công bố năm 1959.
- Ý tưởng tham lam: luôn chốt node chưa chốt có khoảng cách tạm nhỏ nhất, rồi nới lỏng (relax) các cạnh đi ra từ nó.
- Mã giả (viết dạng có hàng đợi ưu tiên).
- **Tính đúng:** khi một node được lấy ra khỏi hàng đợi thì khoảng cách tới nó đã tối ưu, vì mọi đường khác phải đi qua node có khoảng cách lớn hơn hoặc bằng, cộng thêm cạnh **không âm**. Từ đó giải thích vì sao trọng số âm làm Dijkstra sai.
- **Độ phức tạp:** dùng mảng O(V²); heap nhị phân O((V + E) log V); heap Fibonacci O(E + V log V). Với đồ thị thưa, heap nhị phân là đủ.
- Dừng sớm khi lấy được đích ra khỏi hàng đợi.
- **Ví dụ chạy tay** trên đồ thị 5–6 node: bảng từng bước (node được chốt, khoảng cách tạm của các node, nội dung hàng đợi).
- Hình gợi ý: vùng node đã duyệt của Dijkstra trên bản đồ (chụp từ ứng dụng), lan ra gần như hình tròn quanh điểm đi.

### 1.8 Thuật toán A\*

- Nguồn gốc: Hart, Nilsson, Raphael (1968).
- f(n) = g(n) + h(n): g là độ dài đã đi từ điểm đầu, h là ước lượng phần còn lại tới đích.
- **Heuristic chấp nhận được (admissible):** h(n) ≤ h\*(n), không bao giờ ước lượng quá độ dài thật còn lại.
- **Heuristic nhất quán (consistent):** h(u) ≤ w(u, v) + h(v) với mọi cạnh, và h(đích) = 0. Nhất quán thì chấp nhận được; với heuristic nhất quán, mỗi node chỉ cần duyệt một lần.
- **Heuristic Haversine:** đường đi thật luôn dài hơn hoặc bằng đường chim bay nên Haversine thỏa cả 2 điều kiện. Nhóm lấy bán kính Trái Đất 6 371 000 m, nhỏ hơn giá trị OSMnx dùng để tính `length` (6 371 009 m), để chắc chắn không ước lượng quá.
- Trường hợp đặc biệt: h = 0 thì A\* chính là Dijkstra; h ước lượng quá thì nhanh hơn nhưng có thể ra đường không ngắn nhất.
- Có thể nêu cách nhìn khác: A\* với h nhất quán tương đương Dijkstra trên trọng số rút gọn w'(u, v) = w(u, v) − h(u) + h(v) ≥ 0.
- Độ phức tạp trường hợp xấu nhất như Dijkstra; hiệu quả thực tế phụ thuộc h tốt đến đâu.
- Muốn tìm đường **nhanh nhất** (trọng số thời gian) thì heuristic phải là Haversine chia cho tốc độ lớn nhất trên bản đồ.
- Hình gợi ý: vùng duyệt của A\* hẹp, kéo dài về phía đích, đặt cạnh hình của Dijkstra.

### 1.9 Bidirectional Dijkstra

- Chạy đồng thời 2 Dijkstra: xuôi từ điểm đầu, ngược từ điểm cuối (trên các cạnh đảo chiều).
- **Điều kiện dừng:** đỉnh hàng đợi xuôi + đỉnh hàng đợi ngược ≥ độ dài đường tốt nhất đã thấy. Dừng ngay khi 2 phía vừa chạm nhau là sai.
- Vì sao duyệt ít hơn: một hình tròn bán kính r có diện tích πr², hai hình tròn bán kính r/2 có tổng diện tích πr²/2, tức khoảng một nửa.
- Cần đồ thị ngược; kết hợp với A\* (Bidirectional A\*) phức tạp hơn vì điều kiện dừng khác.

### 1.10 Contraction Hierarchies và ALT (giới thiệu)

- **Contraction Hierarchies (CH)**, Geisberger và cộng sự (2008): bước tiền xử lý xếp hạng node theo mức "quan trọng", lần lượt co (contract) từng node, thêm cạnh tắt (shortcut) để giữ nguyên khoảng cách giữa các node còn lại. Khi truy vấn chạy Dijkstra 2 chiều, mỗi phía chỉ đi lên node có hạng cao hơn, nên chỉ duyệt vài trăm node kể cả trên bản đồ cả châu lục. Nhược điểm: tiền xử lý lâu, trọng số thay đổi (kẹt xe) phải tính lại.
- **ALT** (A\*, Landmarks, Triangle inequality), Goldberg và Harrelson (2005): chọn vài node mốc (landmark), tính trước khoảng cách từ mốc tới mọi node và ngược lại. Heuristic h(v) = max theo các mốc L của max(d(L, t) − d(L, v), d(v, L) − d(t, L)), chấp nhận được nhờ bất đẳng thức tam giác. Tốn bộ nhớ: số mốc × số node.
- OSRM dùng CH và Multi-Level Dijkstra, GraphHopper dùng CH và Landmarks (liên hệ chương 3).

### 1.12 Bảng so sánh các thuật toán

| Thuật toán | Đường ngắn nhất trên đồ thị có trọng số? | Độ phức tạp truy vấn | Tiền xử lý | Bộ nhớ thêm | Ưu điểm | Nhược điểm |
|---|---|---|---|---|---|---|
| BFS | Không (chỉ đúng khi trọng số bằng nhau) | O(V + E) | Không | O(V) | Đơn giản | Sai với trọng số khác nhau |
| DFS | Không | O(V + E) | Không | O(V) | Đơn giản | Không cho đường ngắn nhất |
| Dijkstra | Có (trọng số không âm) | O((V + E) log V) | Không | O(V) | Chắc chắn đúng, dễ cài | Duyệt lan mọi hướng |
| A\* | Có (h chấp nhận được) | Xấu nhất như Dijkstra, thực tế ít hơn | Không | O(V) | Duyệt có hướng về đích | Cần tọa độ, heuristic tốt |
| Bidirectional | Có | Thực tế khoảng một nửa Dijkstra | Không | O(V) | Nhanh hơn Dijkstra | Cần đồ thị ngược, điều kiện dừng khó |
| CH | Có | Rất nhanh | Có, lâu | Thêm cạnh tắt | Phù hợp bản đồ rất lớn | Trọng số đổi phải tính lại |
| ALT | Có | Nhanh hơn A\* Haversine | Có | Số mốc × V | Heuristic tốt hơn | Tốn bộ nhớ |

### 4.4 Cài đặt thuật toán và kiểm thử trong ứng dụng

- Cấu trúc kết quả chung của mọi thuật toán (`path`, `distance_m`, `visited_count`, `visited_nodes`, `runtime_ms`).
- Cách dùng `heapq`: không giảm khóa được nên đẩy bản ghi mới, bỏ qua bản ghi cũ khi lấy ra.
- Xử lý cạnh song song, trường hợp không có đường (`NoPathError` → HTTP 404).
- Đo thời gian bằng `time.perf_counter()`.
- Kiểm thử: danh sách test, kết quả `pytest`, đối chiếu với `networkx.shortest_path_length` trên bản đồ thật.

### Slide của TV3

1. Mạng đường thành đồ thị có hướng có trọng số.
2. Dijkstra: ý tưởng, độ phức tạp, hình vùng duyệt.
3. A\*: f = g + h, heuristic Haversine, vì sao vẫn tối ưu, hình vùng duyệt.
4. Bidirectional, CH, ALT (mỗi cái 1–2 ý).
5. Bảng so sánh thuật toán.

### Câu hỏi hay gặp

| Câu hỏi | Gợi ý trả lời |
|---|---|
| Vì sao Dijkstra sai khi có trọng số âm? | Dijkstra chốt node khi lấy ra khỏi hàng đợi; cạnh âm có thể làm một đường đi qua node khác ngắn hơn sau khi đã chốt. |
| Vì sao A\* vẫn cho đường ngắn nhất? | Haversine không bao giờ lớn hơn đường thật còn lại (chấp nhận được) và nhất quán, nên node được lấy ra với f nhỏ nhất thì đã tối ưu. |
| Heuristic ước lượng quá thì sao? | Duyệt ít hơn, chạy nhanh hơn nhưng có thể trả về đường không ngắn nhất. |
| Vì sao A\* giảm số node nhiều hơn giảm thời gian? | Mỗi node A\* phải tính thêm Haversine (hàm lượng giác), nên chi phí mỗi bước lớn hơn Dijkstra. |
| Đẩy trùng phần tử vào heap có sai không? | Không: bản ghi cũ có khoảng cách lớn hơn, khi lấy ra node đã được chốt nên bị bỏ qua. Đổi lại heap lớn hơn một chút. |
| "Node đã duyệt" tính thế nào? | Node được lấy ra khỏi hàng đợi lần đầu (đã chốt khoảng cách), không tính node mới chỉ được thêm vào hàng đợi. |
| Làm sao biết thuật toán đúng? | Test trên đồ thị nhỏ biết trước đáp án và so với `networkx.shortest_path_length` trên bản đồ thật: cùng độ dài. |
| Vì sao Google, OSRM nhanh hơn nhiều? | Dùng tiền xử lý (CH, MLD) và viết bằng C++; nhóm chạy Dijkstra/A\* thuần bằng Python, không tiền xử lý. |

---

## 4. TV4 – Hệ thống tìm đường thực tế

**Viết:** chương 3 (`1.11`) và mục 4.5. **Làm thêm:** chụp hình giao diện cho cả báo cáo.

### 3.1 Cấu trúc chung của một hệ thống tìm đường

Sơ đồ các bước: dữ liệu bản đồ (OSM hoặc dữ liệu riêng) → tiền xử lý (dựng đồ thị theo **hồ sơ phương tiện**: tốc độ từng loại đường, đường cấm, cấm rẽ) → cấu trúc tăng tốc (CH, MLD, tile phân cấp) → dịch vụ truy vấn qua API → hậu xử lý (chỉ dẫn từng bước, mã hóa đường đi).

### 3.2 OSRM (Open Source Routing Machine)

- Viết bằng C++, mã nguồn mở (giấy phép BSD), dùng dữ liệu OSM.
- Hồ sơ phương tiện viết bằng Lua (ô tô, xe đạp, đi bộ).
- Hai cách tăng tốc: **CH** (truy vấn rất nhanh) và **MLD** (Multi-Level Dijkstra, cập nhật trọng số như tình trạng giao thông nhanh hơn CH).
- Các dịch vụ: `route` (tìm đường), `table` (ma trận khoảng cách), `match` (khớp vết GPS vào đường), `trip` (bài toán người du lịch), `nearest`.
- Có máy chủ demo công khai (TV5 dùng để đối chiếu).

### 3.3 GraphHopper

- Viết bằng Java, mã nguồn mở (Apache 2.0), dùng dữ liệu OSM.
- Hỗ trợ CH (nhanh, ít linh hoạt) và Landmarks/ALT (chậm hơn CH nhưng đổi được trọng số khi truy vấn).
- Tùy chỉnh hồ sơ phương tiện, có thêm isochrone (vùng đến được trong X phút), map matching.

### 3.4 Valhalla

- Viết bằng C++, mã nguồn mở (MIT), khởi đầu từ Mapzen.
- Dữ liệu chia thành ô (tile) theo nhiều cấp, nạp từng phần nên tốn ít bộ nhớ.
- Tính chi phí linh hoạt lúc truy vấn (dynamic costing): ô tô, xe máy, xe tải, xe đạp, đi bộ, kết hợp phương tiện công cộng.

### 3.5 Google Maps Directions API / Routes API

- Dịch vụ đóng, dữ liệu riêng của Google, có giao thông thời gian thực và dữ liệu lịch sử để dự đoán thời gian đi.
- Trả phí theo lượt gọi, không tự triển khai được, không biết thuật toán bên trong.
- Google đang chuyển dần từ Directions API sang Routes API (kiểm tra lại khi viết).

### 3.6 Bảng so sánh

| Tiêu chí | OSRM | GraphHopper | Valhalla | Google |
|---|---|---|---|---|
| Ngôn ngữ | C++ | Java | C++ | Không công bố |
| Giấy phép | BSD | Apache 2.0 | MIT | Thương mại |
| Dữ liệu | OSM | OSM | OSM | Riêng |
| Kỹ thuật tăng tốc | CH, MLD | CH, Landmarks | Tile phân cấp | Không công bố |
| Đổi trọng số khi truy vấn | Hạn chế (MLD tốt hơn) | Có (chế độ linh hoạt) | Có | Có |
| Giao thông thời gian thực | Tự đưa dữ liệu vào | Tự đưa dữ liệu vào | Tự đưa dữ liệu vào | Có sẵn |
| Tự triển khai | Được | Được | Được | Không |

### 3.7 Liên hệ với ứng dụng của nhóm

- Nhóm dùng Dijkstra và A\* thuần, không tiền xử lý: đủ nhanh cho một quận nhưng không đủ cho cả thành phố hay quốc gia.
- Các hệ thống thực tế còn tính cấm rẽ, thời gian rẽ, đèn tín hiệu, tốc độ theo giờ; nhóm chỉ dùng độ dài.
- Dẫn kết quả đối chiếu với OSRM/Google từ chương 5 của TV5.

### 4.5 Giao diện bản đồ

- Leaflet và react-leaflet, nền tile OSM (không cần API key).
- Cách chọn điểm (click lần 1, lần 2, lần 3 chọn lại), kéo thả marker, khung bao quận.
- Vẽ đường đi bằng Polyline, node đã duyệt bằng CircleMarker; dùng canvas thay SVG để vẽ hàng nghìn điểm cho mượt.
- Khi so sánh: tô 2 màu, đường bên dưới vẽ dày hơn để thấy cả 2.
- Bố cục 2 cột, trên điện thoại xếp dọc.
- (Nếu làm) animation duyệt node, tìm địa chỉ bằng Nominatim.

**Danh sách hình cần chụp cho cả nhóm:** màn hình ban đầu; kết quả Dijkstra; kết quả A\* cùng cặp điểm; màn hình So sánh có biểu đồ; trang benchmark; thông báo lỗi khi chọn ngoài vùng; giao diện trên điện thoại; trang `/docs` của BE. Chụp cùng cặp điểm cho Dijkstra và A\* để so sánh được.

### Slide của TV4

1. Cấu trúc chung của một hệ thống tìm đường.
2. Bảng so sánh OSRM, GraphHopper, Valhalla, Google.
3. Giao diện ứng dụng của nhóm (ảnh chụp) và cùng TV1 chạy demo.

### Câu hỏi hay gặp

| Câu hỏi | Gợi ý trả lời |
|---|---|
| Vì sao dùng Leaflet mà không dùng Google Maps JavaScript? | Leaflet miễn phí, mã nguồn mở, không cần API key, dùng được với tile OSM. |
| OSRM nhanh nhờ đâu? | Tiền xử lý CH hoặc MLD trước, khi truy vấn chỉ duyệt rất ít node; viết bằng C++. |
| CH khác MLD thế nào? | CH thêm cạnh tắt theo thứ tự node, truy vấn rất nhanh nhưng đổi trọng số phải tính lại; MLD chia bản đồ thành nhiều cấp vùng, cập nhật trọng số nhanh hơn. |
| Vì sao đường của nhóm khác đường Google gợi ý? | Google tính thời gian (có kẹt xe, đèn đỏ, cấm rẽ), nhóm tính độ dài; dữ liệu khác nhau; nhóm bắt điểm click về node gần nhất. |
| Vì sao đường đi không bắt đầu đúng chỗ click? | BE bắt điểm click về giao lộ (node) gần nhất trên đồ thị. |
| Vẽ 5000 điểm có chậm không? | Dùng chế độ canvas của Leaflet nên vẫn mượt; BE cũng chỉ gửi tối đa 5000 điểm. |

---

## 5. TV5 – Đánh giá thực nghiệm

**Viết:** chương 5 (`1.13`) và mục 4.6. **Làm thêm:** gửi số liệu chính cho TV1 điền vào kết luận.

### 5.1 Môi trường thử nghiệm

Bảng: CPU, RAM, hệ điều hành, phiên bản Python, bản đồ (tên quận, số node, số cạnh sau khi lọc), số cặp điểm, `seed`.

### 5.2 Phương pháp

- Chọn ngẫu nhiên N cặp node (100 cặp) bằng `random.Random(seed)` để chạy lại ra cùng bộ dữ liệu.
- Mỗi cặp chạy cả Dijkstra và A\*, ghi: độ dài, thời gian chạy, số node đã duyệt, khoảng cách đường chim bay giữa 2 điểm.
- Thời gian ở mức mili giây nên dễ nhiễu: chạy 3 lần cùng `seed`, lấy trung vị; tắt bớt ứng dụng nặng khi đo.
- Chia cặp điểm theo khoảng cách chim bay: dưới 1 km, 1–2 km, trên 2 km.

### 5.3 Kiểm tra độ đúng

- Tỉ lệ cặp có độ dài Dijkstra = A\* (kỳ vọng 100%).
- Đối chiếu với `networkx.shortest_path_length` (dẫn kết quả test của TV3).

### 5.4 Kết quả hiệu năng

Bảng tổng hợp:

| Chỉ số | Dijkstra | A\* | A\* so với Dijkstra |
|---|---|---|---|
| Độ dài trung bình (m) | | | bằng nhau |
| Thời gian trung bình (ms) | | | giảm …% |
| Thời gian trung vị (ms) | | | |
| Số node duyệt trung bình | | | giảm …% |
| Số cặp A\* nhanh hơn | | … / N | |

Bảng theo nhóm khoảng cách:

| Khoảng cách chim bay | Số cặp | Node duyệt TB (Dijkstra / A\*) | Thời gian TB (Dijkstra / A\*) | Tỉ lệ node A\*/Dijkstra |
|---|---|---|---|---|
| Dưới 1 km | | | | |
| 1–2 km | | | | |
| Trên 2 km | | | | |

Biểu đồ nên có: cột so sánh trung bình; cột theo nhóm khoảng cách; biểu đồ chấm "số node duyệt theo khoảng cách chim bay" (mỗi thuật toán một màu); ảnh vùng duyệt của 2 thuật toán trên cùng cặp điểm.

### 5.5 Đối chiếu với OSRM hoặc Google Maps

| Tuyến | Điểm đi → điểm đến | Ứng dụng nhóm (m) | OSRM (m) | Google Maps (m) | Chênh lệch | Giải thích |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

5–10 tuyến. Nguyên nhân chênh lệch thường gặp: cấm rẽ, hồ sơ phương tiện khác, phiên bản dữ liệu khác, Google tối ưu theo thời gian, nhóm bắt điểm về node gần nhất.

### 5.6 Nhận xét (kiểm tra lại bằng số liệu thật)

- Dijkstra và A\* luôn cho cùng độ dài, phù hợp lý thuyết heuristic chấp nhận được.
- A\* duyệt ít node hơn rõ rệt; chênh lệch càng lớn khi 2 điểm càng xa.
- Thời gian chạy giảm ít hơn số node duyệt giảm, vì A\* tốn thêm chi phí tính Haversine cho mỗi node.
- Với 2 điểm rất gần, hai thuật toán gần như bằng nhau.

### 5.7 Hạn chế của thí nghiệm

Thời gian đo bằng Python có nhiễu; chỉ thử trên một quận; trọng số là độ dài, không phải thời gian; cặp điểm chọn ngẫu nhiên, không phải các tuyến người dùng hay đi.

### 4.6 Bảng điều khiển, số liệu, so sánh, benchmark

- Các thành phần giao diện: chọn thuật toán, nút Tìm đường / So sánh / Xóa, bật tắt node đã duyệt, bảng số liệu, biểu đồ Recharts, trang benchmark có xuất CSV.
- API `GET /api/compare` và `GET /api/benchmark`: tham số, kết quả trả về.

### Slide của TV5

1. Phương pháp thử nghiệm (môi trường, số cặp, cách đo).
2. Bảng tổng hợp và biểu đồ so sánh.
3. Kết quả theo nhóm khoảng cách, đối chiếu OSRM/Google.
4. Nhận xét.

### Câu hỏi hay gặp

| Câu hỏi | Gợi ý trả lời |
|---|---|
| Vì sao phải cố định `seed`? | Để chạy lại ra cùng các cặp điểm, người khác kiểm tra lại được kết quả. |
| Vì sao lấy trung vị mà không chỉ lấy trung bình? | Thời gian chạy hay có vài lần bị chậm đột biến (máy bận); trung vị ít bị ảnh hưởng bởi các giá trị này. |
| 100 cặp có đủ không? | Đủ để thấy xu hướng rõ (A\* luôn duyệt ít hơn); muốn chắc hơn thì tăng số cặp hoặc chạy nhiều `seed`. |
| Vì sao thời gian giảm ít hơn số node giảm? | Mỗi bước A\* phải tính thêm Haversine. |
| Vì sao kết quả khác Google? | Xem mục 5.5: Google tối ưu thời gian, có dữ liệu giao thông và cấm rẽ. |
| Khoảng cách chim bay dùng để làm gì? | Chia cặp điểm thành gần, vừa, xa để xem A\* có lợi nhất ở trường hợp nào. |

---

## 6. Buổi thuyết trình

Thứ tự gợi ý (điều chỉnh theo thời gian môn học cho phép):

| Thứ tự | Phần | Người | Thời gian | Số slide |
|---|---|---|---|---|
| 1 | Mở đầu, mục tiêu, kiến trúc | TV1 | 2 phút | 3 |
| 2 | Tổng quan bản đồ số | TV2 | 3 phút | 4 |
| 3 | Thuật toán | TV3 | 4 phút | 5 |
| 4 | Hệ thống tìm đường thực tế | TV4 | 2 phút | 2 |
| 5 | Demo trực tiếp | TV1, TV4 | 3 phút | 1 |
| 6 | Đánh giá thực nghiệm | TV5 | 3 phút | 4 |
| 7 | Kết luận, hướng phát triển | TV1 | 1 phút | 1 |

Kịch bản demo: theo mục 6 của [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md). Chuẩn bị sẵn: BE đã có file cache bản đồ (không tải lại lúc demo), 2 cặp điểm đã thử trước, ảnh chụp dự phòng nếu máy chiếu hoặc mạng gặp sự cố (tile bản đồ cần Internet).

Mỗi người phải trả lời được câu hỏi về phần mình và nắm được luồng chính của cả hệ thống (mục 4.1).

---

## 7. Checklist nộp phần báo cáo

- [ ] File Markdown trong `docs/bao-cao/`, hình trong `docs/bao-cao/hinh/`.
- [ ] Đủ các mục theo dàn ý ở trên, có số liệu thật của nhóm.
- [ ] Hình và bảng có đánh số, chú thích, được nhắc tới trong bài.
- [ ] Có danh sách tài liệu tham khảo cuối file.
- [ ] Tự đọc lại chính tả, thuật ngữ thống nhất với các phần khác.
- [ ] Tạo Pull Request nhánh `docs/...` vào `main`, gửi nhóm trưởng **trước tuần 5** để kịp ghép báo cáo và làm slide.
- [ ] Đánh dấu `[x]` mục tương ứng trong [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md).
