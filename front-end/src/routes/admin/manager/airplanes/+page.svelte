<script>
	import { onMount } from 'svelte';

	let airplanes = [];
	let error = '';

	const fetchAirplanes = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/airplanes', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (response.ok) {
				const data = await response.json();
				airplanes = data;
				console.log(airplanes);
			} else {
				const err = await response.json();
				error = err.msg || 'Lỗi khi lấy danh sách máy bay';
			}
		} catch (err) {
			console.error('Lỗi khi lấy danh sách máy bay:', error);
			error = 'Đã xảy ra lỗi khi lấy danh sách máy bay.';
		}
	};

	onMount(() => {
		fetchAirplanes();
	});

	let showModalAdd = false;
	let newAirplane = { name_airplane: '', capacity: '' };
	let addError = '';

	const openModalAdd = () => {
		showModalAdd = true;
		newAirplane = { name_airplane: '', capacity: '' };
		addError = '';
	};

	const closeModalAdd = () => {
		showModalAdd = false;
		newAirplane = { name_airplane: '', capacity: '' };
		addError = '';
	};

	const addAirplane = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/airplanes', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify(newAirplane)
			});

			const result = await response.json();

			if (response.ok) {
				alert(result.msg);
				fetchAirplanes();
				closeModalAdd();
			} else {
				const err = await response.json();
				addError = result.msg || 'Không thể thêm máy bay';
			}
		} catch (err) {
			console.error('Lỗi khi thêm máy bay:', error);
			addError = 'Đã xảy ra lỗi khi thêm máy bay.';
		}
	};

	let showModalDelete = false;
	let select_airplane_id = '';

	const openModalDelete = (airplane_id) => {
		select_airplane_id = airplane_id;
		showModalDelete = true;
	};

	const closeModalDelete = () => {
		showModalDelete = false;
		select_airplane_id = '';
	};

	const deleteAirplane = async (airplane_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/airplanes/${airplane_id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchAirplanes();
				closeModalDelete();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi xóa máy bay:', error);
			alert('Đã xảy ra lỗi khi xóa máy bay.');
		}
	};

	let showModalUpdate = false;
	let upAirplane = { name_airplane: '', capacity: '' };
	let updateError = '';

	const openModalUpdate = (airplane_id) => {
		showModalUpdate = true;
		select_airplane_id = airplane_id;
		upAirplane = { name_airplane: '', capacity: '' };
		updateError = '';
	};

	const closeModalUpdate = () => {
		showModalUpdate = false;
		upAirplane = { name_airplane: '', capacity: '' };
		updateError = '';
		select_airplane_id = '';
	};

	const updateAirplane = async (airplane_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/airplanes/${airplane_id}`, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(upAirplane)
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchAirplanes();
				closeModalUpdate();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi cập nhật máy bay:', error);
			updateError = 'Đã xảy ra lỗi khi cập nhật máy bay.';
		}
	};

	function sortById() {
		airplanes = [...airplanes].sort((a, b) => a.airplane_id - b.airplane_id);
	}

	function sortByAirplaneName() {
		airplanes = [...airplanes].sort((a, b) => {
			if (a.name_airplane < b.name_airplane) {
				return -1;
			} else if (a.name_airplane > b.name_airplane) {
				return 1;
			}
			return 0;
		});
	}
</script>

<div class="header-container">
	<div class="info-box">
		<p>Tổng số máy bay: <strong>{airplanes.length}</strong></p>
	</div>
	<div class="add-account-container">
		<button class="btn-add-admin" on:click={openModalAdd}>Thêm máy bay</button>
	</div>
</div>
{#if showModalAdd}
	<div class="modal">
		<div class="modal-content animate">
			<h3>Thêm máy bay</h3>
			{#if addError}
				<p class="error-text">{addError}</p>
			{/if}
			<div class="input-wrapper">
				<label for="name_airplane">Tên máy bay:</label>
				<input
					type="text"
					id="name_airplane"
					bind:value={newAirplane.name_airplane}
					placeholder="Nhập tên máy bay"
					required
				/>
			</div>
			<div class="input-wrapper">
				<label for="capacity">Số lượng ghế:</label>
				<input
					type="number"
					id="capacity"
					bind:value={newAirplane.capacity}
					placeholder="Nhập số lượng"
					required
				/>
			</div>
			<div class="button-group">
				<button class="submit-btn" on:click={addAirplane}>Thêm</button>
				<button class="cancel-btn" on:click={closeModalAdd}>Hủy</button>
			</div>
		</div>
	</div>
{/if}

<table class="table-airplane">
	<thead>
		<tr>
			<th scope="col" class="sortable-header" on:click={sortById}>ID</th>
			<th scope="col" class="sortable-header" on:click={sortByAirplaneName}>Tên máy bay</th>
			<th scope="col" class="sortable-header">Số lượng ghế</th>
			<th scope="col" class="sortable-header">Trạng thái</th>
			<th class="action-header">Hành động</th>
		</tr>
	</thead>
	<tbody>
		{#each airplanes as airplane}
			<tr>
				<td>{airplane.airplane_id}</td>
				<td>{airplane.name_airplane}</td>
				<td>{airplane.capacity}</td>
				<td>
					{#if airplane.is_locked === 1}
						Đang khóa
					{:else}
						Đang mở
					{/if}
				</td>
				<td class="action-cell">
					<button class="edit" on:click={() => openModalUpdate(airplane.airplane_id)}>Sửa</button>
					<button
						class="delete {airplane.is_locked === 1 ? 'open' : 'locked'}"
						on:click={() => openModalDelete(airplane.airplane_id)}
					>
						{#if airplane.is_locked === 1}
							Mở
						{:else}
							Khóa
						{/if}
					</button>
				</td>
			</tr>
		{/each}

		{#if showModalDelete}
			<div class="modal">
				<div class="modal-content delete-modal animate">
					<h3 class="warning-text">Bạn có chắc chắn muốn khóa máy bay?</h3>
					<div class="button-group">
						<button on:click={() => deleteAirplane(select_airplane_id)} class="delete-btn"
							>Đồng ý</button
						>
						<button on:click={closeModalDelete} class="cancel-btn">Không</button>
					</div>
				</div>
			</div>
		{/if}

		{#if showModalUpdate}
			<div class="modal">
				<div class="modal-content animate">
					<h3>Cập nhật thông tin máy bay</h3>
					{#if updateError}
						<p class="error-text">{updateError}</p>
					{/if}
					<div class="input-wrapper">
						<label for="name_airplane">Tên máy bay:</label>
						<input
							type="text"
							id="name_airplane"
							bind:value={upAirplane.name_airplane}
							placeholder="Nhập tên máy bay"
							required
						/>
					</div>
					<div class="input-wrapper">
						<label for="capacity">Số lượng ghế:</label>
						<input
							type="number"
							id="capacity"
							bind:value={upAirplane.capacity}
							placeholder="Nhập số lượng"
							required
						/>
					</div>
					<div class="button-group">
						<button on:click={() => updateAirplane(select_airplane_id)} class="submit-btn"
							>Cập nhật</button
						>
						<button on:click={closeModalUpdate} class="cancel-btn">Hủy</button>
					</div>
				</div>
			</div>
		{/if}
	</tbody>
</table>

<style>
	.modal {
		display: flex;
		justify-content: center;
		align-items: center;
		opacity: 1;
		visibility: visible;
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
