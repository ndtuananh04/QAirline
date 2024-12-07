<script>
	import { onMount } from 'svelte';
	import { quantity, tripType } from '../../store';
	import { goto } from '$app/navigation';

	let flights = [];
	let flightsReturn = [];
	let departure = '';
	let arrival = '';
	let departureDate = '';
	let returnDate = '';
	let selectedDepartureSeat = null;
	let departurePrice = 0;
	let selectedReturnSeat = null;
	let returnPrice = 0;
	let vatDeparture = 0;
	let vatReturn = 0;
	let final_price = 0;

	onMount(() => {
		const params = new URLSearchParams(window.location.search);
		departure = params.get('fromInput');
		arrival = params.get('toInput');
		departureDate = params.get('departureDate');
		returnDate = params.get('returnDate');
		console.log(departure, arrival, departureDate, returnDate);
		fetchDeparture(departure, arrival, departureDate);
		if ($tripType === 'round-trip') {
			fetchReturn(arrival, departure, returnDate);
		}
	});

	async function fetchDeparture(departure, arrival, departureDate) {
		const payload = {
			departure: departure,
			arrival: arrival,
			departure_time: departureDate
		};

		try {
			const response = await fetch('http://localhost:5000/flights-search', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(payload)
			});

			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			const data = await response.json();
			flights = data;
			console.log(flights);
		} catch (error) {
			console.error('Error fetching flights:', error);
		}
	}

	async function fetchReturn(departure, arrival, departureDate) {
		const payload = {
			departure: departure,
			arrival: arrival,
			departure_time: departureDate
		};

		try {
			const response = await fetch('http://localhost:5000/flights-search', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(payload)
			});

			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			const data = await response.json();
			flightsReturn = data;
			console.log(flights);
		} catch (error) {
			console.error('Error fetching flights:', error);
		}
	}

	async function selectDepartureSeat(seat, flight_id) {
		selectedDepartureSeat = seat;
		try {
			const payload = {
				flight_id: flight_id,
				seat_class: seat.seat_class,
				price: seat.price,
				quantity: $quantity,
				trip_type: 'one-way'
			};

			const response = await fetch('http://localhost:5000/select-ticket', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload),
				credentials: 'include'
			});

			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			const data = await response.json();
			departurePrice = data.selected_ticket.total_price;
			vatDeparture = data.selected_ticket.vat;
		} catch (error) {
			console.error('Error selecting departure seat:', error);
		}
	}

	async function selectReturnSeat(seat, flight_id) {
		selectedReturnSeat = seat;
		try {
			const payload = {
				flight_id: flight_id,
				seat_class: seat.seat_class,
				price: seat.price,
				quantity: $quantity,
				trip_type: $tripType
			};

			const response = await fetch('http://localhost:5000/select-ticket', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload),
				credentials: 'include'
			});

			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			const data = await response.json();
			returnPrice = data.selected_ticket.total_price;
			vatReturn = data.selected_ticket.vat;
		} catch (error) {
			console.error('Error selecting return seat:', error);
		}
	}

	async function checkPromotion(code_promotion, total_price) {
		try {
			const payload = {
				code_promotion: code_promotion,
				total_price: total_price
			};

			const response = await fetch('http://localhost:5000/promotion-search', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload)
			});

			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			const data = await response.json();
			final_price = data.final_price;
		} catch (error) {
			console.error('Error selecting code promotion:', error);
		}
	}

	function goToTicketInfo() {
		goto('/user/book/ticketinfo');
	}

	function calculateDuration(departureTime, arrivalTime) {
		const [departureHours, departureMinutes] = departureTime.split(':').map(Number);
		const [arrivalHours, arrivalMinutes] = arrivalTime.split(':').map(Number);

		const departureDate = new Date();
		departureDate.setHours(departureHours, departureMinutes, 0, 0);

		const arrivalDate = new Date();
		arrivalDate.setHours(arrivalHours, arrivalMinutes, 0, 0);

		const durationMs = arrivalDate - departureDate;
		const durationMinutes = Math.floor(durationMs / 60000);
		const hours = Math.floor(durationMinutes / 60);
		const minutes = durationMinutes % 60;

		return `${hours} giờ ${minutes} phút`;
	}
</script>

