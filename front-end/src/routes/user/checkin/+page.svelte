<script>
	let showPlane = false;
	let ticket_number = '';
	let phone_number = '';
	let selectedSeat = null;

	async function handleSubmit() {
		const response = await fetch('http://localhost:5000/checkin', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				ticket_number: ticket_number,
				phone_number: phone_number
			}),
			credentials: 'include'
		});

		if (response.ok) {
			showPlane = true;
			alert('Thông tin đúng, bạn vui lòng chọn chỗ');
		} else {
			const data = await response.json();
			alert(data.msg);
			showPlane = false; // Không hiển thị phần tiếp theo
		}
	}

	// Hàm xử lý chọn ghế
	function handleSeatSelect(seat_number) {
		if (selectedSeat === seat_number) {
			selectedSeat = null; // Bỏ chọn ghế
		} else {
			selectedSeat = seat_number; // Chọn ghế mới
		}
	}

	async function handleSelectSeat() {
		if (!selectedSeat) {
			alert('Bạn chưa chọn ghế');
			return;
		}

		const response = await fetch('http://localhost:5000/seats-airplane', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				seat_number: selectedSeat
			}),
			credentials: 'include'
		});

		if (response.ok) {
			alert('Chọn ghế thành công');
		} else {
			const data = await response.json();
			alert(data.msg);
		}
	}
</script>

<div class="containerr">
	<div class="checkin-form">
		<p class="info-text">Quý khách điền đầy đủ thông tin để làm thủ tục check-in trực tuyến</p>
		<form class="form" on:submit|preventDefault={handleSubmit}>
			<div class="form-group">
				<div class="input-group">
					<label for="ticket_number">Số vé</label>
					<input
						type="text"
						id="ticket_number"
						name="ticket_number"
						placeholder="Nhập số vé"
						bind:value={ticket_number}
						required
					/>
				</div>
				<div class="input-group">
					<label for="phone_number">Số điện thoại</label>
					<input
						type="text"
						id="phone_number"
						name="phone_number"
						placeholder="Nhập số điện thoại"
						bind:value={phone_number}
						required
					/>
				</div>
			</div>
			<button type="submit" class="submit-button">
				{#if showPlane}
					CHỌN GHẾ
				{:else}
					LÀM THỦ TỤC
				{/if}
			</button>
		</form>
	</div>

	{#if showPlane}
		<div class="plane">
			<div class="cockpit">
				<h1>QAirline</h1>
			</div>
			<div class="exit exit--front fuselage"></div>
			<ol class="cabin fuselage">
				<li class="row row--1">
					<ol class="seats" type="A">
						<li class="seat">
							<input
								type="checkbox"
								id="1A"
								checked={selectedSeat === '1A'}
								on:change={() => handleSeatSelect('1A')}
							/>
							<label for="1A">1A</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="1B"
								checked={selectedSeat === '1B'}
								on:change={() => handleSeatSelect('1B')}
							/>
							<label for="1B">1B</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="1C"
								checked={selectedSeat === '1C'}
								on:change={() => handleSeatSelect('1C')}
							/>
							<label for="1C">1C</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="1D"
								checked={selectedSeat === '1D'}
								on:change={() => handleSeatSelect('1D')}
							/>
							<label for="1D">1D</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="1E"
								checked={selectedSeat === '1E'}
								on:change={() => handleSeatSelect('1E')}
							/>
							<label for="1E">1E</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="1F"
								checked={selectedSeat === '1F'}
								on:change={() => handleSeatSelect('1F')}
							/>
							<label for="1F">1F</label>
						</li>
					</ol>
				</li>
				<li class="row row--2">
					<ol class="seats" type="A">
						<li class="seat">
							<input
								type="checkbox"
								id="2A"
								checked={selectedSeat === '2A'}
								on:change={() => handleSeatSelect('2A')}
							/><label for="2A">2A</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="2B"
								checked={selectedSeat === '2B'}
								on:change={() => handleSeatSelect('2B')}
							/><label for="2B">2B</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="2C"
								checked={selectedSeat === '2C'}
								on:change={() => handleSeatSelect('2C')}
							/><label for="2C">2C</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="2D"
								checked={selectedSeat === '2D'}
								on:change={() => handleSeatSelect('2D')}
							/><label for="2D">2D</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="2E"
								checked={selectedSeat === '2E'}
								on:change={() => handleSeatSelect('2E')}
							/><label for="2E">2E</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="2F"
								checked={selectedSeat === '2F'}
								on:change={() => handleSeatSelect('2F')}
							/><label for="2F">2F</label>
						</li>
					</ol>
				</li>
				<li class="row row--3">
					<ol class="seats" type="A">
						<li class="seat">
							<input
								type="checkbox"
								id="3A"
								checked={selectedSeat === '3A'}
								on:change={() => handleSeatSelect('3A')}
							/>
							<label for="3A">3A</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="3B"
								checked={selectedSeat === '3B'}
								on:change={() => handleSeatSelect('3B')}
							/>
							<label for="3B">3B</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="3C"
								checked={selectedSeat === '3C'}
								on:change={() => handleSeatSelect('3C')}
							/>
							<label for="3C">3C</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="3D"
								checked={selectedSeat === '3D'}
								on:change={() => handleSeatSelect('3D')}
							/>
							<label for="3D">3D</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="3E"
								checked={selectedSeat === '3E'}
								on:change={() => handleSeatSelect('3E')}
							/>
							<label for="3E">3E</label>
						</li>
						<li class="seat">
							<input
								type="checkbox"
								id="3F"
								checked={selectedSeat === '3F'}
								on:change={() => handleSeatSelect('3F')}
							/>
							<label for="3F">3F</label>
						</li>
					</ol>
				</li>
			</ol>
			<div class="button-holder">
				<button type="button" class="select-seat-button" on:click={handleSelectSeat}>Chọn Ghế</button>
			</div>
			<div class="exit exit--back fuselage"></div>
		</div>
	{/if}
</div>
