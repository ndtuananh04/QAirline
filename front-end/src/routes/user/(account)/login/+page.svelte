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

<div class="signup">
	<div class="container">
		<div class="signup__content">
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
				<fieldset class="contact-info">
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
						required
					/>
					{#if errorMessages.email}
						<div class="error-message">
							<span class="error-icon">⚠️</span>
							<span>{errorMessages.email}</span>
						</div>
					{/if}
				</div>

				<div class="form-group">
					<label for="password">Mật khẩu</label>
					<input
						type="password"
						id="password"
						bind:value={password}
						name="password"
						placeholder="Mật khẩu"
						required
					/>
				</div>
			</fieldset>

				<div class="form-group checkbox-group">
					<input type="checkbox" id="terms" name="terms" />
					<label for="terms">Remember Me.</label>
				</div>

				<button type="submit" class="submit-btn">Đăng nhập</button>
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
