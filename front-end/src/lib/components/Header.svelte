<script>
	import Icon from "@iconify/svelte";
</script>

<header class="header">
  <div class="container">
    <div class="header__logo">
      <a href="/">
        <img src="/images/logotd.png" alt="QAirline Logo" height="32px"/>
      </a>
    </div>
  
    <nav class="header__links">
      <a href="/explore">Khám phá</a>
      <a href="/booking">Đặt vé</a>
      <a href="/info">Thông tin hành trình</a>
      <a href="/club">Bamboo Club</a>
    </nav>
  
    <div class="header__auth">
      <!-- {#if isLoggedIn}
        <a href="/profile" class="user-icon">👤</a>
      {:else}
        <a href="/login" class="login">Đăng nhập</a> |
        <a href="/register" class="register">Đăng ký</a>
      {/if} -->
      <a href="/login" class="login">Đăng nhập</a> |
      <a href="/signup" class="register">Đăng ký</a>
      <Icon icon="codicon:account" style="font-size: 22px;"/>
    </div>
  </div>
</header>