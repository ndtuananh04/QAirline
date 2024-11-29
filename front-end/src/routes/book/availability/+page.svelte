<script>
	let flights = [
		{
			arrival: 'Thanh Hoa',
			arrival_hour_time: '15:00',
			code_arrival: 'THD',
			code_departure: 'HAN',
			departure: 'Ha Noi',
			departure_hour_time: '11:00',
			departure_time: '2024-11-28',
			flight_number: '123321QAL',
			seats: [
				{
					price: 100.0,
					seat_class: 'BUSINESS'
				},
				{
					price: 10.0,
					seat_class: 'ECONOMY'
				},
				{
					price: 50.0,
					seat_class: 'SKYBOSS'
				}
			],
			terminal: 1
		},
		{
			arrival: 'Thanh Hoa',
			arrival_hour_time: '15:00',
			code_arrival: 'THD',
			code_departure: 'HAN',
			departure: 'Ha Noi',
			departure_hour_time: '11:08',
			departure_time: '2024-11-28',
			flight_number: '123321QAL',
			seats: [
				{
					price: 100.0,
					seat_class: 'BUSINESS'
				},
				{
					price: 10.0,
					seat_class: 'ECONOMY'
				},
				{
					price: 50.0,
					seat_class: 'SKYBOSS'
				}
			],
			terminal: 1
		}
	];

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
									<h3>{flights[0].departure}</h3>
									<h4>{flights[0].code_departure}</h4>
								</div>
								<i class="fa-solid fa-arrow-right" style="font-size: 50px; "></i>
								<div class="city">
									<h3>{flights[0].arrival}</h3>
									<h4>{flights[0].code_arrival}</h4>
								</div>
							</div>
							<div class="time text-right">
								<i class="fa-solid fa-calendar-days" style="font-size: 30px;"></i>
								<p style="font-weight: 700; font-size: 20px;">{flights[0].departure_time}</p>
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
											<div class="flight__seat aligncenter {seat.seat_class.toLowerCase()}">
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
									<h3>{flights[0].arrival}</h3>
									<h4>{flights[0].code_arrival}</h4>
								</div>
								<i class="fa-solid fa-arrow-right" style="font-size: 50px; "></i>
								<div class="city">
									<h3>{flights[0].departure}</h3>
									<h4>{flights[0].code_departure}</h4>
								</div>
							</div>
							<div class="time text-right">
								<i class="fa-solid fa-calendar-days" style="font-size: 30px;"></i>
								<p style="font-weight: 700; font-size: 20px;">{flights[0].departure_time}</p>
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
											<div class="flight__seat aligncenter {seat.seat_class.toLowerCase()}">
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
					
				</div>
			</div>
		</div>
	</div>
</div>
