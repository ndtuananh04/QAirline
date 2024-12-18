<script>
	import HeaderAdmin from '$lib/components/HeaderAdmin.svelte';
	import Menu from '$lib/components/Menu.svelte';
</script>

<div class="admin-layout">
	<!-- Phần Header -->
	<div>
		<HeaderAdmin />
	</div>
	<!-- Phần Menu -->
	<Menu />
	<!-- Phần chứa biểu đồ -->
	<div class="chart-container">
		<slot />
	</div>
</div>
