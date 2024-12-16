<script>
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
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

<style>
	.modal {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.6);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}

	.modal-content {
		background-color: #ffffff;
		padding: 2rem;
		border-radius: 12px;
		box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
		text-align: center;
		max-width: 400px;
		width: 90%;
		transform: scale(0.9);
		opacity: 0;
		transition: all 0.3s ease-out;
	}

	.modal-content.animate {
		transform: scale(1);
		opacity: 1;
	}

	.select-wrapper {
		margin: 5px 0;
	}

	.custom-select {
		appearance: none;
		background-color: #f9f9f9;
		border: 1px solid #ccc;
		border-radius: 5px;
		padding: 5px 10px;
		font-size: 16px;
		color: #333;
		width: 100%;
		cursor: pointer;
		outline: none;
		transition: border-color 0.3s ease;
	}

	.custom-select:hover {
		border-color: #888;
	}

	.custom-select:focus {
		border-color: #007bff;
		box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
	}

	.button-group {
		display: flex;
		justify-content: space-between;
		margin-top: 20px;
	}

	.delete-btn,
	.submit-btn,
	.cancel-btn {
		padding: 10px 20px;
		font-size: 14px;
		border-radius: 5px;
		border: none;
		cursor: pointer;
		transition: background-color 0.3s;
		width: 48%;
	}

	.submit-btn {
		background-color: #007bff;
		color: #ffffff;
	}

	.submit-btn:hover {
		background-color: #0056b3;
	}

	.cancel-btn {
		background-color: #e0e0e0;
		color: #333333;
	}

	.cancel-btn:hover {
		background-color: #c6c6c6;
	}

	.delete-btn {
		background-color: #ff4d4f;
		color: #ffffff;
	}

	.delete-btn:hover {
		background-color: #d9363e;
		transform: translateY(-2px);
	}

	.submit-btn:hover,
	.cancel-btn:hover {
		transform: translateY(-2px);
	}

	.input-wrapper {
		margin: 10px 0;
		text-align: left;
	}

	.input-wrapper label {
		display: block;
		margin-bottom: 5px;
		font-size: 14px;
		color: #333;
	}

	.input-wrapper input {
		width: 100%;
		padding: 8px;
		border: 1px solid #ccc;
		border-radius: 5px;
		font-size: 16px;
		box-sizing: border-box;
	}

	.error-text {
		color: #ff4d4f;
		font-size: 14px;
		margin-bottom: 10px;
		text-align: center;
	}

	@media (max-width: 480px) {
		.modal-content {
			padding: 1.5rem;
		}

		.delete-btn,
		.submit-btn,
		.cancel-btn {
			font-size: 12px;
			padding: 8px 15px;
		}
	}

	.header-container {
		display: flex;
		align-items: center;
		gap: 1rem;
		text-align: right;
		margin-top: 20px;
		margin-right: 20px;
		margin-left: 220px;
	}

	.info-box {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
		background-color: #f9f9f9;
		border: 1px solid #ccc;
		border-radius: 8px;
		padding: 10px 20px;
		box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
		width: auto;
	}

	.info-box p {
		margin: 0;
		font-size: 1rem;
		color: #333;
	}

	.info-box strong {
		color: #007bff;
	}

	.btn-add-admin {
		background-color: #007bff;
		color: #fff;
		border: none;
		padding: 10px 20px;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.btn-add-admin:hover {
		background-color: #0056b3;
	}

	.sortable-header {
		cursor: pointer;
		color: black; /* Màu mặc định */
		transition: color 0.3s ease;
	}

	.sortable-header:hover {
		color: rgb(0, 255, 255); /* Màu khi di chuột */
	}
</style>
