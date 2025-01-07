1. API Đăng ký tài khoản
Người dùng thực hiện:
Nhấn vào nút "Đăng ký" trên giao diện.
Giao diện yêu cầu nhập thông tin: Tên, email, mật khẩu (được mã hóa), địa chỉ, số điện thoại.
Hiển thị:
Nếu đăng ký thành công: Giao diện hiển thị thông báo "Đăng ký thành công" hoặc tự động chuyển hướng đến màn hình đăng nhập.
Nếu thất bại (email trùng hoặc dữ liệu sai): Hiển thị thông báo lỗi cụ thể (ví dụ: "Email đã tồn tại" hoặc "Dữ liệu không hợp lệ").
API thực hiện:
Request: Gửi thông tin người dùng (tên, email, mật khẩu đã mã hóa, địa chỉ, số điện thoại) tới API.
Xử lý trên server:
Kiểm tra xem email đã tồn tại chưa.
Nếu chưa tồn tại, lưu thông tin người dùng vào collection Users.
Trả về mã phản hồi (success hoặc error).
Admin:
Admin có thể xem danh sách người dùng đã đăng ký.
2. API Đăng nhập
Người dùng thực hiện:
Nhấn vào nút "Đăng nhập" trên giao diện và nhập email, mật khẩu.
Hiển thị:
Nếu đăng nhập thành công: Chuyển đến trang chủ của website.
Nếu thất bại (sai email/mật khẩu): Hiển thị thông báo lỗi ("Email hoặc mật khẩu không đúng").
API thực hiện:
Request: Gửi email và mật khẩu của người dùng tới API.
Xử lý trên server:
Kiểm tra email và mật khẩu.
Nếu hợp lệ, tạo token JWT để xác thực người dùng và gửi về client.
Nếu không hợp lệ, trả về thông báo lỗi.
Admin:
Admin có thể quản lý thông tin đăng nhập và hủy token nếu cần.
3. API Giỏ hàng
Người dùng thực hiện:
Nhấn vào sản phẩm và chọn "Thêm vào giỏ hàng".
Có thể xem giỏ hàng bằng cách nhấn vào biểu tượng giỏ hàng.
Hiển thị:
Khi thêm sản phẩm vào giỏ hàng: Hiển thị thông báo "Thêm vào giỏ hàng thành công".
Khi xem giỏ hàng: Hiển thị danh sách sản phẩm đã chọn, số lượng, giá cả và tổng tiền.
API thực hiện:
Thêm vào giỏ hàng:

Gửi user_id, product_id, và quantity tới API.
API kiểm tra xem sản phẩm có tồn tại không.
Thêm vào collection Cart và trả về phản hồi.
Xem giỏ hàng:

Gửi user_id tới API.
API truy vấn dữ liệu giỏ hàng của người dùng từ collection Cart.
Admin:
Admin có thể theo dõi giỏ hàng để phân tích hành vi người dùng.
4. API Đặt hàng
Người dùng thực hiện:
Nhấn vào nút "Thanh toán" trên giao diện giỏ hàng.
Nhập thông tin thanh toán hoặc địa chỉ giao hàng nếu cần.
Hiển thị:
Nếu đặt hàng thành công: Hiển thị thông báo "Đặt hàng thành công" và chi tiết đơn hàng.
Nếu thất bại (lỗi thanh toán, sản phẩm hết hàng): Hiển thị thông báo lỗi cụ thể.
API thực hiện:
Request: Gửi thông tin đặt hàng (bao gồm user_id, danh sách sản phẩm, tổng tiền, địa chỉ giao hàng).
Xử lý trên server:
Kiểm tra giỏ hàng và xác nhận số lượng sản phẩm.
Tạo đơn hàng mới trong collection Orders.
Cập nhật trạng thái sản phẩm trong kho (ví dụ: giảm số lượng).
Admin:
Admin có thể theo dõi danh sách đơn hàng.
Quản lý trạng thái đơn hàng (đang xử lý, đã giao, hủy).
Phê duyệt hoặc xử lý các vấn đề liên quan đến đặt hàng (ví dụ: kiểm tra thanh toán, xử lý đơn hàng bị lỗi).