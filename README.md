
# MS-MILP CVaR: Multistage Stochastic Portfolio Optimization under Geopolitical Risk

Dự án này triển khai mô hình **Tối ưu hóa danh mục đầu tư đa giai đoạn tuyến tính nguyên hỗn hợp dựa trên giá trị rủi ro có điều kiện (MS-MILP CVaR)** ứng phó với bất định từ rủi ro địa chính trị (GPR). Mô hình được hiện thực hóa bằng ngôn ngữ lập trình Python, tích hợp quy trình xử lý dữ liệu vĩ mô, phân cụm kịch bản, và giải bài toán quy hoạch ngẫu nhiên động qua cây kịch bản phân nhánh.

## Các tính năng cốt lõi
- **Phân đoạn thị trường động:** Gán nhãn trạng thái thị trường (Bình thường - N, Căng thẳng - C, Chiến tranh - W) dựa trên các ngưỡng phân vị của chỉ số Geopolitical Risk (GPR).
- **Học cấu trúc rủi ro lịch sử:** Sử dụng thuật toán phân cụm K-means để trích xuất các tâm kịch bản lợi nhuận lũy kế thay vì giả định phân phối chuẩn.
- **Mô hình hóa chuỗi thời gian ngẫu nhiên:** Ước lượng ma trận xác suất chuyển trạng thái Markov bậc một để điều khiển quy trình mô phỏng cây kịch bản Monte Carlo ($T=5$, $S=200$).
- **Tối ưu hóa đa giai đoạn với Recourse động:** Giải quyết bài toán quy hoạch nguyên hỗn hợp (MIP) thông qua thư viện `CVXPY` và bộ giải `GLPK_MI` hoặc `HiGHS`.
- **Ràng buộc ma sát thực tế:** Tích hợp đầy đủ chi phí giao dịch phẳng ($\phi = 0.2\%$), giới hạn tỷ trọng ($5\% \le x \le 40\%$), và kiểm soát số lượng tài sản tối đa đầu tư đồng thời ($M \le 4$).

## 🗂 Cấu trúc thư mục dữ liệu đầu vào
Hệ thống xử lý danh mục bao gồm 7 quỹ ETF đại diện cho các lớp tài sản toàn cầu:
- **Cổ phiếu:** `VTI` (Vốn hóa lớn), `IWM` (Vốn hóa nhỏ).
- **Trái phiếu:** `AGG` (Tổng hợp), `LQD` (Doanh nghiệp), `MUB` (Đô thị).
- **Tài sản trú ẩn & Hàng hóa:** `GLD` (Vàng), `DBC` (Hàng hóa tổng hợp).

## 🚀 Hướng dẫn cài đặt và khởi chạy

### 1. Yêu cầu môi trường
Đảm bảo máy tính của bạn đã cài đặt Python (phiên bản $\ge 3.8$). Các thư viện phụ thuộc bắt buộc bao gồm:

```bash
pip install numpy pandas matplotlib scipy cvxpy yfinance
```
### 2. Hướng dẫn chạy file
```bash
notebooks.ipynb         <-- File notebook thực thi chính
└── src/
        ├── data.py             <-- các hàm tải dữ liệu ETF từ Yahoo Finance
        ├── gpr.py              <-- các hàm xử lý chỉ số GPR vĩ mô
        └── scenario.py         <-- các hàm xây dụng cây kịch bản
└── data/              <-- dữ liệu GPR
```
