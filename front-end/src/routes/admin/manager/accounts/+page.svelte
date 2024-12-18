<script>
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { goto } from '$app/navigation';

	let accounts = [];
	let showModal = false;
	let select_account_id = '';
	let error = '';
	let adminCount = 0;
	let customerCount = 0;

	const fetchAccounts = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/addaccount', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (response.ok) {
				const data = await response.json();
				accounts = data;
			} else {
				const err = await response.json();
				error = err.msg || 'Failed to fetch accounts';
			}
		} catch (err) {
			console.error('Error fetching tickets:', error);
			error = 'An error occurred while fetching tickets.';
		}
	};

	const fetchQuantities = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/quantity-role', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (response.ok) {
				const data = await response.json();
				adminCount = data.admin;
				customerCount = data.customer;
			} else {
				console.error('Failed to fetch account quantities');
			}
		} catch (err) {
			console.error('Error fetching account quantities:', err);
		}
	};

	onMount(() => {
		const token = localStorage.getItem('jwt');
		if (!token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập!');
			goto('/user/login'); // Điều hướng tới trang đăng nhập
		}
		fetchAccounts();
		fetchQuantities();
	});

	const openModal = (account_id) => {
		select_account_id = account_id;
		showModal = true;
	};

	const closeModal = () => {
		showModal = false;
		select_account_id = '';
	};

	const deleteAccount = async (account_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/deleteaccount/${account_id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchAccounts();
				fetchQuantities();
				closeModal();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi xóa tài khoản:', error);
			alert('Đã có lỗi xảy ra khi xóa tài khoản.');
		}
	};

	let showModalUpdate = false;
	let select_role = '';
	const openModalUpdateRole = (account_id, current_role) => {
		select_account_id = account_id;
		select_role = current_role;
		showModalUpdate = true;
	};

	const closeModalUpdateRole = () => {
		showModalUpdate = false;
		select_account_id = '';
		select_role = '';
	};

	const updateRole = async (account_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/deleteaccount/${account_id}`, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ role: select_role })
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchAccounts();
				fetchQuantities();
				closeModalUpdateRole();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi cập nhật tài khoản:', error);
			alert('Đã có lỗi xảy ra.');
		}
	};

	let showModalAdd = false;
	let newAdmin = { email: '', password: '' };
	let addError = '';

	const openModalAdd = () => {
		showModalAdd = true;
		newAdmin = { email: '', password: '' };
		addError = '';
	};

	const closeModalAdd = () => {
		showModalAdd = false;
		newAdmin = { email: '', password: '' };
		addError = '';
	};

	const addAdminAccount = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/addaccount', {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(newAdmin)
			});

			const result = await response.json();

			if (response.ok) {
				alert(result.msg);
				fetchAccounts();
				fetchQuantities();
				closeModalAdd();
			} else {
				addError = result.msg || 'Không thể tạo tài khoản admin';
			}
		} catch (error) {
			console.error('Lỗi khi thêm tài khoản admin:', error);
			addError = 'Đã có lỗi xảy ra khi thêm tài khoản.';
		}
	};

	function sortById() {
		accounts = [...accounts].sort((a, b) => a.account_id - b.account_id);
	}

	function sortByAccountName() {
		accounts = [...accounts].sort((a, b) => {
			if (a.email < b.email) {
				return -1;
			} else if (a.email > b.email) {
				return 1;
			}
			return 0;
		});
	}

	function sortByRole() {
		accounts = [...accounts].sort((a, b) => {
			if (a.role < b.role) {
				return -1;
			} else if (a.role > b.role) {
				return 1;
			}
			return 0;
		});
	}
</script>

<div class="header-container">
	<div class="info-box">
		<p>Tổng số tài khoản Admin: <strong>{adminCount}</strong></p>
	</div>
	<div class="info-box">
		<p>Tổng số tài khoản Customer: <strong>{customerCount}</strong></p>
	</div>
	<div class="add-account-container">
		<button class="btn-add-admin" on:click={openModalAdd}>Thêm tài khoản Admin</button>
	</div>
</div>
{#if showModalAdd}
	<div class="modal">
		<div class="modal-content animate">
			<h3>Thêm tài khoản Admin</h3>
			{#if addError}
				<p class="error-text">{addError}</p>
			{/if}
			<div class="input-wrapper">
				<label for="email">Email:</label>
				<input type="email" id="email" bind:value={newAdmin.email} placeholder="Nhập email" />
			</div>
			<div class="input-wrapper">
				<label for="password">Mật khẩu:</label>
				<input
					type="password"
					id="password"
					bind:value={newAdmin.password}
					placeholder="Nhập mật khẩu"
				/>
			</div>
			<div class="button-group">
				<button class="submit-btn" on:click={addAdminAccount}>Thêm</button>
				<button class="cancel-btn" on:click={closeModalAdd}>Hủy</button>
			</div>
		</div>
	</div>
{/if}

<table class="table-account">
	<thead>
		<tr>
			<th scope="col" class="sortable-header" on:click={sortById}>ID</th>
			<th scope="col" class="sortable-header" on:click={sortByAccountName}>Email</th>
			<th scope="col" class="sortable-header" on:click={sortByRole}>Role</th>
			<th class="action-header">Hành động</th>
		</tr>
	</thead>
	<tbody>
		{#each accounts as account}
			<tr>
				<td>{account.account_id}</td>
				<td>{account.email}</td>
				<td>{account.role}</td>
				<td class="action-cell">
					<button
						class="edit"
						on:click={() => openModalUpdateRole(account.account_id, account.role)}>Sửa</button
					>
					<button class="delete" on:click={() => openModal(account.account_id)}>Xóa</button>
				</td>
			</tr>
		{/each}

		{#if showModal}
			<div class="modal">
				<div class="modal-content delete-modal animate">
					<h3 class="warning-text">Bạn có chắc chắn muốn xóa tài khoản?</h3>
					<div class="button-group">
						<button on:click={() => deleteAccount(select_account_id)} class="delete-btn"
							>Đồng ý</button
						>
						<button on:click={closeModal} class="cancel-btn">Không</button>
					</div>
				</div>
			</div>
		{/if}

		{#if showModalUpdate}
			<div class="modal">
				<div class="modal-content animate">
					<h3>Chỉnh sửa vai trò tài khoản</h3>
					<div class="select-wrapper">
						<select bind:value={select_role} class="custom-select">
							<option value="admin">Admin</option>
							<option value="customer">Customer</option>
						</select>
					</div>
					<div class="button-group">
						<button on:click={() => updateRole(select_account_id)} class="submit-btn"
							>Cập nhật</button
						>
						<button on:click={closeModalUpdateRole} class="cancel-btn">Hủy</button>
					</div>
				</div>
			</div>
		{/if}
	</tbody>
</table>