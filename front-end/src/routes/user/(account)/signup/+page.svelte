<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { writable, get } from 'svelte/store';
	import '@splidejs/splide/dist/css/splide.min.css';
	import Splide from '@splidejs/splide';

	let familyName = '';
	let givenName = '';
	let nationality = '';
	let gender = '';
	let dateOfBirth = '';
	let identification = '';
	let phoneNumber = '';
	let email = '';
	let password = '';
	let errorMessages = {
		familyName: '',
		givenName: '',
		email: '',
		nationality: '',
		phoneNumber: '',
		identification: ''
	};

	onMount(() => {
		splideInstance = new Splide(splideElement, {
			type: 'loop',
			autoplay: true,
			interval: 5000,
			arrows: false,
			pagination: true
		}).mount();

		document.addEventListener('click', handleClickOutside);
	});

	onMount(async () => {
		const response = await fetch('http://127.0.0.1:5000/register');
		const data = await response.json();
		email.set(data.email);
		password.set(data.password);
		identification.set(data.identification);
		familyName.set(data.familyName);
		givenName.set(data.givenName);
		gender.set(data.gender);
		nationality.set(data.nationality);
		dateOfBirth.set(data.dateOfBirth);
		phoneNumber.set(data.phoneNumber);
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
			errorMessages[field] = `${field === 'familyName' ? 'Họ' : field === 'givenName' ? 'Tên đệm & Tên' : 'Quốc tịch'} không được nhập ký tự đặc biệt hoặc số.`;
		} else {
			value = value.toUpperCase();
			errorMessages[field] = '';
			if (field === 'familyName') {
				familyName = value;
			} else if (field === 'givenName') {
				givenName = value;
			} else if (field === 'nationality') {
				nationality = value;
			}
		}
	};

	// Check định dạng số
	const handleInput = (field, e) => {
		const value = e.target.value;
		if (!/^\d*$/.test(value)) {
			errorMessages[field] = `${field === 'phoneNumber' ? 'Số điện thoại' : 'CMND/CCCD'} chỉ được nhập số.`;
		} else {
			errorMessages[field] = '';
			if (field === 'phoneNumber') {
				phoneNumber = value;
			} else {
				identification = value;
			}
		}
	};
</script>

