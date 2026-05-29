"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)"""
    # 1. Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # 2. Infection: Nhập dữ liệu hợp lệ
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # 3. Propagation: Chờ nút "Đăng xuất" xuất hiện
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # 4. Revealability: Kiểm tra kết quả
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


@pytest.mark.parametrize(
    "email_input, password_input, expected_error, tc_id",
    [
        ("ba.nguyen@email.com", "wrongpassword", "Mật khẩu không đúng", "TC-02"),
        ("", "", "Vui lòng nhập email và mật khẩu", "TC-03"),
    ]
)
def test_login_failure(page, test_config, email_input, password_input, expected_error, tc_id):
    """TC-02 & TC-03: Kiểm thử đăng nhập thất bại (Data-Driven Testing)"""
    # 1. Arrange - Truy cập trang
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # 2. Act - Thực hiện nhập dữ liệu (nếu có) và nhấn Đăng nhập
    if email_input:
        flutter_fill(page, "Email", email_input)
    if password_input:
        flutter_fill(page, "Mật khẩu", password_input)
        
    flutter_click_button(page, "Đăng nhập")

    # 3. Smart Wait - Chờ thông báo lỗi xuất hiện trong Semantics Tree
    wait_for_flutter(page, text=expected_error)
    
    # Chụp ảnh minh chứng lưu vào thư mục screenshots/
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"{tc_id.lower()}_fail.png"))

    # 4. Assert - Kiểm tra thông báo lỗi hiển thị trên màn hình
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, f"Không tìm thấy thông báo lỗi mong đợi: {expected_error}"
