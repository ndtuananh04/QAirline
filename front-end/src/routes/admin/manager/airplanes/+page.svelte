<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

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
		const token = localStorage.getItem('jwt');
		if (!token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập!');
			goto('/admin/login'); // Điều hướng tới trang đăng nhập
		}
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
						/>
					</div>
					<div class="input-wrapper">
						<label for="capacity">Số lượng ghế:</label>
						<input
							type="number"
							id="capacity"
							bind:value={upAirplane.capacity}
							placeholder="Nhập số lượng"
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