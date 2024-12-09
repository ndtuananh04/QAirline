<script>
	import { quantity, tripType } from '../../store';
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';

	let forms = Array.from({ length: get(quantity) }, (_, i) => ({
		identification: '',
		family_name: '',
		given_name: '',
		gender: '',
		nationality: '',
		date_of_birth: '',
		phone_number: '',
		email: ''
	}));

	let errorMessages = Array.from({ length: get(quantity) }, () => ({
		family_name: '',
		given_name: '',
		email: '',
		nationality: '',
		phone_number: '',
		identification: ''
	}));

	const handleSubmit = async (e) => {
		e.preventDefault();
		const token = localStorage.getItem('jwt');
		if (!token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập lại.');
			goto('/user/login');
			return;
		}
		// Chuẩn bị dữ liệu payload từ các form
		const payload = {
			trip_type: get(tripType),
			passengers: forms.map((form) => ({
				identification: form.identification,
				family_name: form.family_name,
				given_name: form.given_name,
				gender: form.gender,
				nationality: form.nationality,
				date_of_birth: form.date_of_birth,
				phone_number: form.phone_number,
				email: form.email
			}))
		};

		console.log('Form Data:', payload);

		try {
			const response = await fetch('http://localhost:5000/ticket-customer', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify(payload),
				credentials: 'include'
			});

			if (!response.ok) {
				throw new Error(`Failed to register: ${response.statusText}`);
			}
			alert('Mua vé thành công');
			goto('/user/dashboard');
		} catch (error) {
			console.error('Mua vé không thành công:', error);
			alert('Mua vé không thành công thử lại!');
		}
	};

	const handleInputChange = (field, index, value) => {
		// Tạo bản sao dữ liệu
		let updatedForms = [...forms];
		let updatedErrors = [...errorMessages];

		switch (field) {
			case 'email':
				if (value && !/^[a-zA-Z0-9._%+-]+@gmail\.com$/.test(value)) {
					updatedErrors[index].email = 'Email phải có định dạng @gmail.com';
				} else {
					updatedErrors[index].email = '';
				}
				break;

			case 'family_name':
			case 'given_name':
			case 'nationality':
				if (/[^a-zA-Z\s]/.test(value)) {
					updatedErrors[index][field] =
						`${field === 'family_name' ? 'Họ' : field === 'given_name' ? 'Tên' : 'Quốc tịch'} không được nhập ký tự đặc biệt hoặc số.`;
				} else {
					updatedErrors[index][field] = '';
					value = value.toUpperCase();
				}
				break;

			case 'phone_number':
			case 'identification':
				if (!/^\d*$/.test(value)) {
					updatedErrors[index][field] =
						`${field === 'phone_number' ? 'Số điện thoại' : 'CMND/CCCD'} chỉ được nhập số.`;
				} else {
					updatedErrors[index][field] = '';
				}
				break;
		}

		// Cập nhật giá trị form
		updatedForms[index][field] = value;

		// Gán lại state
		forms = updatedForms;
		errorMessages = updatedErrors;
	};
</script>

<div class="formbold-main-wrapper">
	<form class="signup__form" on:submit={handleSubmit}>
		{#each forms as form, index}
			<div class="formbold-form-container">
				<div class="formbold-form-wrapper">
					<div class="formbold-title-center">
						<p>Người thứ {index + 1}</p>
					</div>

					<div class="formbold-input-flex">
						<div>
							<label for="family_name" class="formbold-form-label"> Họ </label>
							<input
								type="text"
								name="family_name"
								id="family_name"
								placeholder="Ví dụ: NGUYEN"
								bind:value={form.family_name}
								on:input={(e) => handleInputChange('family_name', index, e.target.value)}
								class="formbold-form-input {errorMessages[index].family_name ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages[index].family_name}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages[index].family_name}</span>
								</div>
							{/if}
						</div>
						<div>
							<label for="given_name" class="formbold-form-label"> Tên </label>
							<input
								type="text"
								name="given_name"
								id="given_name"
								placeholder="Ví dụ: VAN A"
								bind:value={form.given_name}
								on:input={(e) => handleInputChange('given_name', index, e.target.value)}
								class="formbold-form-input {errorMessages[index].given_name ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages[index].given_name}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages[index].given_name}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="formbold-input-flex">
						<div>
							<label for="date_of_birth" class="formbold-form-label"> Ngày, Tháng, Năm Sinh </label>
							<input
								type="date"
								name="date_of_birth"
								id="date_of_birth"
								bind:value={form.date_of_birth}
								class="formbold-form-input"
								required
							/>
						</div>
						<div>
							<label for="gender" class="formbold-form-label"> Giới Tính </label>
							<select
								id="gender"
								name="gender"
								bind:value={form.gender}
								class="formbold-form-input"
							>
								<option value="" disabled selected hidden>Chọn giới tính</option>
								<option value="male">Nam</option>
								<option value="female">Nữ</option>
								<option value="other">Khác</option>
							</select>
						</div>
					</div>

					<div class="formbold-mb-3">
						<div>
							<label for="identification" class="formbold-form-label"> CMND/CCCD </label>
							<input
								type="text"
								name="identification"
								id="identification"
								placeholder="CMND/CCCD"
								bind:value={form.identification}
								on:input={(e) => handleInputChange('identification', index, e.target.value)}
								class="formbold-form-input {errorMessages[index].identification
									? 'input-error'
									: ''}"
								required
							/>
							{#if errorMessages[index].identification}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages[index].identification}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="formbold-mb-3">
						<div>
							<label for="email" class="formbold-form-label"> Email </label>
							<input
								type="email"
								name="email"
								id="email"
								placeholder="Email của bạn"
								bind:value={form.email}
								on:input={(e) => handleInputChange('email', index, e.target.value)}
								class="formbold-form-input {errorMessages[index].email ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages[index].email}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages[index].email}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="formbold-input-flex">
						<div>
							<label for="phone_number" class="formbold-form-label"> Số điện thoại </label>
							<input
								type="text"
								name="phone_number"
								id="phone_number"
								placeholder="Số điện thoại"
								bind:value={form.phone_number}
								on:input={(e) => handleInputChange('phone_number', index, e.target.value)}
								class="formbold-form-input {errorMessages[index].phone_number ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages[index].phone_number}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages[index].phone_number}</span>
								</div>
							{/if}
						</div>
						<div>
							<label for="nationality" class="formbold-form-label"> Tên </label>
							<input
								type="text"
								name="nationality"
								id="nationality"
								placeholder="Ví dụ VIET NAM"
								bind:value={form.nationality}
								on:input={(e) => handleInputChange('nationality', index, e.target.value)}
								class="formbold-form-input {errorMessages[index].nationality ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages[index].nationality}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages[index].nationality}</span>
								</div>
							{/if}
						</div>
					</div>
				</div>
			</div>
		{/each}
		<div class="formbold-submit-wrapper">
			<input type="submit" name="submit" value="Đi Tiếp" class="formbold-btn" />
		</div>
	</form>
</div>
