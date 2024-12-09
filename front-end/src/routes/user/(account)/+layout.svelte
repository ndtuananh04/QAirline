<script>
	import Icon from "@iconify/svelte";
  import Footer from '$lib/components/Footer.svelte';
</script>

<header class="header">
  <div class="container">
    <div class="header__logo">
      <a href="/">
        <img src="/images/logo.png" alt="QAirline Logo" height="50px"/>
      </a>
    </div>
    <div class="header__auth">
      <!-- {#if isLoggedIn}
        <a href="/profile" class="user-icon">👤</a>
      {:else}
        <a href="/login" class="login">Đăng nhập</a> |
        <a href="/register" class="register">Đăng ký</a>
      {/if} -->
      <a href="/user/login" class="login">Đăng nhập</a> |
      <a href="/user/signup" class="register">Đăng ký</a>
      <Icon icon="codicon:account" style="font-size: 22px;"/>
    </div>
  </div>
</header>
<slot />
<Footer />
