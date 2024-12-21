<script>
	import Icon from '@iconify/svelte';
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { goto } from '$app/navigation';
	
	let isLoggedIn = writable(false);
	let showDropdown = writable(false);
	let email = writable('');

	onMount(async () => {
		const token = localStorage.getItem('jwt');
		if (token) {
			try {
				const response = await fetch('http://localhost:5000/verify-token-admin', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${token}`
					}
				});
				if (response.ok) {
					const data = await response.json();
					isLoggedIn.set(true);
					email.set(data.email);
				} else {
					isLoggedIn.set(false);
					localStorage.removeItem('jwt'); // Remove invalid token
					const errorData = await response.json();
					alert(errorData.msg);
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
					email.set('');
					alert('Đăng xuất thành công.');
					goto('/admin/login');
				} else {
					alert('Đăng xuất thất bại.');
				}
			} catch (error) {
				console.error('Đăng xuất thất bại:', error);
				alert('Đăng xuất thất bại.');
			}
		}
	};

	const toggleDropdown = () => {
		showDropdown.update((value) => !value);
	};
</script>

<header class="header-admin">
	<div class="container-admin">
		<div class="header-admin__logo">
			<a href="/">
				<img src="/images/logo.png" alt="QAirline Logo" height="42px" />
			</a>
		</div>

		<div class="header-admin__icon">
			<i class="fas fa-bars"></i>
			<i class="fas fa-x d-none"></i>
		</div>

		<div class="header-admin__pcpart">
			<div class="header-admin__auth">
				{#if $isLoggedIn}
					<div class="header-admin__account" on:click={toggleDropdown}>
						<span>{$email}</span>
						<Icon icon="codicon:account" style="font-size: 22px; color: white;" />
					</div>
					{#if $showDropdown}
						<div class="header-admin__dropdown">
							<button on:click={logout} class="logout-btn">Đăng xuất</button>
						</div>
					{/if}
				{/if}
			</div>
		</div>
	</div>
</header>
