<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let seats = [];
	let error = '';

	const fetchSeats = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/seats', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (response.ok) {
				const data = await response.json();
				seats = data;
				console.log(seats);
			} else {
				const err = await response.json();
				error = err.msg || 'Lỗi khi lấy danh sách ghế.';
			}
		} catch (err) {
			console.error('Lỗi khi lấy danh sách ghế.', err);
			error = 'Đã xảy ra lỗi khi lấy danh sách ghế.';
		}
	};

	onMount(() => {
		const token = localStorage.getItem('jwt');
		if (!token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập!');
			goto('/admin/login'); // Điều hướng tới trang đăng nhập
		}
		fetchSeats();
	});

	let showModalAdd = false;
	let newSeat = {
		seat_number: '',
		airplane_id: '',
		seat_class: '',
		price: ''
	};
	let addError = '';

	const openModalAdd = () => {
		showModalAdd = true;
		newSeat = {
			seat_number: '',
			airplane_id: '',
			seat_class: '',
			price: ''
		};
		addError = '';
	};

	const closeModalAdd = () => {
		showModalAdd = false;
		newSeat = {
			seat_number: '',
			airplane_id: '',
			seat_class: '',
			price: ''
		};
		addError = '';
	};

	const addSeat = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/seats', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify(newSeat)
			});

			const result = await response.json();

			if (response.ok) {
				alert(result.msg);
				fetchSeats();
				closeModalAdd();
			} else {
				const err = await response.json();
				addError = result.msg || 'Không thể thêm ghế.';
			}
		} catch (err) {
			console.error('Lỗi khi thêm ghế.', err);
			addError = 'Đã xảy ra lỗi khi thêm ghế.';
		}
	};

	let showModalDelete = false;
	let select_seat_id = '';

	const openModalDelete = (seat_id) => {
		select_seat_id = seat_id;
		showModalDelete = true;
	};

	const closeModalDelete = () => {
		showModalDelete = false;
		select_seat_id = '';
	};

	const deleteSeat = async (seat_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/seats/${seat_id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchSeats();
				closeModalDelete();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi xóa ghế.', error);
			alert('Đã xảy ra lỗi khi xóa ghế.');
		}
	};

	let showModalUpdate = false;
	let upSeat = {
		seat_number: '',
		airplane_id: '',
		seat_class: '',
		price: ''
	};
	let updateError = '';

	const openModalUpdate = (seat_id) => {
		showModalUpdate = true;
		select_seat_id = seat_id;
		upSeat = {
			seat_number: '',
			airplane_id: '',
			seat_class: '',
			price: ''
		};
		updateError = '';
	};

	const closeModalUpdate = () => {
		showModalUpdate = false;
		upSeat = {
			seat_number: '',
			airplane_id: '',
			seat_class: '',
			price: ''
		};
		updateError = '';
		select_seat_id = '';
	};

	const updateSeat = async (seat_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/seats/${seat_id}`, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(upSeat)
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchSeats();
				closeModalUpdate();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi cập nhật ghế.', error);
			updateError = 'Đã xảy ra lỗi khi cập nhật ghế.';
		}
	};
</script>

<div class="header-container">
	<div class="info-box">
		<p>Tổng số lượng ghế: <strong>{seats.length}</strong></p>
	</div>
	<div class="add-account-container">
		<button class="btn-add-admin" on:click={openModalAdd}>Thêm ghế</button>
	</div>
</div>
{#if showModalAdd}
	<div class="modal">
		<div class="modal-content1 animate">
			<h3>Thêm ghế</h3>
			{#if addError}
				<p class="error-text">{addError}</p>
			{/if}

			<div class="modal-body">
				<div class="input-wrapper">
					<label for="seat_number">Số ghế</label>
					<input
						type="text"
						id="seat_number"
						bind:value={newSeat.seat_number}
						placeholder="Nhập số ghế"
					/>
				</div>
				<div class="input-wrapper">
					<label for="airplane_id">ID máy bay</label>
					<input
						type="number"
						id="airplane_id"
						bind:value={newSeat.airplane_id}
						placeholder="Nhập ID máy bay"
					/>
				</div>
			</div>

			<div class="modal-body">
				<div class="input-wrapper">
					<label for="seat_class">Hạng ghế</label>
					<select bind:value={newSeat.seat_class} class="custom-select">
						<option value="">Chọn hạng ghế</option>
						<option value="business">BUSINESS</option>
						<option value="skyboss">SKYBOSS</option>
						<option value="economy">ECONOMY</option>
					</select>
				</div>
				<div class="input-wrapper">
					<label for="price">Giá</label>
					<input type="text" id="price" bind:value={newSeat.price} placeholder="Nhập giá" />
				</div>
			</div>
			<div class="button-group">
				<button class="submit-btn" on:click={addSeat}>Thêm</button>
				<button class="cancel-btn" on:click={closeModalAdd}>Hủy</button>
			</div>
		</div>
	</div>
{/if}

<table class="table-seat">
	<thead>
		<tr>
			<th scope="col" class="sortable-header">ID</th>
			<th scope="col" class="sortable-header">ID máy bay</th>
			<th scope="col" class="sortable-header">Số ghế</th>
			<th scope="col" class="sortable-header">Hạng ghế</th>
			<th scope="col" class="sortable-header">Giá</th>
			<th class="action-header">Hành động</th>
		</tr>
	</thead>
	<tbody>
		{#each seats as seat}
			<tr>
				<td>{seat.seat_id}</td>
				<td>{seat.airplane_id}</td>
				<td>{seat.seat_number}</td>
				<td>{seat.seat_class}</td>
				<td>{seat.price}</td>
				<td class="action-cell">
					<button class="edit" on:click={() => openModalUpdate(seat.seat_id)}>Sửa</button>
					<button class="delete" on:click={() => openModalDelete(seat.seat_id)}>Xóa</button>
				</td>
			</tr>
		{/each}

		{#if showModalDelete}
			<div class="modal">
				<div class="modal-content delete-modal animate">
					<h3 class="warning-text">Bạn có chắc chắn muốn xóa ghế?</h3>
					<div class="button-group">
						<button on:click={() => deleteSeat(select_seat_id)} class="delete-btn">Đồng ý</button>
						<button on:click={closeModalDelete} class="cancel-btn">Không</button>
					</div>
				</div>
			</div>
		{/if}

		{#if showModalUpdate}
			<div class="modal">
				<div class="modal-content1 animate">
					<h3>Cập nhật ghế</h3>
					{#if addError}
						<p class="error-text">{updateError}</p>
					{/if}

					<div class="modal-body">
						<div class="input-wrapper">
							<label for="seat_number">Số ghế</label>
							<input
								type="text"
								id="seat_number"
								bind:value={upSeat.seat_number}
								placeholder="Nhập số ghế"
							/>
						</div>
						<div class="input-wrapper">
							<label for="airplane_id">ID máy bay</label>
							<input
								type="number"
								id="airplane_id"
								bind:value={upSeat.airplane_id}
								placeholder="Nhập ID máy bay"
							/>
						</div>
					</div>

					<div class="modal-body">
						<div class="input-wrapper">
							<label for="seat_class">Hạng ghế</label>
							<select bind:value={upSeat.seat_class} class="custom-select">
								<option value="">Chọn hạng ghế</option>
								<option value="business">BUSINESS</option>
								<option value="skyboss">SKYBOSS</option>
								<option value="economy">ECONOMY</option>
							</select>
						</div>
						<div class="input-wrapper">
							<label for="price">Giá</label>
							<input type="text" id="price" bind:value={upSeat.price} placeholder="Nhập giá" />
						</div>
					</div>
					<div class="button-group">
						<button on:click={() => updateSeat(select_seat_id)} class="submit-btn"
							>Cập nhật</button
						>
						<button class="cancel-btn" on:click={closeModalUpdate}>Hủy</button>
					</div>
				</div>
			</div>
		{/if}
	</tbody>
</table>