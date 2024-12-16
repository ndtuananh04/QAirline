<div class="menu-admin">
	<ul class="menu-admin__list">
		<li>
			<a href="/admin/manager/accounts">
				<img src="/images/account-admin.png" alt="Icon" class="menu-icon" />
				Tài khoản
			</a>
		</li>
		<li>
			<a href="/admin/manager/airplanes">
				<img src="/images/plane-admin.png" alt="Icon" class="menu-icon" />
				Máy bay
			</a>
		</li>
		<li>
			<a href="/admin/manager/flights">
				<img src="/images/flight-admin.png" alt="Icon" class="menu-icon" />
				Chuyến bay
			</a>
		</li>
		<li>
			<a href="/admin/manager/seats">
				<img src="/images/seat-admin.png" alt="Icon" class="menu-icon" />
				Ghế
			</a>
		</li>
		<li>
			<a href="/admin/manager/posts">
				<img src="/images/post-admin.png" alt="Icon" class="menu-icon" />
				Thông báo
			</a>
		</li>
	</ul>
</div>

<style>
	.menu-icon {
		width: 20px; /* Chiều rộng ảnh */
		height: 20px; /* Chiều cao ảnh */
		margin-right: 8px; /* Khoảng cách giữa ảnh và chữ */
		vertical-align: middle; /* Căn giữa ảnh với chữ */
	}

	.menu-admin__list li a {
        display: flex;
        align-items: center; /* Căn giữa ảnh và chữ theo chiều dọc */
        text-decoration: none; /* Loại bỏ gạch chân */
        color: #333; /* Màu chữ mặc định */
        background-color: transparent; /* Nền mặc định */
        padding: 8px 12px; /* Tạo khoảng cách bên trong */
        border-radius: 4px; /* Bo góc */
        transition: all 0.3s ease; /* Tạo hiệu ứng mượt khi thay đổi */
    }

    .menu-admin__list li a:hover {
        color: #fff; /* Màu chữ khi hover */
        background-color: #d3d3d3; /* Màu nền khi hover */
    }

</style>
