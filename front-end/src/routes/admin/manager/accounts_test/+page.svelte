<script>
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	let accounts = writable([]);
	let token = '';
	onMount(async () => {
		import('bootstrap/dist/js/bootstrap.bundle.min.js');
		try {
			token = localStorage.getItem('jwt');
			const response = await fetch('http://localhost:5000/addaccount', {
				method: 'GET', // Confirm with your backend if this is the correct method
				headers: {
					Authorization: `Bearer ${token}` // Fix template literal interpolation
				}
			});
			if (!response.ok) {
				throw new Error(`Failed to fetch accounts: ${response.statusText}`);
			}
			const data = await response.json();
			accounts.set(data);
			console.log(accounts.length);
		} catch (error) {
			console.error('Error fetching accounts:', error);
		}
	});
</script>
<table class="table">
	<thead>
		<tr>
			<th scope="col">#</th>
			<th scope="col">Email</th>
			<th scope="col">Password</th>
			<th scope="col">Role</th>
		</tr>
	</thead>
	<tbody>
		{#each $accounts as account}
			<tr>
				<th scope="row">{account.account_id}</th>
				<td>{account.email}</td>
				<td>{account.password}</td>
				<td>{account.role}</td>
			</tr>
		{/each}
	</tbody>
</table>