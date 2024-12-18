<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	export async function handle({ event, resolve }) {
		const token = localStorage.getItem('jwt');

		// Kiểm tra nếu người dùng truy cập vào các route yêu cầu đăng nhập
		if (event.url.pathname.startsWith('/admin') && !token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập!');
			goto('/user/login'); // Chuyển hướng tới trang đăng nhập
			return;
		}

		return resolve(event);
	}

	onMount(() => {
		const token = localStorage.getItem('jwt');
		if (!token) {
			alert('Bạn chưa đăng nhập. Vui lòng đăng nhập!');
			goto('/user/login'); // Điều hướng tới trang đăng nhập
		}
	});
</script>

<h1>Trang quản trị</h1>
<p>Chào mừng bạn đến với trang admin/dashboard.</p>
