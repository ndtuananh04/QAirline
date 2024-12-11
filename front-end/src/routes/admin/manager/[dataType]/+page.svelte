<script>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { page } from '$app/stores';
    import { get } from 'svelte/store';

    let data = writable([]);
    let token = '';
    let email = '';
    let password = '';
    let retypePassword = '';

    const dataType = Object.values(get(page).params)[0];
    console.log(dataType);

    onMount(async () => {
        try {
            switch (dataType) {
                case 'accounts':
                    await getData('http://127.0.0.1:5000/addaccount', data);
                    break;
                case 'airplanes':
                    await getData('http://127.0.0.1:5000/airplanes', data);
                    break;
                case 'flights':
                    await getData('http://127.0.0.1:5000/flights', data);
                    break;
                case 'ticket':
                    await getData('http://127.0.0.1:5000/ticket-admin', data);
                    break;
                case 'seats':
                    break;
            }

            data.subscribe((value) => {
                console.log(value);
            });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    async function getData(url, data) {
        try {
            token = localStorage.getItem('jwt');
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch data: ${response.statusText}`);
            }

            const data_fetch = await response.json();
            console.log(data_fetch);
            data.set(data_fetch);
        } catch (error) {
            console.error(`Error in getData: ${error.message}`);
        }
    }

    async function submitAccountInput(e) {
        if (password != retypePassword) {
            alert('Mật khẩu không giống nhau!');
            return;
        }

		const response = await fetch('http://localhost:5000/addaccount', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				email: email,
				password: password
			})
		});
		if (!response.ok) {
			const errorData = await response.json();
            alert(errorData.msg || 'Add Data Failed');
		} else {
			const updatedData = await response.json();
			data.set(updatedData)
            alert("Thêm thành công");
		}
	}
</script>

<!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#addDataModal">
    Add Data
  </button>
  
  <!-- Modal -->
  <div class="modal fade" id="addDataModal" tabindex="-1" role="dialog" aria-labelledby="addDataModalCenter" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addDataModalCenter">Add data</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
            <form on:submit={submitAccountInput}>
                <div class="form-group">
                  <label for="newEmail">Email address</label>
                  <input type="email" class="form-control" id="newEmail" placeholder="Enter email" bind:value={email}>
                </div>
                <div class="form-group">
                  <label for="newPassword">Password</label>
                  <input type="password" class="form-control" id="newPassword" aria-describedby="passwordHelp" placeholder="Password" bind:value={password}>
                  <small id="passwordHelp" class="form-text text-muted">Mật khẩu phải có ít nhất 8 ký tự, có ít nhất một chữ viết hoa, 
                    một chữ viết thường,  
                    một số và một ký tự đặc biệt</small>
                    <label for="retypePassword">Retype Password</label>
                    <input type="password" class="form-control" id="retypePassword" placeholder="Retype Password" bind:value={retypePassword}>
                </div>
              </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button type="submit" class="btn btn-primary" data-dismiss="modal">Save changes</button>
        </div>
      </div>
    </div>
  </div>


<hr />


<table class="table">
	<thead>
		<tr>
            {#if dataType == 'accounts'}
			<th scope="col">#</th>
			<th scope="col">Email</th>
			<th scope="col">Role</th>
            {:else if dataType == 'airplanes'}
            <th scope="col">#</th>
			<th scope="col">Name</th>
			<th scope="col">Capacity</th>
            {:else if dataType == 'flights'}
            <th scope="col">#</th>
			<th scope="col">Number</th>
			<th scope="col">Depature Time</th>
            <th scope="col">Depature Hour Time</th>
            <th scope="col">Arrival Hour Time</th>
            <th scope="col">Terminal</th>
            <th scope="col">Status</th>
            {:else if dataType == 'tickets'}
            <th scope="col">#</th>
			<th scope="col">Flight ID</th>
			<th scope="col">Ticket Number</th>
            <th scope="col">Class</th>
            <th scope="col">Seat Number</th>
            <th scope="col">Booking Time</th>
            <th scope="col">Status</th>
            {/if}
		</tr>
	</thead>
	<tbody>
		{#each $data as item}
			<tr>
                {#if dataType == 'accounts'}
				<th scope="row">{item.account_id}</th>
				<td>{item.email}</td>
				<td>{item.role}</td>
                {:else if dataType == 'airplanes'}
                <th scope="row">{item.airplane_id}</th>
				<td>{item.name_airplane}</td>
				<td>{item.capacity}</td>
                {:else if dataType == 'flights'}
                <th scope="row">{item.flight_id}</th>
				<td>{item.flight_number}</td>
				<td>{item.departure_time}</td>
                <td>{item.departure_hour_time}</td>
                <td>{item.arrival_hour_time}</td>
                <td>{item.terminal}</td>
                <td>{item.status}</td>
                {:else if dataType == 'tickets'}
                <th scope="row">{item.ticket_id}</th>
				<td>{item.flight_id}</td>
				<td>{item.ticket_number}</td>
                <td>{item.seat_class}</td>
                <td>{item.seat_number}</td>
                <td>{item.booking_time}</td>
                <td>{item.status}</td>
                {/if}
			</tr>
		{/each}
	</tbody>
</table>