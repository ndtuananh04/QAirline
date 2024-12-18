<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let postsss = [];
	let error = '';

	// Hàm gọi API để lấy danh sách bài viết
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
				console.log(postsss); // Kiểm tra dữ liệu trả về (chỉ có post_id và title)
			} else {
				const err = await response.json();
				error = err.msg || 'Lỗi khi lấy danh sách bài viết';
			}
		} catch (err) {
			console.error('Lỗi khi lấy danh sách bài viết:', err);
			error = 'Đã xảy ra lỗi khi lấy danh sách bài viết.';
		}
	};
	// Gọi hàm fetchPostAdmin khi trang được tải lên
	onMount(() => {
		fetchPostAdmin();
	});
</script>

<div class="header-container">
	<div class="add-account-container">
		<button class="btn-add-admin">Thêm bài viết</button>
	</div>
</div>

{#if error}
	<p class="error">{error}</p>
	<!-- Hiển thị lỗi nếu có -->
{/if}

<table class="table-post">
	<thead>
		<tr>
			<th scope="col" class="sortable-header">ID</th>
			<th scope="col" class="sortable-header">Tiêu đề</th>
		</tr>
	</thead>
	<tbody>
		{#each postsss as post}
			<tr>
				<td>{post.post_id}</td>
				<td>{post.title}</td>
			</tr>
		{/each}
	</tbody>
</table>
