<div class="signup">
    <div class="container">
        <div class="signup__content">
            <div class="signup__form">
                <div class="form-header">
                    <img src="bamboo-logo.png" alt="QAirline Logo" class="logo">
                    <h2>Bạn đã sẵn sàng đăng ký tài khoản tại QAirline? Hãy bắt đầu ngay!</h2>
                    <p>Vui lòng điền đầy đủ thông tin cá nhân giống trên CMND/CCCD của bạn.</p>
                </div>
                <fieldset class="personal-info">
                <legend>Thông tin cá nhân</legend>
                
                <div class="signup__group">
                    <div class="form-group">
                        <label for="lastname">Họ</label>
                        <input type="text" id="lastname" name="lastname" placeholder="Họ, ví dụ: PHAM">
                    </div>
    
                    <div class="form-group">
                        <label for="fullname">Tên đệm & Tên</label>
                        <input type="text" id="fullname" name="fullname" placeholder="Tên đệm & Tên">
                    </div>
                </div>

                <div class="form-group">
                    <label for="birthdate">Ngày, Tháng, Năm Sinh</label>
                    <input type="date" id="birthdate" name="birthdate">
                </div>

                <div class="form-group">
                    <label for="gender">Giới tính</label>
                    <select id="gender" name="gender">
                        <option value="">Giới tính</option>
                        <option value="male">Nam</option>
                        <option value="female">Nữ</option>
                        <option value="other">Khác</option>
                    </select>
                </div>
            </fieldset>

            <fieldset class="contact-info">
                <legend>Thông tin liên hệ</legend>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="Email của bạn">
                </div>

                <div class="form-group">
                    <label for="phone">Số điện thoại</label>
                    <input type="tel" id="phone" name="phone" placeholder="Số điện thoại">
                </div>

                <div class="form-group">
                    <label for="country">Quốc tịch</label>
                    <input type="text" id="country" name="country" placeholder="Quốc tịch">
                </div>
            </fieldset>

            <div class="form-group">
                <input type="checkbox" id="terms" name="terms">
                <label for="terms">Tôi đã đọc và đồng ý với các điều khoản và điều kiện của Bamboo Airways và Bamboo Club.</label>
            </div>

            <button type="submit" class="submit-btn">Đăng ký</button>
            </div>
            <div class="signup__image">
            </div>
        </div>
    </div>
</div>