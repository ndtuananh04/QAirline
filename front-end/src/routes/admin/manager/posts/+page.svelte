<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let postsss = [];
	let error = '';
	let select_post_id = '';

	const fetchPostAdmin = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/posts', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (response.ok) {
				const data = await response.json();
				postsss = data;
				console.log(postsss);
			} else {
				const err = await response.json();
				error = err.msg || 'Lỗi khi lấy danh sách bài viết';
			}
		} catch (err) {
			console.error('Lỗi khi lấy danh sách bài viết:', err);
			error = 'Đã xảy ra lỗi khi lấy danh sách bài viết.';
		}
	};

	onMount(() => {
		const token = localStorage.getItem('jwt');
		if (!token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập!');
			goto('/admin/login'); // Điều hướng tới trang đăng nhập
		}
		fetchPostAdmin();
	});

    let showModalAdd = false;
	let newPost = { title: '', block_1: '', block_2: '', block_3: '', block_4: '', block_5: '' };
	let addError = '';

	const openModalAdd = () => {
		showModalAdd = true;
		newPost = { title: '', block_1: '', block_2: '', block_3: '', block_4: '', block_5: '' };
		addError = '';
	};

	const closeModalAdd = () => {
		showModalAdd = false;
		newPost = { title: '', block_1: '', block_2: '', block_3: '', block_4: '', block_5: '' };
		addError = '';
	};

	const addPost = async () => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch('http://localhost:5000/posts', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify(newPost)
			});

			const result = await response.json();

			if (response.ok) {
				alert(result.msg);
				fetchPostAdmin();
				closeModalAdd();
			} else {
				const err = await response.json();
				addError = result.msg || 'Không thể thêm bài viết';
			}
		} catch (err) {
			console.error('Lỗi khi thêm bài viết:', error);
			addError = 'Đã xảy ra lỗi khi thêm bài viết.';
		}
	};

	let showModalUpdate = false;
	let upPost = { title: '', block_1: '', block_2: '', block_3: '', block_4: '', block_5: '' };
	let updateError = '';

	const openModalUpdate = (post_id) => {
		showModalUpdate = true;
		select_post_id = post_id;
		fetchUpShowModal(post_id);
		updateError = '';
	};

	const closeModalUpdate = () => {
		showModalUpdate = false;
		upPost = { title: '', block_1: '', block_2: '', block_3: '', block_4: '', block_5: '' };
		updateError = '';
		select_post_id = '';
	};

	const updatePost = async (post_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/posts/${post_id}`, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(upPost)
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchPostAdmin();
				closeModalUpdate();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi cập nhật bài viết:', error);
			updateError = 'Đã xảy ra lỗi khi cập nhật bài viết.';   
		}
	};

    const fetchUpShowModal = async (post_id) => {
        const token = localStorage.getItem('jwt');
        try {
            const response = await fetch(`http://localhost:5000/post-modal/${post_id}`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Dữ liệu từ API:', data);
                upPost = {
                    title: data.title,
                    block_1: data.block_1,
                    block_2: data.block_2 || '',
                    block_3: data.block_3 || '',
                    block_4: data.block_4 || '',
                    block_5: data.block_5 || ''
                };
                console.log(upPost);
            } else {
                const err = await response.json();
                updateError = err.msg || 'Lỗi khi lấy thông tin bài viết';
            }
        } catch (err) {
            console.error('Lỗi khi lấy thông tin bài viết:', err);
            updateError = 'Đã xảy ra lỗi khi lấy thông tin bài viết.';
        }
    };

    let showModalDelete = false;
	const openModalDelete = (post_id) => {
		select_post_id = post_id;
		showModalDelete = true;
	};

	const closeModalDelete = () => {
		showModalDelete = false;
		select_post_id = '';
	};

	const deletePost = async (post_id) => {
		const token = localStorage.getItem('jwt');
		try {
			const response = await fetch(`http://localhost:5000/posts/${post_id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});
			const result = await response.json();
			if (response.ok) {
				alert(result.msg);
				fetchPostAdmin();
				closeModalDelete();
			} else {
				alert(result.msg);
			}
		} catch (error) {
			console.error('Lỗi khi xóa bài viết:', error);
			alert('Đã xảy ra lỗi khi xóa bài viết.');
		}
	};
</script>

<div class="header-container">
    <div class="info-box">
		<p>Tổng số bài viết: <strong>{postsss.length}</strong></p>
	</div>
	<div class="add-account-container">
		<button class="btn-add-admin" on:click={openModalAdd}>Thêm bài viết</button>
	</div>
</div>
{#if showModalAdd}
	<div class="modal">
		<div class="modal-content animate">
			<h3>Thêm bài viết</h3>
			{#if addError}
				<p class="error-text">{addError}</p>
			{/if}
			<div class="input-wrapper">
                <label for="title">Tiêu đề:</label>
                <input
                    type="text"
                    id="title"
                    bind:value={newPost.title}
                    placeholder="Nhập tiêu đề"
                />
            </div>
            <div class="input-wrapper">
                <label for="block_1">Nội dung 1</label>
                <input
                    type="text"
                    id="block_1"
                    bind:value={newPost.block_1}
                    placeholder="Nhập nội dung 1"
                />
            </div>
            <div class="input-wrapper">
                <label for="block_2">Nội dung 2</label>
                <input
                    type="text"
                    id="block_2"
                    bind:value={newPost.block_2}
                    placeholder="Nhập nội dung 2"
                />
            </div>
            <div class="input-wrapper">
                <label for="block_3">Nội dung 3</label>
                <input
                    type="text"
                    id="block_3"
                    bind:value={newPost.block_3}
                    placeholder="Nhập nội dung 3"
                />
            </div>
            <div class="input-wrapper">
                <label for="block_4">Nội dung 4</label>
                <input
                    type="text"
                    id="block_4"
                    bind:value={newPost.block_4}
                    placeholder="Nhập nội dung 4"
                />
            </div>
            <div class="input-wrapper">
                <label for="block_5">Nội dung 5</label>
                <input
                    type="text"
                    id="block_5"
                    bind:value={newPost.block_5}
                    placeholder="Nhập nội dung 5"
                />
            </div>
			<div class="button-group">
				<button class="submit-btn" on:click={addPost}>Thêm</button>
				<button class="cancel-btn" on:click={closeModalAdd}>Hủy</button>
			</div>
		</div>
	</div>
{/if}

<table class="table-post">
	<thead>
		<tr>
			<th scope="col" class="sortable-header">ID</th>
			<th scope="col" class="sortable-header">Tiêu đề</th>
			<th class="action-header">Hành động</th>
		</tr>
	</thead>
	<tbody>
		{#each postsss as post}
			<tr>
				<td>{post.post_id}</td>
				<td>{post.title}</td>
				<td class="action-cell">
					<button class="edit" on:click={() => openModalUpdate(post.post_id)}>Sửa</button>
					<button class="delete" on:click={() => openModalDelete(post.post_id)}>Xóa</button>
				</td>
			</tr>
		{/each}

        {#if showModalDelete}
			<div class="modal">
				<div class="modal-content delete-modal animate">
					<h3 class="warning-text">Bạn có chắc chắn muốn xóa bài viết?</h3>
					<div class="button-group">
						<button on:click={() => deletePost(select_post_id)} class="delete-btn"
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
						<label for="title">Tiêu đề:</label>
						<input
							type="text"
							id="title"
							bind:value={upPost.title}
							placeholder="Nhập tiêu đề"
						/>
					</div>
					<div class="input-wrapper">
						<label for="block_1">Nội dung 1</label>
						<input
							type="text"
							id="block_1"
							bind:value={upPost.block_1}
							placeholder="Nhập nội dung 1"
						/>
					</div>
                    <div class="input-wrapper">
						<label for="block_2">Nội dung 2</label>
						<input
							type="text"
							id="block_2"
							bind:value={upPost.block_2}
							placeholder="Nhập nội dung 2"
						/>
					</div>
                    <div class="input-wrapper">
                        <label for="block_3">Nội dung 3</label>
                        <input
                            type="text"
                            id="block_3"
                            bind:value={upPost.block_3}
                            placeholder="Nhập nội dung 3"
                        />
                    </div>
                    <div class="input-wrapper">
                        <label for="block_4">Nội dung 4</label>
                        <input
                            type="text"
                            id="block_4"
                            bind:value={upPost.block_4}
                            placeholder="Nhập nội dung 4"
                        />
                    </div>
                    <div class="input-wrapper">
                        <label for="block_5">Nội dung 5</label>
                        <input
                            type="text"
                            id="block_5"
                            bind:value={upPost.block_5}
                            placeholder="Nhập nội dung 5"
                        />
                    </div>
					<div class="button-group">
						<button on:click={() => updatePost(select_post_id)} class="submit-btn"
							>Cập nhật</button
						>
						<button on:click={closeModalUpdate} class="cancel-btn">Hủy</button>
					</div>
				</div>
			</div>
		{/if}
	</tbody>
</table>
