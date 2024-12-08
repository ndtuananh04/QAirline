<script>
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';

	let errorMessages = {
		email: ''
	};

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

	async function submitInput(e) {
		const response = await fetch('http://localhost:5000/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				email: email,
				password: password
			})
		});
		if (!response.ok) {
			const errorData = await response.json();
			throw new Error(errorData.message || 'Login failed');
		} else {
			const data = await response.json();
			localStorage.setItem('jwt', data.access_token);
			alert('Đăng nhập thành công');
			goto('/user/dashboard/');
		}
	}
</script>

<div class="formbold-main-wrapper">
	<div class="formbold-form-container">
		<div class="formbold-form-wrapper">
			<form class="signup__form" on:submit={submitInput}>
				<div class="form-header">
					<img
						src="/images/logo.png"
						alt="QAirline Logo"
						class="logo"
						style="width: 120px; height: auto"
					/>
					<h2>Hãy bắt đầu ngay với tài khoản QAirline</h2>
				</div>
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

				<div class="formbold-checkbox-wrapper">
					<label for="supportCheckbox" class="formbold-checkbox-label">
					  <div class="formbold-relative">
						<input
						  type="checkbox"
						  id="supportCheckbox"
						  class="formbold-input-checkbox"
						/>
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
					  Remember Me
					</label>
				</div>

				<button class="formbold-btn">Đăng Nhập</button>
			</form>
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
