<script>
	import { onMount } from 'svelte';

	let flights = [];
	let error = '';

	const fetchFlights = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/flights', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (response.ok) {
				const data = await response.json();
				flights = data;
				console.log(flights);
			} else {
				const err = await response.json();
				error = err.msg || 'Lỗi khi lấy dữ liệu chuyến bay.';
			}
		} catch (err) {
			console.error('Lỗi khi lấy dữ liệu chuyến bay.', err);
			error = 'Đã xảy ra lỗi khi lấy dữ liệu chuyến bay.';
		}
	};

	onMount(() => {
		fetchFlights();
	});

	let showModalDelete = false;
	let select_flight_id = '';

	const openModalDelete = (flight_id) => {
		select_flight_id = flight_id;
		showModalDelete = true;
	};

	const closeModalDelete = () => {
		showModalDelete = false;
		select_flight_id = '';
	};

	const deleteFlight = async (flight_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/flights/${flight_id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchFlights();
				closeModalDelete();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi khóa chuyến bay.', error);
			alert('Đã xảy ra lỗi khi khóa chuyến bay.');
		}
	};
</script>

<div class="header-container">
	<div class="info-box">
		<p>Tổng số chuyến bay: <strong>{flights.length}</strong></p>
	</div>
	<div class="add-account-container">
		<button class="btn-add-admin">Thêm chuyến bay</button>
	</div>
</div>

<table class="table-flight">
	<thead>
		<tr>
			<th scope="col">ID</th>
			<th scope="col">Tên chuyến bay</th>
			<th scope="col">Điểm đi</th>
			<th scope="col">Điểm đến</th>
			<th scope="col">Ngày đi</th>
			<th scope="col">Giờ đi</th>
			<th scope="col">Trạng thái</th>
			<th scope="col">Máy bay</th>
			<th scope="col">Khóa</th>
			<th class="action-header">Hành động</th>
		</tr>
	</thead>
	<tbody>
		{#each flights as flight}
			<tr>
				<td>{flight.flight_id}</td>
				<td>{flight.flight_number}</td>
				<td>{flight.departure}</td>
				<td>{flight.arrival}</td>
				<td>{flight.departure_time}</td>
				<td>{flight.departure_hour_time}</td>
				<td>{flight.status}</td>
				<td>{flight.airplane_id}</td>
				<td>
					{#if flight.is_locked === 1}
						Khóa
					{:else}
						Mở
					{/if}
				</td>
				<td class="action-cell">
					<button class="edit">Sửa</button>
					<button
						class="delete {flight.is_locked === 1 ? 'open' : 'locked'}"
						on:click={() => openModalDelete(flight.flight_id)}
					>
						{#if flight.is_locked === 1}
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
					<h3 class="warning-text">Bạn có chắc chắn muốn khóa chuyến bay?</h3>
					<div class="button-group">
						<button on:click={() => deleteFlight(select_flight_id)} class="delete-btn"
							>Đồng ý</button
						>
						<button on:click={closeModalDelete} class="cancel-btn">Không</button>
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
</style>
