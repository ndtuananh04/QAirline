<script>
	import FooterAdmin from '../../../lib/components/FooterAdmin.svelte';
</script>

<div class="sign-background">
	<slot />
</div>
<FooterAdmin />

<style>
	.sign-background {
		background-image: url('/images/signup-background.jpg');
		background-size: cover;
		background-position: center;
		background-repeat: no-repeat;
	}

	
</style>

