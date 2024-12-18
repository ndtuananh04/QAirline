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
		const token = localStorage.getItem('jwt');
		if (!token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập!');
			goto('/admin/login'); // Điều hướng tới trang đăng nhập
		}
		fetchFlights();
	});

	let showModalAdd = false;
	let newFlight = {
		flight_number: '',
		departure: '',
		code_departure: '',
		arrival: '',
		code_arrival: '',
		departure_time: '',
		departure_hour_time: '',
		arrival_hour_time: '',
		boarding_time: '',
		terminal: '',
		status: '',
		airplane_id: ''
	};
	let addError = '';

	const openModalAdd = () => {
		showModalAdd = true;
		newFlight = {
			flight_number: '',
			departure: '',
			code_departure: '',
			arrival: '',
			code_arrival: '',
			departure_time: '',
			departure_hour_time: '',
			arrival_hour_time: '',
			boarding_time: '',
			terminal: '',
			status: '',
			airplane_id: ''
		};
		addError = '';
	};

	const closeModalAdd = () => {
		showModalAdd = false;
		newFlight = {
			flight_number: '',
			departure: '',
			code_departure: '',
			arrival: '',
			code_arrival: '',
			departure_time: '',
			departure_hour_time: '',
			arrival_hour_time: '',
			boarding_time: '',
			terminal: '',
			status: '',
			airplane_id: ''
		};
		addError = '';
	};

	const addFlight = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/flights', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify(newFlight)
			});

			const result = await response.json();

			if (response.ok) {
				alert(result.msg);
				fetchFlights();
				closeModalAdd();
			} else {
				const err = await response.json();
				addError = result.msg || 'Không thể thêm chuyến bay.';
			}
		} catch (err) {
			console.error('Lỗi khi thêm chuyến bay.', err);
			addError = 'Đã xảy ra lỗi khi thêm chuyến bay.';
		}
	};

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

	let showModalUpdate = false;
	let upFlight = {
		flight_number: '',
		departure: '',
		code_departure: '',
		arrival: '',
		code_arrival: '',
		departure_time: '',
		departure_hour_time: '',
		arrival_hour_time: '',
		boarding_time: '',
		status: '',
		airplane_id: ''
	};
	let updateError = '';

	const openModalUpdate = (flight_id) => {
		showModalUpdate = true;
		select_flight_id = flight_id;
		upFlight = {
			flight_number: '',
			departure: '',
			code_departure: '',
			arrival: '',
			code_arrival: '',
			departure_time: '',
			departure_hour_time: '',
			arrival_hour_time: '',
			boarding_time: '',
			status: '',
			airplane_id: ''
		};
		updateError = '';
	};

	const closeModalUpdate = () => {
		showModalUpdate = false;
		upFlight = {
			flight_number: '',
			departure: '',
			code_departure: '',
			arrival: '',
			code_arrival: '',
			departure_time: '',
			departure_hour_time: '',
			arrival_hour_time: '',
			boarding_time: '',
			status: '',
			airplane_id: ''
		};
		updateError = '';
		select_flight_id = '';
	};

	const updateFlight = async (flight_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/flights/${flight_id}`, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(upFlight)
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchFlights();
				closeModalUpdate();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi cập nhật chuyến bay.', error);
			updateError = 'Đã xảy ra lỗi khi cập nhật chuyến bay.';
		}
	};

	const validateTime = (time) => {
		const regex = /^([01]?[0-9]|2[0-3]):([0-5][0-9])$/;
		const match = time.match(regex); // Kiểm tra định dạng HH:MM

		if (!match) {
			return false; // Nếu không khớp định dạng HH:MM
		}

		const hours = parseInt(match[1], 10); // Giờ (HH)
		const minutes = parseInt(match[2], 10); // Phút (MM)

		// Kiểm tra giờ lớn hơn 0 và nhỏ hơn 24, phút từ 0 đến 59
		if (hours >= 0 && hours < 24 && minutes >= 0 && minutes <= 59) {
			return true;
		}

		return false;
	};

	function sortById() {
		flights = [...flights].sort((a, b) => a.flight_id - b.flight_id);
	}

	function sortByFlightName() {
		flights = [...flights].sort((a, b) => {
			if (a.flight_number < b.flight_number) {
				return -1;
			} else if (a.flight_number > b.flight_number) {
				return 1;
			}
			return 0;
		});
	}

	function sortByDeparture() {
		flights = [...flights].sort((a, b) => a.departure.localeCompare(b.departure));
	}

	function sortByArrival() {
		flights = [...flights].sort((a, b) => a.arrival.localeCompare(b.arrival));
	}

	function sortByDepartureTime() {
		flights = [...flights].sort((a, b) => new Date(b.departure_time) - new Date(a.departure_time));
	}

	function sortByDepartureHourTime() {
		flights = [...flights].sort((a, b) => {
			const timeA = a.departure_hour_time.split(':').map(Number);
			const timeB = b.departure_hour_time.split(':').map(Number);
			const totalMinutesA = timeA[0] * 60 + timeA[1];
			const totalMinutesB = timeB[0] * 60 + timeB[1];
			return (totalMinutesA - totalMinutesB) * sortOrder;
		});
		sortOrder *= -1; // Đổi thứ tự tăng/giảm
	}

	function sortByStatus() {
		flights = [...flights].sort((a, b) => {
			if (a.status < b.status) {
				return -1;
			} else if (a.status > b.status) {
				return 1;
			}
			return 0;
		});
	}

	function sortByAirplaneId() {
		flights = [...flights].sort((a, b) => {
			return (a.airplane_id - b.airplane_id) * sortOrder;
		});
		sortOrder *= -1; // Đổi thứ tự tăng/giảm
	}

	function sortByIsLocked() {
		flights = [...flights].sort((a, b) => {
			return (b.is_locked - a.is_locked) * sortOrder; // Ưu tiên giá trị is_locked = 1 (Khóa) lên đầu
		});
		sortOrder *= -1; // Đổi thứ tự tăng/giảm
	}
</script>

<div class="header-container">
	<div class="info-box">
		<p>Số chuyến bay: <strong>{flights.length}</strong></p>
	</div>
	<div class="info-box">
		<p>Số chuyến bay đang lên lịch: <strong>{flights.filter(flight => flight.status === 'SCHEDULED').length}</strong></p>
	</div>
	<div class="info-box">
		<p>Số chuyến bay chậm: <strong>{flights.filter(flight => flight.status === 'DELAYED').length}</strong></p>
	</div>
	<div class="info-box">
		<p>Số chuyến bay hủy: <strong>{flights.filter(flight => flight.status === 'CANCELLED').length}</strong></p>
	</div>
	<div class="add-account-container">
		<button class="btn-add-admin" on:click={openModalAdd}>Thêm chuyến bay</button>
	</div>
</div>
{#if showModalAdd}
	<div class="modal">
		<div class="modal-content1 animate">
			<h3>Thêm chuyến bay</h3>
			{#if addError}
				<p class="error-text">{addError}</p>
			{/if}

			<div class="modal-body">
				<div class="input-wrapper">
					<label for="flight_number">Tên chuyến bay:</label>
					<input
						type="text"
						id="flight_number"
						bind:value={newFlight.flight_number}
						placeholder="Nhập tên chuyến bay"
						required
					/>
				</div>
				<div class="input-wrapper">
					<label for="departure_time">Ngày đi:</label>
					<input type="date" id="departure_time" bind:value={newFlight.departure_time} required />
				</div>
			</div>

			<div class="modal-body">
				<div class="input-wrapper">
					<label for="departure">Điểm đi:</label>
					<input
						type="text"
						id="departure"
						bind:value={newFlight.departure}
						placeholder="Nhập điểm đi"
						required
					/>
				</div>
				<div class="input-wrapper">
					<label for="code_departure">Mã điểm đến:</label>
					<input
						type="text"
						id="code_departure"
						bind:value={newFlight.code_departure}
						placeholder="Nhập mã điểm đến"
						required
					/>
				</div>
			</div>

			<div class="modal-body">
				<div class="input-wrapper">
					<label for="arrival">Điểm đến:</label>
					<input
						type="text"
						id="arrival"
						bind:value={newFlight.arrival}
						placeholder="Nhập điểm đến"
						required
					/>
				</div>
				<div class="input-wrapper">
					<label for="code_arrival">Mã điểm đến:</label>
					<input
						type="text"
						id="code_arrival"
						bind:value={newFlight.code_arrival}
						placeholder="Nhập mã điểm đến"
						required
					/>
				</div>
			</div>

			<div class="modal-body">
				<div class="input-wrapper">
					<label for="departure_hour_time">Giờ đi:</label>
					<input
						type="text"
						id="departure_hour_time"
						placeholder="HH:MM"
						bind:value={newFlight.departure_hour_time}
						on:input={() => {
							if (!validateTime(newFlight.departure_hour_time)) {
								updateError = 'Giờ đi phải theo định dạng HH:MM';
							} else {
								updateError = '';
							}
						}}
						required
					/>
				</div>
				<div class="input-wrapper">
					<label for="arrival_hour_time">Giờ đến:</label>
					<input
						type="text"
						id="arrival_hour_time"
						placeholder="HH:MM"
						bind:value={newFlight.arrival_hour_time}
						on:input={() => {
							if (!validateTime(newFlight.arrival_hour_time)) {
								updateError = 'Giờ đến phải theo định dạng HH:MM';
							} else {
								updateError = '';
							}
						}}
						required
					/>
				</div>
			</div>

			<div class="modal-body">
				<div class="input-wrapper">
					<label for="boarding_time">Thời gian lên máy bay:</label>
					<input
						type="text"
						id="boarding_time"
						placeholder="HH:MM"
						bind:value={newFlight.boarding_time}
						on:input={() => {
							if (!validateTime(newFlight.boarding_time)) {
								updateError = 'Thời gian lên máy bay phải theo định dạng HH:MM';
							} else {
								updateError = '';
							}
						}}
						required
					/>
				</div>
				<div class="input-wrapper">
					<label for="status">Trạng thái:</label>
					<select bind:value={newFlight.status} class="custom-select">
						<option value="scheduled">SCHEDULED</option>
						<option value="delayed">DELAYED</option>
						<option value="cancelled">CANCELLED</option>
					</select>
				</div>
			</div>

			<div class="modal-body">
				<div class="input-wrapper">
					<label for="terminal">Nhà ga:</label>
					<input type="number" id="terminal" bind:value={newFlight.terminal} required />
				</div>
				<div class="input-wrapper">
					<label for="airplane_id">Máy bay:</label>
					<input type="number" id="airplane_id" bind:value={newFlight.airplane_id} required />
				</div>
			</div>

			<div class="button-group">
				<button class="submit-btn" on:click={addFlight}>Thêm</button>
				<button class="cancel-btn" on:click={closeModalAdd}>Hủy</button>
			</div>
		</div>
	</div>
{/if}

<table class="table-flight">
	<thead>
		<tr>
			<th scope="col" class="sortable-header" on:click={sortById}>ID</th>
			<th scope="col" class="sortable-header" on:click={sortByFlightName}>Tên chuyến bay</th>
			<th scope="col" class="sortable-header" on:click={sortByDeparture}>Điểm đi</th>
			<th scope="col" class="sortable-header" on:click={sortByArrival}>Điểm đến</th>
			<th scope="col" class="sortable-header" on:click={sortByDepartureTime}>Ngày đi</th>
			<th scope="col" class="sortable-header" on:click={sortByDepartureHourTime}>Giờ đi</th>
			<th scope="col" class="sortable-header" on:click={sortByStatus}>Trạng thái</th>
			<th scope="col" class="sortable-header" on:click={sortByAirplaneId}>Máy bay</th>
			<th scope="col" class="sortable-header" on:click={sortByIsLocked}>Khóa</th>
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
					<button class="edit" on:click={() => openModalUpdate(flight.flight_id)}>Sửa</button>
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

		{#if showModalUpdate}
			<div class="modal">
				<div class="modal-content1 animate">
					<h3>Cập nhật thông tin chuyến bay</h3>
					{#if updateError}
						<p class="error-text">{updateError}</p>
					{/if}

					<div class="modal-body">
						<div class="input-wrapper">
							<label for="flight_number">Tên chuyến bay:</label>
							<input
								type="text"
								id="flight_number"
								bind:value={upFlight.flight_number}
								placeholder="Nhập tên chuyến bay"
							/>
						</div>
						<div class="input-wrapper">
							<label for="departure_time">Ngày đi:</label>
							<input
								type="date"
								id="departure_time"
								bind:value={upFlight.departure_time}
							/>
						</div>
					</div>

					<div class="modal-body">
						<div class="input-wrapper">
							<label for="departure">Điểm đi:</label>
							<input
								type="text"
								id="departure"
								bind:value={upFlight.departure}
								placeholder="Nhập điểm đi"
							/>
						</div>
						<div class="input-wrapper">
							<label for="code_departure">Mã điểm đến:</label>
							<input
								type="text"
								id="code_departure"
								bind:value={upFlight.code_departure}
								placeholder="Nhập mã điểm đến"
							/>
						</div>
					</div>

					<div class="modal-body">
						<div class="input-wrapper">
							<label for="arrival">Điểm đến:</label>
							<input
								type="text"
								id="arrival"
								bind:value={upFlight.arrival}
								placeholder="Nhập điểm đến"
							/>
						</div>
						<div class="input-wrapper">
							<label for="code_arrival">Mã điểm đến:</label>
							<input
								type="text"
								id="code_arrival"
								bind:value={upFlight.code_arrival}
								placeholder="Nhập mã điểm đến"
							/>
						</div>
					</div>

					<div class="modal-body">
						<div class="input-wrapper">
							<label for="departure_hour_time">Giờ đi:</label>
							<input
								type="text"
								id="departure_hour_time"
								placeholder="HH:MM"
								bind:value={upFlight.departure_hour_time}
								on:input={() => {
									if (!validateTime(upFlight.departure_hour_time)) {
										updateError = 'Giờ đi phải theo định dạng HH:MM';
									} else {
										updateError = '';
									}
								}}
							/>
						</div>
						<div class="input-wrapper">
							<label for="arrival_hour_time">Giờ đến:</label>
							<input
								type="text"
								id="arrival_hour_time"
								placeholder="HH:MM"
								bind:value={upFlight.arrival_hour_time}
								on:input={() => {
									if (!validateTime(upFlight.arrival_hour_time)) {
										updateError = 'Giờ đến phải theo định dạng HH:MM';
									} else {
										updateError = '';
									}
								}}
							/>
						</div>
					</div>

					<div class="modal-body">
						<div class="input-wrapper">
							<label for="boarding_time">Thời gian lên máy bay:</label>
							<input
								type="text"
								id="boarding_time"
								placeholder="HH:MM"
								bind:value={upFlight.boarding_time}
								on:input={() => {
									if (!validateTime(upFlight.boarding_time)) {
										updateError = 'Thời gian lên máy bay phải theo định dạng HH:MM';
									} else {
										updateError = '';
									}
								}}
							/>
						</div>
						<div class="input-wrapper">
							<label for="status">Trạng thái:</label>
							<select bind:value={upFlight.status} class="custom-select">
								<option value="scheduled">SCHEDULED</option>
								<option value="delayed">DELAYED</option>
								<option value="cancelled">CANCELLED</option>
							</select>
						</div>
					</div>

					<div class="modal-body">
						<div class="input-wrapper">
							<label for="airplane_id">Máy bay:</label>
							<input type="number" id="airplane_id" bind:value={upFlight.airplane_id} />
						</div>
					</div>

					<div class="button-group">
						<button on:click={() => updateFlight(select_flight_id)} class="submit-btn"
							>Cập nhật</button
						>
						<button on:click={closeModalUpdate} class="cancel-btn">Hủy</button>
					</div>
				</div>
			</div>
		{/if}
	</tbody>
</table>