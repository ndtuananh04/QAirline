<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

    let promotions = [];
    let error = '';

    const fetchPromotion = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/promotions', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (response.ok) {
				const data = await response.json();
				promotions = data;
			} else {
				const err = await response.json();
				error = err.msg || 'Lỗi khi lấy danh sách mã khuyến mãi.';
			}
		} catch (err) {
			console.error('Lỗi khi lấy danh sách mã khuyến mãi.', err);
			error = 'Đã xảy ra lỗi khi lấy danh sách mã khuyến mãi.';
		}
	};

	onMount(() => {
		const token = localStorage.getItem('jwt');
		if (!token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập!');
			goto('/admin/login'); // Điều hướng tới trang đăng nhập
		}
		fetchPromotion();
	});

    let showModalAdd = false;
	let newPromotion = { code_promotion: '', percent: '' };
	let addError = '';

	const openModalAdd = () => {
		showModalAdd = true;
		newPromotion = { code_promotion: '', percent: '' };
		addError = '';
	};

	const closeModalAdd = () => {
		showModalAdd = false;
		newPromotion = { code_promotion: '', percent: '' };
		addError = '';
	};

	const addPromotion = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/promotions', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify(newPromotion)
			});

			const result = await response.json();

			if (response.ok) {
				alert(result.msg);
				fetchPromotion();
				closeModalAdd();
			} else {
				const err = await response.json();
				addError = result.msg || 'Không thể thêm mã khuyến mãi.';
			}
		} catch (err) {
			console.error('Lỗi khi thêm mã khuyến mãi.', err);
			addError = 'Đã xảy ra lỗi khi thêm mã khuyến mãi.';
		}
	};

    let showModalUpdate = false;
	let upPromotion = { code_promotion: '', percent: '' };
	let updateError = '';
    let select_promotion_id = '';

	const openModalUpdate = (promotion_id) => {
		showModalUpdate = true;
		select_promotion_id = promotion_id;
		upPromotion = { code_promotion: '', percent: '' };
		updateError = '';
	};

	const closeModalUpdate = () => {
		showModalUpdate = false;
		upPromotion = { code_promotion: '', percent: '' };
		updateError = '';
		select_promotion_id = '';
	};

	const updatePromotion = async (promotion_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/promotions/${promotion_id}`, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(upPromotion)
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchPromotion();
				closeModalUpdate();
			} else {
				alert(result.msg);
                updateError = result.msg || 'Không thể cập nhật khuyến mãi.';
			}
		} catch (error) {
			console.error('Lỗi khi cập nhật khuyến mãi:', error);
			updateError = 'Đã xảy ra lỗi khi cập nhật khuyến mãi.';
		}
	};
    let showModalDelete = false;

	const openModalDelete = (promotion_id) => {
		select_promotion_id = promotion_id;
		showModalDelete = true;
	};

	const closeModalDelete = () => {
		showModalDelete = false;
		select_promotion_id = '';
	};

	const deletePromotion = async (promotion_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/promotions/${promotion_id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchPromotion();
				closeModalDelete();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi xóa khuyến mãi:', error);
			alert('Đã xảy ra lỗi khi xóa khuyến mãi.'); 
		}
	};
</script>

<div class="header-container">
    <div class="info-box">
		<p>Tổng số khuyễn mãi: <strong>{promotions.length}</strong></p>
	</div>
	<div class="add-account-container">
		<button class="btn-add-admin" on:click={openModalAdd}>Thêm mã khuyến mại</button>
	</div>
</div>
{#if showModalAdd}
	<div class="modal">
		<div class="modal-content animate">
			<h3>Thêm mã khuyến mại</h3>
			{#if addError}
				<p class="error-text">{addError}</p>
			{/if}
			<div class="input-wrapper">
                <label for="code_promotion">Mã khuyến mại:</label>
                <input
                    type="text"
                    id="code_promotion"
                    bind:value={newPromotion.code_promotion}
                    placeholder="Nhập mã khuyến mại"
                />
            </div>
            <div class="input-wrapper">
                <label for="percent">Phần trăm</label>
                <input
                    type="text"
                    id="percent"
                    bind:value={newPromotion.percent}
                    placeholder="Nhập phần trăm"
                />
            </div>
			<div class="button-group">
				<button class="submit-btn" on:click={addPromotion}>Thêm</button>
				<button class="cancel-btn" on:click={closeModalAdd}>Hủy</button>
			</div>
		</div>
	</div>
{/if}

<table class="table-post">
	<thead>
		<tr>
			<th scope="col" class="sortable-header">ID</th>
			<th scope="col" class="sortable-header">Mã khuyến mãi</th>
            <th scope="col" class="sortable-header">Phần trăm</th>
			<th class="action-header">Hành động</th>
		</tr>
	</thead>
	<tbody>
		{#each promotions as promotion}
			<tr>
				<td>{promotion.promotion_id}</td>
				<td>{promotion.code_promotion}</td>
                <td>{promotion.percent}</td>
				<td class="action-cell">
					<button class="edit" on:click={() => openModalUpdate(promotion.promotion_id)}>Sửa</button>
					<button class="delete" on:click={() => openModalDelete(promotion.promotion_id)}>Xóa</button>
				</td>
			</tr>
		{/each}

        {#if showModalDelete}
			<div class="modal">
				<div class="modal-content delete-modal animate">
					<h3 class="warning-text">Bạn có chắc chắn muốn xóa khuyến mại?</h3>
					<div class="button-group">
						<button on:click={() => deletePromotion(select_promotion_id)} class="delete-btn"
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
					<h3>Cập nhật mã khuyến mại</h3>
					{#if updateError}
						<p class="error-text">{updateError}</p>
					{/if}
					<div class="input-wrapper">
						<label for="code_promotion">Mã khuyến mại:</label>
						<input
							type="text"
							id="code_promotio"
							bind:value={upPromotion.code_promotion}
							placeholder="Nhập mã khuyến mại"
						/>
					</div>
					<div class="input-wrapper">
						<label for="percent">Phần trăm</label>
						<input
							type="number"
							id="percent"
							bind:value={upPromotion.percent}
							placeholder="Nhập phần trăm"
						/>
					</div>
					<div class="button-group">
						<button on:click={() => updatePromotion(select_promotion_id)} class="submit-btn"
							>Cập nhật</button
						>
						<button on:click={closeModalUpdate} class="cancel-btn">Hủy</button>
					</div>
				</div>
			</div>
		{/if}
    </tbody>
</table>