<div class="flight">
	<div class="flight__header">
		<div class="container d-flex justify-content-between">
			<h2 class="flight__title">CHỌN CHUYẾN BAY</h2>
			<div class="flight__icon d-flex align-items-center">
				<i class="fas fa-plane"></i>
				<i class="fas fa-user"></i>
				<i class="fas fa-shopping-cart"></i>
				<i class="fas fa-dollar-sign"></i>
			</div>
		</div>
	</div>

	<div class="flight__main">
		<div class="container">
			<div class="divider d-flex">
				<div class="flight__info">
					<div class="flight__departure">
						<div class="flight__bar d-flex justify-content-between">
							<div class="location d-flex">
								<i class="fa-solid fa-plane-departure" style="font-size: 50px;"></i>
								<div class="city">
									<h3>{departure}</h3>
									<!-- <h4>{flights[0].code_departure}</h4> -->
								</div>
								<i class="fa-solid fa-arrow-right" style="font-size: 50px; "></i>
								<div class="city">
									<h3>{arrival}</h3>
									<!-- <h4>{flights[0].code_arrival}</h4> -->
								</div>
							</div>
							<div class="time text-right">
								<i class="fa-solid fa-calendar-days" style="font-size: 30px;"></i>
								<p style="font-weight: 700; font-size: 20px;">{departureDate}</p>
							</div>
						</div>
						{#if flights.length > 0}
							<div class="flight__list">
								{#each flights as flight}
									<div class="flight__item d-flex">
										<div class="flight__time d-flex">
											<div class="flight__time--exact aligncenter">
												<p class="code">{flight.flight_number}</p>
												<div class="d-flex">
													<div class="text-center">
														<h3>{flight.departure_hour_time}</h3>
														<p>{flight.code_departure}</p>
													</div>
													đến
													<div class="text-center">
														<h3>{flight.arrival_hour_time}</h3>
														<p>{flight.code_arrival}</p>
													</div>
												</div>
												<p class="code">Tên mb</p>
											</div>
											<div class="flight__time--total aligncenter">
												<p>Thời gian bay dự kiến:</p>
												<p>
													{calculateDuration(flight.departure_hour_time, flight.arrival_hour_time)}
												</p>
											</div>
										</div>
										<div class="flight__seats d-flex">
											{#each flight.seats as seat}
												<div
													class="flight__seat aligncenter {seat.seat_class.toLowerCase()} 
                                                {selectedDepartureSeat === seat ? 'selected' : ''}"
													on:click={() => selectDepartureSeat(seat, flight.flight_id)}
												>
													<div class="flight__seat--class">
														<b>{seat.seat_class}</b>
													</div>
													<div class="flight__seat--price">
														<b>{seat.price}</b>
													</div>
												</div>
											{/each}
										</div>
									</div>
								{/each}
							</div>
						{:else}
							<div class="flight__out">
								<h3>Không có chuyến bay nào trong thời gian này</h3>
							</div>
						{/if}
					</div>
					{#if $tripType === 'round-trip'}
						<div class="flight__return">
							<div class="flight__bar d-flex justify-content-between">
								<div class="location d-flex">
									<i class="fa-solid fa-plane-departure fa-flip-horizontal" style="font-size: 50px;"
									></i>
									<div class="city">
										<h3>{arrival}</h3>
										<!-- <h4>{flights[0].code_arrival}</h4> -->
									</div>
									<i class="fa-solid fa-arrow-right" style="font-size: 50px; "></i>
									<div class="city">
										<h3>{departure}</h3>
										<!-- <h4>{flights[0].code_departure}</h4> -->
									</div>
								</div>
								<div class="time text-right">
									<i class="fa-solid fa-calendar-days" style="font-size: 30px;"></i>
									<p style="font-weight: 700; font-size: 20px;">{returnDate}</p>
								</div>
							</div>
							{#if flightsReturn.length > 0}
								<div class="flight__list">
									{#each flightsReturn as flight}
										<div class="flight__item d-flex">
											<div class="flight__time d-flex">
												<div class="flight__time--exact aligncenter">
													<p class="code">{flight.flight_number}</p>
													<div class="d-flex">
														<div class="text-center">
															<h3>{flight.departure_hour_time}</h3>
															<p>{flight.code_departure}</p>
														</div>
														đến
														<div class="text-center">
															<h3>{flight.arrival_hour_time}</h3>
															<p>{flight.code_arrival}</p>
														</div>
													</div>
													<p class="code">Tên mb</p>
												</div>
												<div class="flight__time--total aligncenter">
													<p>Thời gian bay dự kiến:</p>
													<p>
														{calculateDuration(
															flight.departure_hour_time,
															flight.arrival_hour_time
														)}
													</p>
												</div>
											</div>
											<div class="flight__seats d-flex">
												{#each flight.seats as seat, index}
													<div
														class="flight__seat aligncenter {seat.seat_class.toLowerCase()}
														{selectedReturnSeat === seat ? 'selected' : ''}"
														on:click={() => selectReturnSeat(seat, flight.flight_id)}
													>
														<div class="flight__seat--class">
															<b>{seat.seat_class}</b>
														</div>
														<div class="flight__seat--price">
															<b>{seat.price}</b>
														</div>
													</div>
												{/each}
											</div>
										</div>
									{/each}
								</div>
							{:else}
								<div class="flight__out">
									<h3>Không có chuyến bay nào trong thời gian này</h3>
								</div>
							{/if}
						</div>
					{/if}
				</div>
				<div class="flight__aside">
					<div class="flight__aheader">
						<h3>Thông tin đặt vé</h3>
					</div>
					<div class="flight__price d-flex justify-content-between">
						<p>Chuyến đi</p>
						<p>{departurePrice}</p>
					</div>
					<div class="flight__price d-flex justify-content-between">
						<p>VAT</p>
						<p>{vatDeparture}</p>
					</div>
					{#if $tripType === 'round-trip'}
						<div class="flight__price d-flex justify-content-between">
							<p>Chuyến về</p>
							<p>{returnPrice}</p>
						</div>
						<div class="flight__price d-flex justify-content-between">
							<p>VAT</p>
							<p>{vatReturn}</p>
						</div>
					{/if}
					<div class="flight__price d-flex justify-content-between">
						<p>Tổng tiền</p>
						<p>{departurePrice + returnPrice - vatDeparture - vatReturn}</p>
					</div>
					<div class="flight__price d-flex justify-content-between">
						<p>Khuyến Mại</p>
						<input type="text" class="form-control" placeholder="" />
					</div>
					<div class="flight__button">
						<button class="btn btn-primary" on:click={goToTicketInfo}>Đi tiếp</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
