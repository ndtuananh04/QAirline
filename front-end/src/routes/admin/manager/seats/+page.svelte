<script>
	import { onMount } from 'svelte';

	let seats = [];
	let error = '';

	const fetchSeats = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/seats-airplane', {
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
		fetchSeats();
	});
</script>

<div class="header-container">
	<div class="add-account-container">
		<button class="btn-add-admin">Thêm ghế</button>
	</div>
</div>

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
					<button class="edit" >Sửa</button>
					<button class="delete" >Xóa</button>
				</td>
			</tr>
		{/each}
	</tbody>
</table>

<style>
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