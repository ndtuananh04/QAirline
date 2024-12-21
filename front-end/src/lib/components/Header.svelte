<script>
	import Icon from '@iconify/svelte';
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { goto } from '$app/navigation';
	import { fade } from 'svelte/transition';

	let showDropdown = writable(false);
	let family_name = writable('');
	let given_name = writable('');
	let isLoggedIn = writable(false);
	let showMobileMenu = writable(false);

	onMount(() => {
		const token = localStorage.getItem('jwt');
		if (token) {
			family_name.set(localStorage.getItem('family_name'));
			given_name.set(localStorage.getItem('given_name'));
			isLoggedIn.set(true);
			console.log('Logged in as:', $family_name, $given_name);
		}
	});

	// onMount(async() => {
	// 	const token = localStorage.getItem('jwt');
	// 	if (token) {
	// 		try {
	// 			const response = await fetch('http://localhost:5000/verify-token', {
	// 				method: 'POST',
	// 				headers: {
	// 					'Content-Type': 'application/json',
	// 					Authorization: `Bearer ${token}`
	// 				}
	// 			});

	// 			if (response.ok) {
	// 				const data = await response.json();
	// 				isLoggedIn.set(true);
	// 				family_name.set(data.family_name);
	// 				given_name.set(data.given_name);
	// 				console.log('Logged in as:', data.family_name, data.given_name);
	// 			} else {
	// 				isLoggedIn.set(false);
	// 				localStorage.removeItem('jwt'); // Remove invalid token
	// 			}
	// 		} catch (error) {
	// 			console.error('Error verifying token:', error);
	// 			isLoggedIn.set(false);
	// 			localStorage.removeItem('jwt'); // Remove invalid token
	// 		}
	// 	}
	// });
	const logout = async () => {
		const token = localStorage.getItem('jwt');
		if (token) {
			try {
				const response = await fetch('http://localhost:5000/logout', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${token}`
					}
				});
				if (response.ok) {
					localStorage.removeItem('jwt');
					localStorage.removeItem('family_name');
					localStorage.removeItem('given_name');
					isLoggedIn.set(false);
					family_name.set('');
					given_name.set('');
					alert('Bạn đã đăng xuất');
					goto('/');
				} else {
					alert('Đăng xuất thất bại');
				}
			} catch (error) {
				console.error('Lỗi khi đăng xuất:', error);
				alert('Đăng xuất thất bại');
			}
		}
	};

	const toggleDropdown = () => {
		showDropdown.update((value) => !value);
	};

	const toggleMobileMenu = () => {
		showMobileMenu.update((value) => !value);
		if ($showMobileMenu) {
			document.body.classList.add('no-scroll');
		} else {
			document.body.classList.remove('no-scroll');
		}
	};

</script>

<header class="header">
	<div class="container">
		<div class="header__logo">
			<a href="/">
				<img src="/images/logo.png" alt="QAirline Logo" height="42px" />
			</a>
		</div>

		<div class="header__pcpart">
			<nav class="header__links">
				<a href="/user/dashboard#news-section">Khám phá</a>
				<a href="/user/checkin">Làm thủ tục</a>
				<a href="/user/ticket">Thông tin vé</a>
			</nav>

			<div class="header__auth">
				{#if $isLoggedIn}
					<div class="header__account" on:click={toggleDropdown}>
						<span>{$family_name} {$given_name}</span>
						<Icon icon="codicon:account" style="font-size: 22px; color: white;" />
					</div>
					{#if $showDropdown}
						<div class="header__dropdown">
							<a href="/user/user-info" class="info-btn">Thông tin cá nhân</a>
							<a  class="logoutt-btn" on:click={logout}>Đăng xuất</a>
						</div>
					{/if}
				{:else}
					<a href="/user/login" class="login">Đăng nhập</a> |
					<a href="/user/signup" class="register">Đăng ký</a>
				{/if}
			</div>
		</div>

		<div class="header__icon" on:click={toggleMobileMenu}>
			{#if $showMobileMenu}
				<i class="fas fa-x"></i>
			{:else}
				<i class="fas fa-bars"></i>
			{/if}
		</div>

		{#if $showMobileMenu}
			<div class="overlay" transition:fade on:click={toggleMobileMenu}></div>
			<div class="header__mobile-menu" transition:fade>
				<nav class="header__mobile-links">
					<a href="/user/dashboard#news-section" on:click={toggleMobileMenu}>Khám phá</a>
					<a href="/user/checkin" on:click={toggleMobileMenu}>Làm thủ tục</a>
					<a href="/user/ticket" on:click={toggleMobileMenu}>Thông tin vé</a>
				</nav>

				<div class="header__mobile-links">
					{#if $isLoggedIn}
						<div class="header__mobile-auth">
							<div class="header__mobile-account">
								<span class="header__mobile-username" on:click={toggleDropdown}>{$family_name} {$given_name}</span>
								<Icon icon="codicon:account" style="font-size: 22px; color: $light-purple;" />
							</div>
							<button class="info-btn" on:click={goto('/user/user-info'), toggleMobileMenu}>Thông tin cá nhân</button>
							<button on:click={logout} class="logoutt-btn">Đăng xuất</button>
						</div>
					{:else}
						<div class="header__mobile-auth">
							<button on:click={() => goto('/user/login')} class="login">Đăng nhập</button>
							<button on:click={() => goto('/user/signup')} class="register">Đăng ký</button>
						</div>
					{/if}
				</div>
			</div>
		{/if}
	</div>
</header>
