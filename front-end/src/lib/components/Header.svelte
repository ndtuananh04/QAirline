<script>
	import Icon from '@iconify/svelte';
</script>

<header class="header">
	<div class="container">
		<div class="header__logo">
			<a href="/">
				<img src="/images/logo.png" alt="QAirline Logo" height="42px" />
			</a>
		</div>

		<div class="header__icon">
			<i class="fas fa-bars"></i>
			<i class="fas fa-x d-none"></i>
		</div>

		<div class="header__pcpart">
			<nav class="header__links">
				<a href="/explore">Khám phá</a>
				<a href="/booking">Đặt vé</a>
				<a href="/info">Thông tin hành trình</a>
			</nav>

			<div class="header__auth">
				<a href="/user/login" class="login">Đăng nhập</a> |
				<a href="/user/signup" class="register">Đăng ký</a>
				<Icon icon="codicon:account" style="font-size: 22px; color: white;" />
			</div>
		</div>
	</div>
</header>
