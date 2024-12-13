<script>
	import 'jquery/dist/jquery.slim.min.js';
    import 'bootstrap/dist/js/bootstrap.bundle.min.js';
</script>

<div class="admin-dashboard">
	<div class="admin-dashboard__menu">
		<div class="admin-dashboard__logo">
			<img src="/images/logo.png" alt="logo" />
		</div>
		<ul>
			<li><a href="/admin/manager/accounts">Account Manager</a></li>
			<li><a href="/admin/manager/airplanes">Airplane Manager</a></li>
			<li><a href="/admin/manager/flights">Flight Manager</a></li>
			<li><a href="/admin/manager/tickets">Ticket Manager</a></li>
		</ul>
	</div>
	<div class="admin-dashboard__content">
		<slot />
	</div>
</div>