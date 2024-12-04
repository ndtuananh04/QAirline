<script>
import { onMount } from 'svelte';
import { writable } from 'svelte/store';

let accounts = writable([]);

onMount(async () => {
		const response = await fetch('http://127.0.0.1:5000/addaccount');
		const data = await response.json();
		accounts.set(data)
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
      {#each accounts as account}
      <tr>
        <th scope="row">1</th>
        <td>{account.email}</td>
        <td>{account.password}</td>
        <td>{account.role}</td>
      </tr>
      {/each}
    </tbody>
  </table>