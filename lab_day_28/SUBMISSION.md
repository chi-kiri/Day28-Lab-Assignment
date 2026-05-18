# Hướng Dẫn Nộp Bài - Lab #28: Full Platform Integration Sprint

## Yêu Cầu Nộp Bài

**Full AI infrastructure platform demo** - từ data ingestion đến model serving với full observability.

## Các Artifacts Cần Nộp

### 1. Source Code
- Folder `lab28/` hoàn chỉnh với tất cả files
- Tất cả integration scripts hoạt động
- Prefect flows đã deploy và schedule

### 2. Screenshots Demo
Chụp màn hình các bước:
- Prefect UI: http://localhost:4200 (flow đang chạy)
- API Gateway call: `curl http://localhost:8000/health`
- Grafana dashboard: http://localhost:3000

### 3. Kết Quả Smoke Tests
Chạy và chụp màn hình kết quả:
```bash
cd lab28
pytest smoke-tests/ -v
```
Kỳ vọng: 5/5 tests passing

### 4. Production Readiness Score
```bash
python scripts/production_readiness_check.py
```
Kỳ vọng: Score >80%

### 5. Documentation
- `README.md` giải thích cách:
  - Start platform: `docker compose up -d`
  - Deploy Prefect flows
  - Run smoke tests
  - Access dashboards (Grafana:3000, Prometheus:9090, Prefect:4200)

## Định Dạng Nộp Bài

Tạo Repo GitHub chứa:
```
lab28_submission_[student_id]
├── lab28/                    # Source code hoàn chỉnh
│   ├── docker-compose.yml
│   ├── prefect/flows/
│   ├── scripts/
│   ├── api-gateway/
│   └── monitoring/
├── screenshots/              # Screenshots demo
│   ├── prefect_ui.png
│   ├── api_gateway.png
│   └── grafana_dashboard.png
├── smoke_tests_results.png   # Screenshot kết quả pytest
├── production_readiness.png  # Screenshot readiness score
└── README.md                # Hướng dẫn setup
```

## Địa Điểm Nộp
Nộp link repo GitHub qua LMS

## Tiêu Chí Chấm Điểm

| Tiêu Chí | Trọng Số | Mô Tả |
|----------|----------|-------|
| Integration Completeness | 40% | Tất cả 10 integration points hoạt động, data flow end-to-end |
| Observability | 25% | Logs, metrics, traces hiển thị; alerts configured |
| Performance | 20% | Latency trong SLO; load tested; không có memory leaks |
| Architecture Quality | 15% | Clean separation, GitOps config, documented decisions |

## Các Vấn Đề Cần Tránh

- Config drift giữa các environments
- Thiếu error handling tại integration points
- Monitoring coverage không hoàn chỉnh
- Không có rollback strategy
- Demo không test trước khi nộp

## 5 Câu Hỏi Cần Trả Lời Khi Nộp

1. **Phân tích các trade-offs trong thiết kế kiến trúc AI platform của bạn. Bạn đã cân bằng giữa performance, reliability, và maintainability như thế nào?**
> - **Performance vs. Cost**: Dùng Qwen2.5-7B (quantized GPTQ-Int4) qua vLLM giúp đảm bảo inference siêu nhanh với phần cứng tối thiểu (GPU T4 của Kaggle).
> - **Reliability vs. Complexity**: Việc thêm Apache Kafka và API Gateway làm tăng độ phức tạp, nhưng bảo đảm dữ liệu không bị mất nếu worker sập và dễ quản lý truy cập độc lập.
> - **Maintainability**: Hệ thống được module hóa thành các microservices qua Docker Compose (Prefect, Kafka, Redis, Qdrant). Dễ deploy và chỉnh sửa từng phần độc lập.

2. **Trong kiến trúc hybrid (Local + Kaggle), bạn xử lý ngắt kết nối giữa local và Kaggle như thế nào? Có cơ chế fallback không?**
> - Sử dụng Ngrok/Cloudflared để cấp phát dynamic URL. Ở phía API Gateway local, URL được đọc qua biến môi trường (`VLLM_URL` từ file `.env`), cho phép fallback/reconnect bằng cách khởi động lại container mà không cần sửa code.
> - Cấu hình timeout và exception handling trong httpx Client giúp API trả về lỗi graceful (ví dụ 504) thay vì crash hệ thống.

3. **Giải thích cách event-driven architecture với Kafka giúp decouple các components trong AI platform của bạn.**
> Kafka đóng vai trò message queue nằm giữa Data Ingestion và Data Processing. Nhờ Kafka, các ứng dụng đẩy dữ liệu (Producers) không cần biết hệ thống xử lý phía sau (Consumers) hoạt động ra sao. Nếu Prefect worker bảo trì, dữ liệu thô vẫn lưu an toàn trên topic `data.raw`. Khi worker bật lại, nó tiếp tục đọc từ offset cũ mà không rớt dữ liệu.

4. **Bạn đã implement observability như thế nào? Logs, metrics, và traces được thu thập và visualized ra sao?**
> - **Metrics**: Dùng `prometheus-fastapi-instrumentator` trong API Gateway để tự động theo dõi RPS, Error Rate, và Latency. Prometheus kéo (scrape) các thông số này về.
> - **Visualization**: Các metrics được hiển thị trực quan thông qua Grafana dashboard giúp theo dõi trạng thái hệ thống theo thời gian thực.
> - **Traces**: (Optionally) LangSmith được tích hợp vào luồng LLM để lưu vết chất lượng phản hồi ở cấp độ AI prompt.

5. **Nếu một service trong stack (ví dụ: Qdrant hoặc Kafka) bị crash, hệ thống của bạn sẽ xử lý như thế nào? Có graceful degradation không?**
> Có. Hệ thống được bảo vệ qua retry và error handling:
> - Kafka crash: Prefect flows có cơ chế retry tự động (`@flow(retries=3)`).
> - Qdrant crash: API Gateway bắt (catch) lỗi từ HTTPX client, có thể cấu hình bypass RAG (trả lời chay) thay vì sập toàn hệ thống.
> - Docker compose dùng rule `restart: always` để vực dậy các container lỗi.

## Câu Hỏi Thêm?
Liên hệ giảng viên qua LMS hoặc office hours.
