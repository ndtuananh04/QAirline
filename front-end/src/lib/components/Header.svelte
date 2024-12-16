<script>
	import Icon from '@iconify/svelte';
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { goto } from '$app/navigation';
	
	let isLoggedIn = writable(false);
	let family_name = writable('');
	let given_name = writable('');
	let showDropdown = writable(false);

	onMount(async () => {
		const token = localStorage.getItem('jwt');
		if (token) {
			try {
				const response = await fetch('http://localhost:5000/verify-token', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${token}`
					}
				});
				if (response.ok) {
					const data = await response.json();
					isLoggedIn.set(true);
					family_name.set(data.family_name);
					given_name.set(data.given_name);
					console.log('Logged in as:', data.family_name, data.given_name);
				} else {
					isLoggedIn.set(false);
					localStorage.removeItem('jwt'); // Remove invalid token
				}
			} catch (error) {
				console.error('Error verifying token:', error);
				isLoggedIn.set(false);
				localStorage.removeItem('jwt'); // Remove invalid token
			}
		}
	});

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
					isLoggedIn.set(false);
					family_name.set('');
					given_name.set('');
					alert('Logged out successfully');
					goto('/');
				} else {
					alert('Failed to log out');
				}
			} catch (error) {
				console.error('Error logging out:', error);
				alert('Failed to log out');
			}
		}
	};

	const toggleDropdown = () => {
		showDropdown.update((value) => !value);
	};
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
							<button on:click={logout} class="logout-btn">Đăng xuất</button>
						</div>
					{/if}
				{:else}
					<a href="/user/login" class="login">Đăng nhập</a> |
					<a href="/user/signup" class="register">Đăng ký</a>
				{/if}
			</div>
		</div>
	</div>
</header>
