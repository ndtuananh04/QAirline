<script>
	import Icon from '@iconify/svelte';
	import Footer from '$lib/components/Footer.svelte';
</script>

<header class="header">
	<div class="container">
		<div class="header__logo">
			<a href="/">
				<img src="/images/logo.png" alt="QAirline Logo" height="50px" />
			</a>
		</div>
		<div class="header__auth">
			<a href="/user/login" class="login">Đăng nhập</a> |
			<a href="/user/signup" class="register">Đăng ký</a>
			<Icon icon="codicon:account" style="font-size: 22px;" />
		</div>
	</div>
</header>
<div class="sign-background">
	<slot />
</div>
<Footer />

<style>
	.sign-background {
		background-image: url('/images/signup-background-1.png');
		background-size: cover;
		background-position: center;
		background-repeat: no-repeat;
	}
</style>
