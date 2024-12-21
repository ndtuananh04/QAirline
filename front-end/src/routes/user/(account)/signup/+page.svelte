<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { writable, get } from 'svelte/store';
	import '@splidejs/splide/dist/css/splide.min.css';
	import Splide from '@splidejs/splide';
	import flatpickr from 'flatpickr';
	import 'flatpickr/dist/flatpickr.min.css';

	let family_name = '';
	let given_name = '';
	let nationality = '';
	let gender = '';
	let date_of_birth = '';
	let identification = '';
	let phone_number = '';
	let email = '';
	let password = '';

	let errorMessages = {
		family_name: '',
		given_name: '',
		email: '',
		nationality: '',
		phone_number: '',
		identification: ''
	};
	
	let dateOfBirthPicker;

	onMount(() => {
		if (dateOfBirthPicker) {
			flatpickr(dateOfBirthPicker, {
				dateFormat: 'd/m/Y',
				altFormat: 'Y-m-d',
				maxDate: new Date().setFullYear(new Date().getFullYear()),
				onChange: function (selectedDates) {
					if (selectedDates[0]) {
						const date = selectedDates[0];
						date_of_birth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
					}
				}
			});
		}
	});

	// Check định dạng email
	const handleEmailInput = (e) => {
		const value = e.target.value;
		if (value && !/^[a-zA-Z0-9._%+-]+@gmail\.com$/.test(value)) {
			errorMessages.email = 'Email phải có định dạng @gmail.com';
		} else {
			// Xóa lỗi nếu giá trị hợp lệ
			errorMessages.email = '';
			email = value;
		}
	};

	// Check định dạng chữ
	const handleTextInput = (field, e) => {
		let value = e.target.value;
		if (/[^a-zA-Z\s]/.test(value)) {
			errorMessages[field] =
				`${field === 'family_name' ? 'Họ' : field === 'given_name' ? 'Tên đệm & Tên' : 'Quốc tịch'} không được nhập ký tự đặc biệt hoặc số.`;
		} else {
			value = value.toUpperCase();
			errorMessages[field] = '';
			if (field === 'family_name') {
				family_name = value;
			} else if (field === 'given_name') {
				given_name = value;
			} else if (field === 'nationality') {
				nationality = value;
			}
		}
	};

	// Check định dạng số
	const handleInput = (field, e) => {
		const value = e.target.value;
		if (!/^\d*$/.test(value)) {
			errorMessages[field] =
				`${field === 'phone_number' ? 'Số điện thoại' : 'CMND/CCCD'} chỉ được nhập số.`;
		} else {
			errorMessages[field] = '';
			if (field === 'phone_number') {
				phone_number = value;
			} else {
				identification = value;
			}
		}
	};

	const handleSubmit = async (e) => {
		e.preventDefault();

		const userData = {
			email: email,
			password: password,
			identification: String(identification),
			family_name: family_name,
			given_name: given_name,
			gender: gender,
			nationality: nationality,
			date_of_birth: date_of_birth,
			phone_number: phone_number
		};
		try {
			const response = await fetch('http://localhost:5000/register', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(userData)
			});

			const data = await response.json();

			if (!response.ok) {
				alert(data.msg);
			} else {
				alert(data.msg); // Hiển thị thông báo thành công
				goto('/user/login');
			}
		} catch (error) {
			console.error('Error:', error);
			alert('Đã xảy ra lỗi. Vui lòng thử lại sau.');
		}
	};
</script>

