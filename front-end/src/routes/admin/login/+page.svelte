<script>
	import { goto } from '$app/navigation';
	let email = '';
	let password = '';
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
			goto('/admin/dashboard/1'); // Redirect to a secure page after login
		}
	}
</script>
<main class="login-form">
	<div class="cotainer">
		<div class="row justify-content-center">
			<div class="col-md-8">
				<div class="card">
					<div class="card-header">Đăng nhập hệ thống</div>
					<div class="card-body">
						<form on:submit={submitInput}>
							<div class="form-group row">
								<label for="email_address" class="col-md-4 col-form-label text-md-right"
									>E-Mail</label
								>
								<div class="col-md-6">
									<input
										type="text"
										id="email_address"
										class="form-control"
										name="email-address"
										bind:value={email}
										required
										autofocus
									/>
								</div>
							</div>
							<div class="form-group row">
								<label for="password" class="col-md-4 col-form-label text-md-right">Mật khẩu</label>
								<div class="col-md-6">
									<input
										type="password"
										id="password"
										class="form-control"
										name="password"
										bind:value={password}
										required
									/>
								</div>
							</div>
							<div class="form-group row">
								<div class="col-md-6 offset-md-4">
									<div class="checkbox">
										<label>
											<input type="checkbox" name="remember" /> Remember Me
										</label>
									</div>
								</div>
							</div>
							<div class="col-md-6 offset-md-4">
								<button type="submit" class="btn btn-primary"> Đăng nhập </button>
								<a href="#" class="btn btn-link"> Quên mật khẩu </a>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</div>
</main>