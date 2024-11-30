<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { writable, get } from 'svelte/store';
	import '@splidejs/splide/dist/css/splide.min.css';
	import Splide from '@splidejs/splide';

	let splideElement;
	let splideInstance;
	let showHiddenForm = false;
	let departures = writable([]);
	let arrivals = writable([]);
	let fromInput = '';
	let toInput = '';
	let tripType = 'round-trip';
	let departureDate = '';
	let returnDate = '';
	let showDepartureSuggestions = false;
	let showArrivalSuggestions = false;
	let filteredDepartures = writable([]);
	let filteredArrivals = writable([]);

	onMount(() => {
		splideInstance = new Splide(splideElement, {
			type: 'loop',
			autoplay: true,
			interval: 5000,
			arrows: false,
			pagination: true
		}).mount();

		document.addEventListener('click', handleClickOutside);
	});

	onMount(async () => {
		const response = await fetch('http://127.0.0.1:5000/departure-arrival');
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
		</div>

		<div class="booking-form" on:click={toggleHiddenForm}>
			<form method="GET" action="/user/book/availability">
				<div class="booking__basic row">
					<div class="trip-type col-12 col-md-4">
						<label
							><input type="radio" name="tripType" value="one-way" bind:group={tripType} /> Một chiều</label
						>
						<label
							><input
								type="radio"
								name="tripType"
								value="round-trip"
								checked
								bind:group={tripType}
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
								type="date"
								id="departure"
								name="departureDate"
								bind:value={departureDate}
								required
							/>
						</div>
						{#if tripType === 'round-trip'}
							<div class="form-group col-12 col-md-4">
								<label for="return-date">Ngày về</label>
								<input
									type="date"
									id="return-date"
									name="returnDate"
									bind:value={returnDate}
									required
								/>
							</div>
						{/if}
						<div class="form-group col-12 col-md-4">
							<label for="passengers">Số người</label>
							<input type="number" id="passengers" value="1" />
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

<section class="news">
	<div class="container">
		<div class="padding-tb">
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
							Thai Airways International and Thai-Chinese Chamber of Commerce have signed a
							Memorandum of Understanding...
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
						<h3 class="news__item-title">
							THAI Operates as Usual While Implementing Reform Plan...
						</h3>
						<p class="news__description">
							Mr. Chakrit Parapuntakul, Second Vice Chairman of the Board of Directors of Thai
							Airways International...
						</p>
						<span class="news__date">19 May 2020</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>