<div class="formbold-main-wrapper">
	<div class="formbold-form-container">
		<div class="formbold-form-wrapper">
			<form class="signup__form" on:submit={handleSubmit}>
				<div class="form-header">
					<img
						src="/images/logo.png"
						alt="QAirline Logo"
						class="logo"
						style="width: 120px; height: auto"
					/>
					<h2>Đăng Ký QAirline</h2>
					<p>Vui lòng điền đầy đủ thông tin!</p>
				</div>

				<hr class="separator" />

				<fieldset class="personal-info">
					<legend>Thông tin cá nhân</legend>
					<div class="formbold-input-flex">
						<div>
							<label for="family_name" class="formbold-form-label"> Họ </label>
							<input
								type="text"
								id="family_name"
								name="family_name"
								placeholder="Ví dụ: NGUYEN"
								bind:value={family_name}
								on:input={(e) => handleTextInput('family_name', e)}
								class="formbold-form-input {errorMessages.family_name ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages.family_name}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages.family_name}</span>
								</div>
							{/if}
						</div>
						<div>
							<label for="given-name" class="formbold-form-label"> Tên </label>
							<input
								type="text"
								id="given-name"
								name="given-name"
								placeholder="Ví dụ: VAN A"
								bind:value={given_name}
								on:input={(e) => handleTextInput('given_name', e)}
								class="formbold-form-input {errorMessages.given_name ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages.given_name}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages.given_name}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="formbold-input-flex">
						<div>
							<label for="date_of_birth" class="formbold-form-label"> Ngày, Tháng, Năm Sinh </label>
							<input
								type="text"
								id="date_of_birth"
								bind:this={dateOfBirthPicker}
								name="date_of_birth"
								class="formbold-form-input"
								placeholder="Chọn ngày sinh"
								required
							/>
						</div>
						<div>
							<label for="gender" class="formbold-form-label"> Giới Tính </label>
							<select id="gender" name="gender" bind:value={gender} class="formbold-form-input">
								<option value="" disabled selected hidden>Giới tính</option>
								<option value="male">Nam</option>
								<option value="female">Nữ</option>
								<option value="other">Khác</option>
							</select>
						</div>
					</div>

					<div class="formbold-input-flex">
						<div>
							<label for="nationality" class="formbold-form-label"> Quốc Tịch </label>
							<input
								type="text"
								id="nationality"
								name="nationality"
								placeholder="Quốc tịch"
								bind:value={nationality}
								on:input={(e) => handleTextInput('nationality', e)}
								class="formbold-form-input {errorMessages.nationality ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages.nationality}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages.nationality}</span>
								</div>
							{/if}
						</div>
						<div>
							<label for="identification" class="formbold-form-label"> CMND/CCCD </label>
							<input
								type="text"
								id="identification"
								bind:value={identification}
								on:input={(e) => handleInput('identification', e)}
								placeholder="CMND/CCCD"
								class="formbold-form-input {errorMessages.identification ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages.identification}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages.identification}</span>
								</div>
							{/if}
						</div>
					</div>
				</fieldset>

				<hr class="separator" />

				<fieldset class="contact-info">
					<legend>Thông tin liên hệ</legend>
					<div class="formbold-mb-3">
						<div>
							<label for="email" class="formbold-form-label"> Email </label>
							<input
								type="email"
								id="email"
								name="email"
								placeholder="Email của bạn"
								bind:value={email}
								on:input={handleEmailInput}
								class="formbold-form-input {errorMessages.email ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages.email}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages.email}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="formbold-mb-3">
						<div>
							<label for="phone_number" class="formbold-form-label"> Số điện thoại </label>
							<input
								type="text"
								id="phone_number"
								bind:value={phone_number}
								on:input={(e) => handleInput('phone_number', e)}
								placeholder="Số điện thoại"
								class="formbold-form-input {errorMessages.phone_number ? 'input-error' : ''}"
								required
							/>
							{#if errorMessages.phone_number}
								<div class="error-message">
									<span class="error-icon">⚠️</span>
									<span>{errorMessages.phone_number}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="formbold-mb-3">
						<label for="password" class="formbold-form-label"> Mật khẩu </label>
						<input
							type="password"
							id="password"
							bind:value={password}
							name="password"
							placeholder="Mật khẩu"
							class="formbold-form-input"
							required
						/>
					</div>
				</fieldset>

				<div class="formbold-checkbox-wrapper">
					<label for="supportCheckbox" class="formbold-checkbox-label">
						<div class="formbold-relative">
							<input type="checkbox" id="supportCheckbox" class="formbold-input-checkbox" />
							<div class="formbold-checkbox-inner">
								<span class="formbold-opacity-0">
									<svg
										width="11"
										height="8"
										viewBox="0 0 11 8"
										fill="none"
										class="formbold-stroke-current"
									>
										<path
											d="M10.0915 0.951972L10.0867 0.946075L10.0813 0.940568C9.90076 0.753564 9.61034 0.753146 9.42927 0.939309L4.16201 6.22962L1.58507 3.63469C1.40401 3.44841 1.11351 3.44879 0.932892 3.63584C0.755703 3.81933 0.755703 4.10875 0.932892 4.29224L0.932878 4.29225L0.934851 4.29424L3.58046 6.95832C3.73676 7.11955 3.94983 7.2 4.1473 7.2C4.36196 7.2 4.55963 7.11773 4.71406 6.9584L10.0468 1.60234C10.2436 1.4199 10.2421 1.1339 10.0915 0.951972ZM4.2327 6.30081L4.2317 6.2998C4.23206 6.30015 4.23237 6.30049 4.23269 6.30082L4.2327 6.30081Z"
											stroke-width="0.4"
										></path>
									</svg>
								</span>
							</div>
						</div>
						Tôi đồng ý với điều khoản của QAirline
					</label>
				</div>

				<button class="formbold-btn">Đăng Ký</button>
			</form>
		</div>
	</div>
</div>

<style>
	.formbold-main-wrapper {
		margin: 0;
	}
</style>
