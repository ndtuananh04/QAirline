<script>
	import { onMount, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { writable, get } from 'svelte/store';
	import '@splidejs/splide/dist/css/splide.min.css';
	import Splide from '@splidejs/splide';
	import { quantity, tripType } from '../store';
	import flatpickr from 'flatpickr';
	import 'flatpickr/dist/flatpickr.min.css';

	let splideElement1;
	let splideElement2;
	let splideElement3;
	let showHiddenForm = false;
	let departures = writable([]);
	let arrivals = writable([]);
	let fromInput = '';
	let toInput = '';
	let departureDatePicker;
	let returnDatePicker;
	let departureDate = '';
	let returnDate = '';
	let showDepartureSuggestions = false;
	let showArrivalSuggestions = false;
	let filteredDepartures = writable([]);
	let filteredArrivals = writable([]);
	let localQuantity = 1;

	let posts = []; // Dữ liệu tin tức
	let delayedFlights = writable([]); // Dữ liệu chuyến bay bị delay

	let showModal = false; // Hiển thị modal
	let selectedPost = null; // Dữ liệu bài viết được chọn

	const imageList = [
		'/images/airplane1.jpg',
		'/images/airplane2.jpg',
		'/images/airplane3.jpg',
		'/images/airplane4.jpg',
		'/images/airplane5.jpg',
		'/images/airplane6.jpg'
	];

	// Gọi API để lấy thông tin tin tức
	async function fetchPosts() {
		try {
			const response = await fetch('http://localhost:5000/post-customer');
			if (response.ok) {
				const data = await response.json();
				posts = data.map((post) => ({
					...post,
					image_url: getRandomImage() // Gán ảnh ngẫu nhiên
				}));
				await tick();
				initializeSplide();
				console.log('Posts loaded:', posts); // Debug
			} else {
				console.error('Failed to fetch posts:', response.status);
			}
		} catch (error) {
			console.error('Error loading posts:', error);
		}
	}

	async function fetchDelayedFlights() {
		try {
			const response = await fetch('http://localhost:5000/flights-delay');
			if (response.ok) {
				const data = await response.json();
				delayedFlights.set(data);
				await tick();
				initializeSplideDelay();
				console.log('Delayed flights loaded:', data);
			} else {
				console.error('Failed to fetch delayed flights:', response.status);
			}
		} catch (error) {
			console.error('Error loading delayed flights:', error);
		}
	}

	// Hàm gọi API lấy chi tiết bài viết
	async function fetchPostDetail(post_id) {
		try {
			console.log('Fetching post detail for ID:', post_id); // Debug
			const response = await fetch(`http://localhost:5000/post-detail/${post_id}`);
			if (response.ok) {
				const data = await response.json();
				console.log('Post detail fetched:', data); // Debug
				selectedPost = data; // Lưu thông tin bài viết chi tiết
				showModal = true; // Hiển thị modal
			} else {
				console.error('Failed to fetch post detail:', response.status);
			}
		} catch (error) {
			console.error('Error loading post detail:', error);
		}
	}
	let currentIndex = 0;
	// Hàm chọn ảnh ngẫu nhiên
	function getRandomImage() {
		const image = imageList[currentIndex];
		currentIndex = (currentIndex + 1) % imageList.length;
		return image;
	}

	const initializeSplide = () => {
		const splideInstance = new Splide(splideElement1, {
			type: 'loop',
			autoplay: true,
			interval: 5000,
			speed: 1500,
			easing: 'ease',
			arrows: false,
			pagination: true,
			pauseOnHover: false,
			pauseOnFocus: false
		}).mount();

		const splidePost = new Splide(splideElement2, {
			type: 'loop',
			autoplay: true,
			interval: 4000,
			speed: 1500,
			easing: 'ease',
			arrows: true,
			pagination: false,
			pauseOnHover: false,
			pauseOnFocus: false,
			perPage: 3,
			perMove: 1,
			gap: '12px',
			breakpoints: {
				1200: {
					perPage: 2,
					gap: '8px'
				},
				768: {
					perPage: 1,
					gap: '5px'
				}
			}
		}).mount();
	};

	const initializeSplideDelay = () => {
		console.log('splide');
		const splideDelay = new Splide(splideElement3, {
			type: 'loop',
			autoplay: true,
			interval: 4000,
			speed: 1500,
			pagination: false,
			easing: 'ease',
			arrows: false,
			direction: 'ttb', // Thiết lập trượt dọc
			height: '100px',
			perPage: 1, // Số lượng phần tử hiển thị cùng lúc
			gap: '10px'
		}).mount();

		let isScrolling = false;

		splideElement3.addEventListener('wheel', (event) => {
			event.preventDefault(); // Ngăn chặn hành vi mặc định của sự kiện cuộn

			if (!isScrolling) {
				isScrolling = true;
				requestAnimationFrame(() => {
					if (event.deltaY > 0) {
						splideDelay.go('>');
					} else {
						splideDelay.go('<');
					}
					isScrolling = false;
				});
			}
		});
	};

	let formattedDepartureDate = '';
	let formattedReturnDate = '';
	let dpInstance;
	let returnInstance;
	const initializeDatePickers = () => {
		if (departureDatePicker) {
			dpInstance = flatpickr(departureDatePicker, {
				dateFormat: 'd/m/Y',
				altFormat: 'Y-m-d',
				minDate: 'today',
				onChange: function (selectedDates) {
					if (selectedDates[0]) {
						const date = selectedDates[0];
						formattedDepartureDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
						if (returnInstance) {
							returnInstance.set('minDate', date);
						}
					}
				}
			});
		}

		if (returnDatePicker) {
			console.log('dpIN',dpInstance);
			returnInstance = flatpickr(returnDatePicker, {
				dateFormat: 'd/m/Y',
				altFormat: 'Y-m-d',
				minDate: 'today',
				onChange: function (selectedDates) {
					if (selectedDates[0]) {
						const date = selectedDates[0];
						formattedReturnDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
					}
				}
			});
		}
	};

	onMount(() => {
		initializeDatePickers();
		fetchDelayedFlights();
		fetchPosts();
	});

	function closeModal() {
		showModal = false;
	}

	onMount(() => {
		document.addEventListener('click', handleClickOutside);
	});

	onMount(async () => {
		const response = await fetch('http://localhost:5000/departure-arrival');
		const data = await response.json();
		departures.set(data.departure);
		arrivals.set(data.arrival);
	});

	function removeDiacritics(str) {
		return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
	}

	function suggest(input, suggestions) {
		const value = removeDiacritics(input.toLowerCase());
		const suggestionsArray = get(suggestions);
		const filteredSuggestions = suggestionsArray.filter((suggestion) => {
			const normalizedSuggestion = removeDiacritics(suggestion.toLowerCase());
			return normalizedSuggestion.includes(value);
		});
		return filteredSuggestions;
	}

	function handleFromInput(event) {
		fromInput = event.target.value;
		filteredDepartures.set(suggest(fromInput, departures));
		showDepartureSuggestions = true;
	}

	function handleToInput(event) {
		toInput = event.target.value;
		filteredArrivals.set(suggest(toInput, arrivals));
		showArrivalSuggestions = true;
	}

	function selectDeparture(suggestion, event) {
		event.stopPropagation();
		fromInput = suggestion;
		showDepartureSuggestions = false;
	}

	function selectArrival(suggestion, event) {
		event.stopPropagation();
		toInput = suggestion;
		showArrivalSuggestions = false;
	}

	function handleClickOutside(event) {
		const form = document.querySelector('.booking-form');
		if (form && !form.contains(event.target)) {
			showHiddenForm = false;
			showDepartureSuggestions = false;
			showArrivalSuggestions = false;
		}
	}

	function toggleHiddenForm() {
		showHiddenForm = true;
	}
</script>

<div class="slick">
	<div class="blur {showHiddenForm ? 'show' : 'd-none'}"></div>
	<div class="splide splide--1" bind:this={splideElement1}>
		<div class="splide__track">
			<ul class="splide__list">
				<li
					class="splide__slide splide__slide--1"
					style="background-image: url('/images/cau.jpg');"
				></li>
				<li
					class="splide__slide splide__slide--1"
					style="background-image: url('/images/vinhhalong.jpg');"
				></li>
				<li
					class="splide__slide splide__slide--1"
					style="background-image: url('/images/ruongbacthang.jpg');"
				></li>
			</ul>
		</div>
	</div>
	<div class="slick__heading">
		<h1>Khám Phá Việt Nam - Vẻ Đẹp Bất Tận</h1>
	</div>
	<div class="slick__form">
		<div class="booking-tabs">
			<button class="active">Đặt Vé</button>
		</div>

		<div class="booking-form" on:click={toggleHiddenForm}>
			<form method="GET" action="/user/book/availability">
				<div class="booking__basic row">
					<div class="trip-type col-12 col-md-4">
						<label
							><input type="radio" name="tripType" value="one-way" bind:group={$tripType} /> Một chiều</label
						>
						<label
							><input
								type="radio"
								name="tripType"
								value="round-trip"
								checked
								bind:group={$tripType}
							/> Khứ hồi</label
						>
					</div>
					<div class="form-group col-12 col-md-4 suggested">
						<label for="from">Điểm đi</label>
						<input
							type="text"
							id="from"
							name="fromInput"
							bind:value={fromInput}
							on:input={handleFromInput}
							required
						/>
						{#if fromInput && showDepartureSuggestions && $filteredDepartures.length > 0}
							<ul class="suggestions">
								{#each $filteredDepartures as suggestion}
									<li on:click={(event) => selectDeparture(suggestion, event)}>{suggestion}</li>
								{/each}
							</ul>
						{/if}
					</div>
					<div class="form-group col-12 col-md-4 suggested">
						<label for="to">Điểm đến</label>
						<input
							type="text"
							id="to"
							name="toInput"
							bind:value={toInput}
							on:input={handleToInput}
							required
						/>
						{#if toInput && showArrivalSuggestions && $filteredArrivals.length > 0}
							<ul class="suggestions">
								{#each $filteredArrivals as suggestion}
									<li on:click={(event) => selectArrival(suggestion, event)}>{suggestion}</li>
								{/each}
							</ul>
						{/if}
					</div>
				</div>
				<div class="booking__hiden {showHiddenForm ? 'show' : 'hiden'}">
					<div class="row">
						<div class="form-group col-12 col-md-4">
							<label for="departure">Ngày đi</label>
							<input
								type="text"
								id="departure"
								bind:this={departureDatePicker}
								placeholder="Chọn ngày đi"
								required
							/>
							<input type="hidden" name="departureDate" value={formattedDepartureDate} />
						</div>
						{#if $tripType === 'round-trip'}
							<div class="form-group col-12 col-md-4">
								<label for="return-date">Ngày về</label>
								<input
									type="text"
									id="return-date"
									bind:this={returnDatePicker}
									placeholder="Chọn ngày về"
									required
								/>
								<input type="hidden" name="returnDate" value={formattedReturnDate} />
							</div>
						{/if}
						<div class="form-group col-12 col-md-4">
							<label for="quantity">Số người</label>
							<input
								type="number"
								id="quantity"
								name="quantity"
								bind:value={localQuantity}
								on:change={() => quantity.set(localQuantity)}
								required
							/>
						</div>
					</div>
					<div class="form-group submit">
						<button type="submit" class="search-button">Tìm Chuyến Bay</button>
					</div>
				</div>
			</form>
		</div>
	</div>
</div>

<div class="delayed-flights">
	<h2 class="delayed-flights__header">Thông Báo Chuyến Bay Bị Hoãn</h2>
	<div bind:this={splideElement3} class="splide splide-delayed-flights">
		<div class="splide__track delayed-flights__track">
			<ul class="splide__list delayed-flights__list">
				{#if $delayedFlights.length === 0}
					<li class="splide__slide delayed-flights__item">Không có chuyến bay nào bị hoãn.</li>
				{:else}
					{#each $delayedFlights as flight}
						<li class="splide__slide delayed-flights__item">
							<p>
								<strong>Chuyến bay:</strong>
								{flight.flight_number} <br />
								<strong>Hành trình:</strong>
								{flight.departure} - {flight.arrival} <br />
								<strong>Thời gian mới:</strong>
								{flight.departure_time} khởi hành lúc {flight.departure_hour_time}
							</p>
						</li>
					{/each}
				{/if}
			</ul>
		</div>
	</div>
</div>

<section id="news-section" class="news">
	<div class="container">
		<div class="news__header">
			<h2 class="news__title">Tin Tức và Thông Báo</h2>
			<button class="news__view-all">Xem thêm</button>
		</div>
		<div bind:this={splideElement2} class="splide splide-news">
			<div class="splide__track">
				<ul class="splide__list">
					{#if posts.length === 0}
						<li class="splide__slide">Đang tải...</li>
					{:else}
						{#each posts as post}
							<li class="splide__slide news__item" on:click={() => fetchPostDetail(post.post_id)}>
								<img
									class="news__image"
									src={post.image_url || 'https://via.placeholder.com/150'}
									alt="anh"
								/>
								<div class="news__content">
									<h3 class="news__item-title">{post.title}</h3>
									<p class="news__description">{post.block_1 || 'Không có mô tả'}</p>
									<span class="news__date">{post.post_date || 'Ngày không xác định'}</span>
								</div>
							</li>
						{/each}
					{/if}
				</ul>
			</div>
		</div>
	</div>

	<!-- Modal -->
	{#if showModal}
		<div class="modal" on:click={closeModal}>
			<div class="modal__content" on:click|stopPropagation>
				<button class="modal__close" on:click|stopPropagation={closeModal}>×</button>
				<h2>{selectedPost.title}</h2>
				<p>{selectedPost.block_1}</p>
				<p>{selectedPost.block_2}</p>
				<p>{selectedPost.block_3}</p>
				<p>{selectedPost.block_4}</p>
				<p>{selectedPost.block_5}</p>
				<p>{selectedPost.post_date}</p>
			</div>
		</div>
	{/if}
</section>

<style>
	.modal {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		display: flex; /* Căn chỉnh chính giữa */
		justify-content: center; /* Căn giữa theo chiều ngang */
		align-items: center; /* Căn giữa theo chiều dọc */
		z-index: 999;
	}

	.modal__content {
		background: white;
		padding: 20px;
		border-radius: 10px;
		width: 900px; /* Kích thước cố định chiều rộng */
		height: 600px; /* Kích thước cố định chiều cao */
		position: relative;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
		overflow-y: auto; /* Bật cuộn nếu nội dung quá dài */
		word-wrap: break-word; /* Đảm bảo từ dài sẽ xuống dòng */
	}

	.modal__content h2 {
		font-size: 24px; /* Tăng kích thước tiêu đề */
		font-weight: bold;
		margin-bottom: 20px;
		text-align: center; /* Căn giữa tiêu đề */
		color: #333; /* Màu sắc tiêu đề */
	}

	.modal__content p {
		font-size: 16px; /* Giữ nội dung ở kích thước trung bình */
		line-height: 1.5;
		color: #555;
		margin-bottom: 10px;
		white-space: normal; /* Đảm bảo nội dung sẽ xuống dòng khi cần thiết */
		word-wrap: break-word; /* Đảm bảo từ dài sẽ xuống dòng */
	}

	.modal__content p:last-child {
		font-size: 14px; /* Giảm kích thước cho ngày tháng */
		font-style: italic;
		color: #777; /* Màu sắc nhạt hơn cho ngày tháng */
		text-align: right; /* Căn phải ngày tháng */
		margin-top: 20px;
	}

	.modal__close {
		position: absolute;
		top: 10px;
		right: 10px;
		background: none;
		border: none;
		font-size: 20px;
		cursor: pointer;
	}
</style>
