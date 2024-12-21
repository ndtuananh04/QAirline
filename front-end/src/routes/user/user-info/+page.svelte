<script>
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import flatpickr from 'flatpickr';
	import 'flatpickr/dist/flatpickr.min.css';

	let isEditing = writable(false); // Biến để kiểm tra trạng thái đang chỉnh sửa
	let user = writable({
		family_name: '',
		given_name: '',
		gender: '',
		date_of_birth: '',
		identification: '',
		nationality: '',
		email: '',
		phone_number: ''
	});

	let isLoading = writable(true);

	const fetchInfo = async () => {
		const token = localStorage.getItem('jwt');
		const response = await fetch('http://127.0.0.1:5000/user-info', {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`
			}
		});

		if (response.ok) {
			const data = await response.json();
			user.set(data);
		} else {
			const err = await response.json();
			alert(err.msg || 'Lỗi khi lấy thông tin người dùng');
		}
	};

	let dateOfBirthPicker;

	onMount(() => {
		if (dateOfBirthPicker) {
			flatpickr(dateOfBirthPicker, {
				dateFormat: 'd/m/Y',
				altFormat: 'Y-m-d',
				maxDate: new Date().setFullYear(new Date().getFullYear()),
				onChange: function (selectedDates) {
					if (selectedDates[0]) {
						const date = selectedDates[0];
						$user.date_of_birth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
					}
				}
			});
		}
	});

	onMount(async () => {
		const token = localStorage.getItem('jwt');
		if (!token) {
			goto('/');
		}
		fetchInfo();
	});

	function toggleEdit() {
		isEditing.update((value) => !value);
	}

	async function updateUser() {
		const token = localStorage.getItem('jwt');
		const res = await fetch('http://127.0.0.1:5000/user-info', {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify($user)
		});
		if (res.ok) {
			alert('Cập nhật thông tin thành công!');
			isEditing.set(false);
		} else {
			alert('Cập nhật thất bại!');
		}
	}
</script>

<div class="container">
	<div class="main-body">
		<div class="row gutters-sm">
			<div class="col-md-4 mb-3">
				<div class="card">
					<div class="card-body">
						<div class="d-flex flex-column align-items-center text-center">
							<img src="/images/user.png" alt="Admin" class="rounded-circle" width="150" />
							<div class="mt-3">
								<h4>{$user.family_name} {$user.given_name}</h4>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="col-md-8">
				<div class="card mb-3">
					<div class="card-body">
						<div class="row">
							<div class="col-sm-3">
								<h6 class="mb-0">Họ:</h6>
							</div>
							<div class="col-sm-9 text-secondary">
								{#if $isEditing}
									<input type="text" bind:value={$user.family_name} class="form-control" />
								{:else}
									{$user.family_name}
								{/if}
							</div>
						</div>
						<hr />
						<div class="row">
							<div class="col-sm-3">
								<h6 class="mb-0">Tên:</h6>
							</div>
							<div class="col-sm-9 text-secondary">
								{#if $isEditing}
									<input type="text" bind:value={$user.given_name} class="form-control" />
								{:else}
									{$user.given_name}
								{/if}
							</div>
						</div>
						<hr />
						<div class="row">
							<div class="col-sm-3">
								<h6 class="mb-0">Giới tính:</h6>
							</div>
							<div class="col-sm-9 text-secondary">
								{#if $isEditing}
									<input type="text" bind:value={$user.gender} class="form-control" />
								{:else}
									{$user.gender}
								{/if}
							</div>
						</div>
						<hr />
						<div class="row">
							<div class="col-sm-3">
								<h6 class="mb-0">Ngày sinh:</h6>
							</div>
							<div class="col-sm-9 text-secondary">
								{#if $isEditing}
									<input
										type="text"
										id="date_of_birth"
										bind:this={dateOfBirthPicker}
										name="date_of_birth"
										class="form-control"
										placeholder="Chọn ngày sinh"
										required
									/>
								{:else}
									{$user.date_of_birth}
								{/if}
							</div>
						</div>
						<hr />
						<div class="row">
							<div class="col-sm-3">
								<h6 class="mb-0">CCCD:</h6>
							</div>
							<div class="col-sm-9 text-secondary">
								{#if $isEditing}
									<input type="text" bind:value={$user.identification} class="form-control" />
								{:else}
									{$user.identification}
								{/if}
							</div>
						</div>
						<hr />
						<div class="row">
							<div class="col-sm-3">
								<h6 class="mb-0">Quốc tịch:</h6>
							</div>
							<div class="col-sm-9 text-secondary">
								{#if $isEditing}
									<input type="text" bind:value={$user.nationality} class="form-control" />
								{:else}
									{$user.nationality}
								{/if}
							</div>
						</div>
						<hr />
						<div class="row">
							<div class="col-sm-3">
								<h6 class="mb-0">Email:</h6>
							</div>
							<div class="col-sm-9 text-secondary">
								{#if $isEditing}
									<input type="text" bind:value={$user.email} class="form-control" />
								{:else}
									{$user.email}
								{/if}
							</div>
						</div>
						<hr />
						<div class="row">
							<div class="col-sm-3">
								<h6 class="mb-0">Số điện thoại:</h6>
							</div>
							<div class="col-sm-9 text-secondary">
								{#if $isEditing}
									<input type="text" bind:value={$user.phone_number} class="form-control" />
								{:else}
									{$user.phone_number}
								{/if}
							</div>
						</div>
						<hr />
						<div class="row">
							<div class="col-sm-12">
								{#if $isEditing}
									<button class="btn btn-success" on:click={updateUser}>Cập nhật</button>
									<button class="btn btn-secondary" on:click={toggleEdit}>Hủy</button>
								{:else}
									<button class="btn btn-info" on:click={toggleEdit}>Sửa</button>
								{/if}
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
