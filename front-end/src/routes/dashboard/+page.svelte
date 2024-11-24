<script>
	import { onMount } from 'svelte';
	import '@splidejs/splide/dist/css/splide.min.css';
	import Splide from '@splidejs/splide';

	let splideElement;
	let splideInstance;

	onMount(() => {
		splideInstance = new Splide(splideElement, {
			type: 'loop',
			autoplay: true,
			interval: 5000,
			arrows: false,
			pagination: true
		}).mount();
	});
</script>

<div class="slick">
	<div class="splide" bind:this={splideElement}>
		<div class="splide__track">
			<ul class="splide__list">
				<li class="splide__slide" style="background-image: url('/images/cau.jpg');"></li>
				<li class="splide__slide" style="background-image: url('/images/vinhhalong.jpg');"></li>
				<li class="splide__slide" style="background-image: url('/images/ruongbacthang.jpg');"></li>
			</ul>
		</div>
	</div>
	<div class="slick__heading">
		<h1>Khám Phá Việt Nam - Vẻ Đẹp Bất Tận</h1>
	</div>
	<div class="slick__form">
		<div class="booking-tabs">
			<button class="active">Đặt Vé</button>
			<button>Làm Thủ Tục</button>
			<button>Đặt Chỗ Của Tôi</button>
		</div>

		<div class="booking-form">
			<form>
				<div class="trip-type">
					<label><input type="radio" name="trip" value="one-way" /> Một chiều</label>
					<label><input type="radio" name="trip" value="round-trip" checked /> Khứ hồi</label>
				</div>

				<div class="form-group">
					<label for="from">Từ</label>
					<input type="text" id="from" value="Hà Nội (HAN)" />
				</div>
				<div class="form-group">
					<label for="to">Tới</label>
					<input type="text" id="to" value="TP. Hồ Chí Minh (SGN)" />
				</div>
				<div class="form-group">
					<label for="departure">Ngày đi</label>
					<input type="date" id="departure" />
				</div>
				<div class="form-group">
					<label for="return">Ngày về</label>
					<input type="date" id="return" />
				</div>
				<div class="form-group">
					<label for="passengers">Hành khách</label>
					<input type="number" id="passengers" value="1" />
				</div>
				<div class="form-group">
					<button type="submit" class="search-button">Tìm Chuyến Bay</button>
				</div>
			</form>
		</div>
	</div>
</div>

<section class="news">
	<div class="news__header">
		<h2 class="news__title">Tin Tức và Thông Báo</h2>
		<button class="news__view-all">View All</button>
	</div>
	<div class="news__list">
		<div class="news__item">
			<img class="news__image" src="image1.jpg" alt="Tin tức 1" />
			<div class="news__content">
				<h3 class="news__item-title">The 16th World Chinese Entrepreneurs Convention (WCEC)</h3>
				<p class="news__description">
					Thai Airways International and Thai-Chinese Chamber of Commerce have signed a Memorandum
					of Understanding...
				</p>
				<span class="news__date">24 April 2023</span>
			</div>
		</div>
		<div class="news__item">
			<img class="news__image" src="image2.jpg" alt="Tin tức 2" />
			<div class="news__content">
				<h3 class="news__item-title">
					The Central Bankruptcy Court granted THAI’s business reorganization petition...
				</h3>
				<p class="news__description">
					Mr. Chansin Treenuchagron, Director and Acting President of Thai Airways International
					Public Company...
				</p>
				<span class="news__date">14 September 2020</span>
			</div>
		</div>
		<div class="news__item">
			<img class="news__image" src="image3.jpg" alt="Tin tức 3" />
			<div class="news__content">
				<h3 class="news__item-title">THAI Operates as Usual While Implementing Reform Plan...</h3>
				<p class="news__description">
					Mr. Chakrit Parapuntakul, Second Vice Chairman of the Board of Directors of Thai Airways
					International...
				</p>
				<span class="news__date">19 May 2020</span>
			</div>
		</div>
	</div>
</section>
