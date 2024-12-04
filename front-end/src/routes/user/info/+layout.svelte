<script>
	import Footer from '$lib/components/Footer.svelte';
	import Header from '$lib/components/Header.svelte';
</script>

<div class="info-background">
	<Header />
	<slot />
	<Footer />
</div>
