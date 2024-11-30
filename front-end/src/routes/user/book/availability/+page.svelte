<script>
	import { onMount } from 'svelte';

	let flights = [];
	let flightsReturn = [];
	let departure = '';
	let arrival = '';
	let departureDate = '';
	let returnDate = '';

	onMount(() => {
		const params = new URLSearchParams(window.location.search);
		const tripType = params.get('tripType');
		departure = params.get('fromInput');
		arrival = params.get('toInput');
		departureDate = params.get('departureDate');
		returnDate = params.get('returnDate');
		console.log(departure, arrival, departureDate, returnDate);
		fetchDeparture(departure, arrival, departureDate);
		fetchReturn(arrival, departure, returnDate);
	});

	async function fetchDeparture(departure, arrival, departureDate) {
		const payload = {
			departure: departure,
			arrival: arrival,
			departure_time: departureDate
		};

		try {
			const response = await fetch('http://127.0.0.1:5000/flights-search', {
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
			console.log(flightss);
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
			const response = await fetch('http://127.0.0.1:5000/flights-search', {
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
			console.log(flightss);
		} catch (error) {
			console.error('Error fetching flights:', error);
		}
	}

	let selectedDepartureSeat = null;
	let departurePrice = 0;
	let selectedReturnSeat = null;
	let returnPrice = 0;

	// Function to handle selecting a seat
	function selectDepartureSeat(seat) {
		selectedDepartureSeat = seat;
		departurePrice = seat.price;
	}

	function selectReturnSeat(seat) {
		selectedReturnSeat = seat;
		returnPrice = seat.price;
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
												on:click={() => selectDepartureSeat(seat)}
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
					</div>

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
												{calculateDuration(flight.departure_hour_time, flight.arrival_hour_time)}
											</p>
										</div>
									</div>
									<div class="flight__seats d-flex">
										{#each flight.seats as seat, index}
											<div
												class="flight__seat aligncenter {seat.seat_class.toLowerCase()}
												{selectedReturnSeat === seat ? 'selected' : ''}"
												on:click={() => selectReturnSeat(seat)}
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
					</div>
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
						<p>Chuyến về</p>
						<p>{returnPrice}</p>
					</div>
					<div class="flight__price d-flex justify-content-between">
						<p>Tổng tiền</p>
						<p>{departurePrice + returnPrice}</p>
					</div>
					<div class="flight__button">
						<button class="btn btn-primary">Đi tiếp</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