<div class="signup">
	<div class="container">
	  <div class="signup__content">
		<div class="signup__form">
		  <div class="form-header">
			<img src="/images/logo.png" alt="QAirline Logo" class="logo" style="width: 120px; height: auto" />
			<h2>Bạn đã sẵn sàng đăng ký tài khoản tại QAirline? Hãy bắt đầu ngay!</h2>
			<p>Vui lòng điền đầy đủ thông tin cá nhân giống trên CMND/CCCD của bạn.</p>
		  </div>
		  <fieldset class="personal-info">
			<legend>Thông tin cá nhân</legend>
			<div class="signup__group">
				<div class="form-group">
					<label for="family_name">Họ</label>
					<input
						type="text"
						id="family_name"
						name="family_name"
						placeholder="Ví dụ: NGUYEN"
						bind:value={familyName}
						on:input={(e) => handleTextInput('familyName', e)}
						class={errorMessages.familyName ? 'input-error' : ''}
					/>
					{#if errorMessages.familyName}
					  	<div class="error-message">
							<span class="error-icon">⚠️</span>
							<span>{errorMessages.familyName}</span>
					  	</div>
					{/if}
					</div>
					<div class="form-group">
						<label for="given-name">Tên đệm & Tên</label>
						<input
							type="text"
							id="given-name"
							name="given-name"
							placeholder="Ví dụ: VAN A"
							bind:value={givenName}
							on:input={(e) => handleTextInput('givenName', e)}
							class={errorMessages.givenName ? 'input-error' : ''}
						/>
					{#if errorMessages.givenName}
						<div class="error-message">
							<span class="error-icon">⚠️</span>
							<span>{errorMessages.givenName}</span>
						</div>
					{/if}
				</div>
			</div>
  
			<div class="signup__group">
			  <div class="form-group">
				<label for="date_of_birth">Ngày, Tháng, Năm Sinh</label>
				<input type="date" id="date_of_birth" name="date_of_birth" />
			  </div>
  
			  <div class="form-group">
				<label for="gender">Giới tính</label>
				<select id="gender" name="gender">
				  <option value="" disabled selected hidden>Giới tính</option>
				  <option value="male">Nam</option>
				  <option value="female">Nữ</option>
				  <option value="other">Khác</option>
				</select>
			  </div>
			</div>
  
			<div class="form-group">
				<label for="nationality">Quốc tịch</label>
				<input
					type="text"
					id="nationality"
					name="nationality"
					placeholder="Quốc tịch"
					bind:value={nationality}
					on:input={(e) => handleTextInput('nationality', e)}
					class={errorMessages.nationality ? 'input-error' : ''}
				/>
				{#if errorMessages.nationality}
				  	<div class="error-message">
						<span class="error-icon">⚠️</span>
						<span>{errorMessages.nationality}</span>
				  	</div>
				{/if}
			</div>

			<div class="form-group">
				<label for="identification">CMND/CCCD</label>
				<input
					type="text"
					id="identification"
					bind:value={identification}
					on:input={(e) => handleInput('identification', e)}
					placeholder="CMND/CCCD"
					class={errorMessages.identification ? 'input-error' : ''}
				/>
				{#if errorMessages.identification}
					<div class="error-message">
						<span class="error-icon">⚠️</span>
						<span>{errorMessages.identification}</span>
					</div>
				{/if}
			</div>
		  </fieldset>
  
		  <fieldset class="contact-info">
			<legend>Thông tin liên hệ</legend>
			<div class="form-group">
				<label for="email">Email</label>
				<input
					type="email"
					id="email"
					name="email"
					placeholder="Email của bạn"
					bind:value={email}
					on:input={handleEmailInput}
					class={errorMessages.email ? 'input-error' : ''}
				/>
				{#if errorMessages.email}
				  	<div class="error-message">
						<span class="error-icon">⚠️</span>
						<span>{errorMessages.email}</span>
				  	</div>
				{/if}
			</div>

			<div class="form-group">
				<label for="phone_number">Số điện thoại</label>
				<input
					type="text"
					id="phone_number"
					bind:value={phoneNumber}
					on:input={(e) => handleInput('phoneNumber', e)}
					placeholder="Số điện thoại"
					class={errorMessages.phoneNumber ? 'input-error' : ''}
				/>
				{#if errorMessages.phoneNumber}
					<div class="error-message">
						<span class="error-icon">⚠️</span>
						<span>{errorMessages.phoneNumber}</span>
					</div>
				{/if}
			</div>
  
			<div class="form-group">
			  <label for="password">Mật khẩu</label>
			  <input type="text" id="password" name="password" placeholder="Mật khẩu" />
			</div>
		  </fieldset>
  
		  <div class="form-group checkbox-group">
			<input type="checkbox" id="terms" name="terms" />
			<label for="terms">Tôi đã đọc và đồng ý với các điều khoản và điều kiện của QAirline.</label>
		  </div>
  
		  <button type="submit" class="submit-btn">Đăng ký</button>
		</div>
		<div class="signup__image"></div>
	  </div>
	</div>
  </div>

  <style>
	.form-group {
	  margin-bottom: 20px;
	}
  
	input {
	  width: 100%;
	  padding: 10px;
	  font-size: 1rem;
	  border: 1px solid #ccc;
	  border-radius: 4px;
	  transition: border-color 0.3s ease;
	}
  
	input:focus {
	  border-color: #007bff;
	  outline: none;
	}
  
	input.input-error {
	  border-color: #dc3545;
	}
  
	.error-message {
	  display: flex;
	  align-items: center;
	  margin-top: 5px;
	  color: #dc3545;
	  font-size: 0.9rem;
	  background-color: #ffe4e6;
	  padding: 8px 12px;
	  border-radius: 4px;
	  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}
  
	.error-icon {
	  margin-right: 8px;
	  font-size: 1.2rem;
	}
  </style>
  