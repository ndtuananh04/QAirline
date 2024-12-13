<script>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { page } from '$app/stores';
    

    let data = writable([]);
    let token = '';
    let selected = 0;

    //Add Account
    let email = '';
    let password = '';
    let retypePassword = '';

    //Add Airplane
    let name_airplane = '';
    let capacity = '';

    //Add Flight
    let newFlightNumber = '';
    let departure = '';
    let code_departure = '';
    let arrival = '';
    let code_arrival = '';
    let departure_time = '';
    let departure_hour_time = '';
    let arrival_hour_time = '';
    let boarding_time = '';
    let terminal = '';
    let status = '';
    let available_seats = '';
    let airplane_id = '';

    //Update Account
    let updatedEmail = '';
    let updatedPassword = '';
    let updatedRetypePassword = '';

    //Update Flight
    let updatedFlightNumber = '';
    let updatedDeparture = '';
    let updatedArrival = '';
    let updatedDepartureTime = '';
    let updatedDepartureHourTime = '';
    let updatedArrivalHourTime = '';
    let updatedBoardingTime = '';
    let updatedTerminal = '';
    let updatedStatus = '';
    let updatedAvailableSeats = '';
    let updatedAirplaneId = '';

    //Update Airplane
    let updatedAirplaneName = '';
    let updatedCapacity = '';

    const dataType = $page.params.dataType;
    console.log(dataType);

    onMount(async () => {
        try {
            switch (dataType) {
                case 'accounts':
                    await getData('http://127.0.0.1:5000/add-account-admin', data);
                    break;
                case 'airplanes':
                    await getData('http://127.0.0.1:5000/airplanes', data);
                    break;
                case 'flights':
                    await getData('http://127.0.0.1:5000/flights', data);
                    break;
                case 'tickets':
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

		const response = await fetch('http://localhost:5000/add-account-admin', {
			method: 'POST',
			headers: {
                Authorization: `Bearer ${token}`,
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

    async function submitAirplaneInput(e) {
        
		const response = await fetch('http://localhost:5000/airplanes', {
			method: 'POST',
			headers: {
                Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name_airplane: name_airplane,
                capacity: parseInt(capacity)
			})
		});
		if (!response.ok) {
			const errorData = await response.json();
            alert(errorData.msg || 'Add Data Failed');
		} else {
            await getData('http://127.0.0.1:5000/airplanes', data);
			const alertmsg = await response.json();
            alert(alertmsg.msg);
		}
	}

    async function submitFlightInput(e) {

		const response = await fetch('http://localhost:5000/flights', {
			method: 'POST',
			headers: {
                Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				flight_number: newFlightNumber,
				departure: departure,
                code_departure: code_departure,
                arrival: arrival,
                code_arrival: code_arrival,
                departure_time: departure_time,
                departure_hour_time: departure_hour_time,
                arrival_hour_time: arrival_hour_time,
                boarding_time: boarding_time,
                terminal: terminal,
                status: status,
                available_seats: available_seats,
                airplane_id: airplane_id
			})
		});
		if (!response.ok) {
			const errorData = await response.json();
            alert(errorData.msg || 'Add Data Failed');
		} else {
            await getData('http://127.0.0.1:5000/flights', data);
			const alertmsg = await response.json();
            alert(alertmsg.msg);
		}
	}

    function updateVariables(a, b, c, d, e, f, g, h, i, j, k, l) {
        if (dataType == 'accounts') {
            selected = a; 
            updatedEmail = b;
            updatedPassword = '';
            updatedRetypePassword = '';
        } else if (dataType == 'airplanes') {
            selected = a;
            updatedAirplaneName = b;
            updatedCapacity = c;
        } else if (dataType == 'flights') {
            selected = a;
            updatedFlightNumber = b;
            updatedDeparture = c;
            updatedArrival = d;
            updatedDepartureTime = e;
            updatedDepartureHourTime = f;
            updatedArrivalHourTime = g;
            updatedBoardingTime = h
            updatedTerminal = i;
            updatedStatus = j;
            updatedAvailableSeats = k;
            updatedAirplaneId = l;
        }
    }
    async function updateAccount(e) {
        if (updatedPassword == '' || updatedEmail == '') {
            alert('All fields cannot be left blank!')
            return;
        } else if (updatedPassword != updatedRetypePassword) {
            alert('Passwords do not match!')
            return;
        }
        const response = await fetch('http://localhost:5000/update-account-admin', {
			method: 'POST',
			headers: {
                Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				account_id: selected,
				email: updatedEmail,
                password: updatedPassword
			})
		});
		if (!response.ok) {
			const errorData = await response.json();
            alert(errorData.msg || 'Update Data Failed');
		} else {
            await getData('http://127.0.0.1:5000/add-account-admin', data);
            alert("Update Complete!");
		}
    }

    async function updateAirplane(e) {
        if (updatedAirplaneName == '' || updatedCapacity == '') {
            alert("All fields cannot be left blank!");
            return;
        }

        const response = await fetch('http://localhost:5000/airplanes', {
			method: 'PUT',
			headers: {
                Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
                name_airplane: updatedAirplaneName,
                capacity: updatedCapacity
			})
		});
		if (!response.ok) {
			const errorData = await response.json();
            alert(errorData.msg || 'Update Data Failed');
		} else {
            await getData('http://127.0.0.1:5000/airplanes', data);
            alert("Update Complete!");
		}

    }

    async function updateFlight(e) {
        if (updatedFlightNumber == '' ||
            updatedDeparture == '' ||
            updatedArrival == '' ||
            updatedDepartureTime == '' ||
            //updatedDepartureHourTime == '' ||
            //updatedArrivalHourTime == '' ||
            //updatedBoardingTime == '' ||
            //updatedTerminal == '' ||
            updatedStatus == '' ||
            updatedAvailableSeats == '' ||
            updatedAirplaneId == ''
        ) {
            alert("All fields cannot be left blank!")
            return;
        }
        
        const response = await fetch('http://localhost:5000/flights', {
			method: 'PUT',
			headers: {
                Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
                flight_id: selected,
				flight_number: updatedFlightNumber,
				departure: updatedDeparture,
                arrival: updatedArrival,
                departure_time: updatedDepartureTime,
                //departure_hour_time: updatedDepartureHourTime,
                //arrival_hour_time: updatedArrivalHourTime,
                //boarding_time: updatedBoardingTime,
                //terminal: updatedTerminal,
                status: updatedStatus,
                available_seats: updatedAvailableSeats,
                airplane_id: updatedAirplaneId
			})
		});
		if (!response.ok) {
			const errorData = await response.json();
            alert(errorData.msg || 'Update Data Failed');
		} else {
            await getData('http://127.0.0.1:5000/flights', data);
            alert("Update Complete!");
		}
    }

    async function deleteFromDatabase(e) {
        switch(dataType) {
            case 'accounts':
                const account_response = await fetch('http://127.0.0.1:5000/delete-account-admin', {
                    method: 'DELETE',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        account_id: selected
                    })
                });
                if (!account_response.ok) {
                    const errorData = await account_response.json();
                    alert(errorData.msg || 'Update Data Failed');
		        } else {
                    await getData('http://127.0.0.1:5000/add-account-admin', data);
                    alert("Deleted!");
		        }
                break;
            case 'flights':
                const flight_response = await fetch('http://127.0.0.1:5000/flights', {
                    method: 'DELETE',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        flight_id: selected
                    })
                });
                if (!flight_response.ok) {
                    const errorData = await flight_response.json();
                    alert(errorData.msg || 'Update Data Failed');
		        } else {
                    await getData('http://127.0.0.1:5000/flights', data);
                    alert("Deleted!");
		        }
                break;
            case 'airplanes':
                const airplane_response = await fetch('http://127.0.0.1:5000/airplanes', {
                    method: 'DELETE',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        airplane_id: selected
                    })
                });
                if (!airplane_response.ok) {
                    const errorData = await airplane_response.json();
                    alert(errorData.msg || 'Update Data Failed');
		        } else {
                    await getData('http://127.0.0.1:5000/airplanes', data);
                    alert("Deleted!");
		        }
                break;
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

            {#if dataType == 'accounts'}

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
                </div>
                <div class="form-group">
                    <label for="retypePassword">Retype Password</label>
                    <input type="password" class="form-control" id="retypePassword" placeholder="Retype Password" bind:value={retypePassword}>
                </div>
                
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Save changes</button>
                  
            </form>

            {:else if dataType == 'airplanes'}

            <form on:submit={submitAirplaneInput}>
                <div class="form-group">
                  <label for="newName">Name</label>
                  <input type="text" class="form-control" id="newName" placeholder="Enter name" bind:value={name_airplane}>
                </div>
                <div class="form-group">
                  <label for="newCapacity">Capacity</label>
                  <input type="text" class="form-control" id="newCapacity" placeholder="Capacity" bind:value={capacity}>
                </div>
                
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Save changes</button>
                  
            </form>


            {:else if dataType == 'flights'}

            <form on:submit={submitFlightInput}>
                <div class="form-group">
                  <label for="newFlightNumber">Number</label>
                  <input type="text" class="form-control" id="newFlightNumber" placeholder="Number" bind:value={newFlightNumber}>
                </div>
                <div class="form-group">
                  <label for="newDeparture">Departure</label>
                  <input type="text" class="form-control" id="newDeparture" placeholder="Departure" bind:value={departure}>
                </div>
                <div class="form-group">
                    <label for="newCodeDeparture">Code Departure</label>
                    <input type="text" class="form-control" id="newCodeDeparture" placeholder="Code Departure" bind:value={code_departure}>
                </div>
                <div class="form-group">
                    <label for="newArrival">Arrival</label>
                    <input type="text" class="form-control" id="newArrival" placeholder="Arrival" bind:value={arrival}>
                </div>
                <div class="form-group">
                    <label for="newCodeArrival">Code Arrival</label>
                    <input type="text" class="form-control" id="newCodeArrival" placeholder="Code Arrival" bind:value={code_arrival}>
                </div>
                <div class="form-group">
                    <label for="newDepartureTime">Departure Time</label>
                    <input type="text" class="form-control" id="newDepartureTime" placeholder="Departure Time" bind:value={departure_time}>
                </div>
                <div class="form-group">
                    <label for="newDepartureHourTime">Departure Hour Time</label>
                    <input type="text" class="form-control" id="newDepartureHourTime" placeholder="Departure Hour Time" bind:value={departure_hour_time}>
                </div>
                <div class="form-group">
                    <label for="newArrivalHourTime">Arrival Hour Time</label>
                    <input type="text" class="form-control" id="newArrivalHourTime" placeholder="Arrival Hour Time" bind:value={arrival_hour_time}>
                </div>
                <div class="form-group">
                    <label for="newBoardingTime">Boarding Time</label>
                    <input type="text" class="form-control" id="newBoardingTime" placeholder="Boarding Time" bind:value={boarding_time}>
                </div>
                <div class="form-group">
                    <label for="newTerminal">Terminal</label>
                    <input type="text" class="form-control" id="newTerminal" placeholder="Terminal" bind:value={terminal}>
                </div>
                <div class="form-group">
                    <label for="newStatus">Status</label>
                    <input type="text" class="form-control" id="newStatus" placeholder="Status" bind:value={status}>
                </div>
                <div class="form-group">
                    <label for="newAvailableSeats">Available Seats</label>
                    <input type="text" class="form-control" id="newAvailableSeats" placeholder="Available Seats" bind:value={available_seats}>
                </div>
                <div class="form-group">
                    <label for="FlightAirplaneID">Airplane ID</label>
                    <input type="text" class="form-control" id="FlightAirplaneID" placeholder="Airplane ID" bind:value={airplane_id}>
                </div>
                
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Save changes</button>
                  
            </form>


            {:else if dataType == 'tickets'}



            {/if}
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
            <th scope="col">Options</th>
            {:else if dataType == 'airplanes'}
            <th scope="col">#</th>
			<th scope="col">Name</th>
			<th scope="col">Capacity</th>
            <th scope="col">Options</th>
            {:else if dataType == 'flights'}
            <th scope="col">#</th>
			<th scope="col">Number</th>
            <!--
            <th scope="col">Depature</th>
            <th scope="col">Arrival</th>
            -->
			<th scope="col">Depature Time</th>
            <th scope="col">Depature Hour Time</th>
            <th scope="col">Arrival Hour Time</th>
            <!--
            <th scope="col">Boarding Time</th>
            -->
            <th scope="col">Terminal</th>
            <th scope="col">Status</th>
            <!--
            <th scope="col">Available Seats</th>
            <th scope="col">Airplane ID</th>
            -->
            <th scope="col">Options</th>
            {:else if dataType == 'tickets'}
            <th scope="col">#</th>
			<th scope="col">Flight ID</th>
			<th scope="col">Ticket Number</th>
            <th scope="col">Class</th>
            <th scope="col">Seat Number</th>
            <th scope="col">Booking Time</th>
            <th scope="col">Status</th>
            <th scope="col">Options</th>
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
                <td>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#updateDataModal" 
                    on:click={updateVariables(item.account_id, item.email)}>
                        Update
                      </button>

                      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#deleteActionConfirmation" on:click={selected = item.account_id}>
                        Delete
                      </button>
                </td>
                {:else if dataType == 'airplanes'}
                <th scope="row">{item.airplane_id}</th>
				<td>{item.name_airplane}</td>
				<td>{item.capacity}</td>
                <td>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#updateDataModal" 
                    on:click={updateVariables(item.airplane_id, item.name_airplane, item.capacity)}>
                        Update
                      </button>

                      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#deleteActionConfirmation" on:click={selected = item.airplane_id}>
                        Delete
                      </button>
                </td>
                {:else if dataType == 'flights'}
                <th scope="row">{item.flight_id}</th>
				<td>{item.flight_number}</td>
                <!--
                <td>{item.departure}</td>
                <td>{item.arrival}</td>
                -->
				<td>{item.departure_time}</td>
                <td>{item.departure_hour_time}</td>
                <td>{item.arrival_hour_time}</td>
                <!--
                <td>{item.boarding_time}</td>
                -->
                <td>{item.terminal}</td>
                <td>{item.status}</td>
                <!--
                <td>{item.available_seats}</td>
                <td>{item.airplane_id}</td>
                -->
                <td>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#updateDataModal" 
                    on:click={updateVariables(item.flight_id, item.flight_number,
                     item.departure, item.arrival, item.departure_time, item.departure_hour_time,
                     item.arrival_hour_time, item.boarding_time, item.terminal, item.status, item.available_seats,
                     item.airplane_id)}>
                        Update
                      </button>

                      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#deleteActionConfirmation" on:click={selected = item.flight_id}>
                        Delete
                      </button>
                </td>
                {:else if dataType == 'tickets'}
                <th scope="row">{item.ticket_id}</th>
				<td>{item.flight_id}</td>
				<td>{item.ticket_number}</td>
                <td>{item.seat_class}</td>
                <td>{item.seat_number}</td>
                <td>{item.booking_time}</td>
                <td>{item.status}</td>
                <td>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#updateDataModal" on:click={selected = item.ticket_id}>
                        Update
                      </button>

                      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#deleteActionConfirmation" on:click={selected = item.ticket_id}>
                        Delete
                      </button>
                </td>
                {/if}
			</tr>
		{/each}
	</tbody>
</table>


<div class="modal fade" id="updateDataModal" tabindex="-1" role="dialog" aria-labelledby="updateDataModalTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="updateDataModalTitle">Update Data</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          {#if dataType == 'accounts'}
          <form on:submit={updateAccount}>
          <div class="form-group">
            <label for="selectedAccountID">Account ID</label>
            <input type="text" class="form-control" id="selectedAccountID" placeholder={selected} bind:value={selected} disabled=true>
          </div>
          <div class="form-group">
            <label for="updatedEmail">Email</label>
            <input type="text" class="form-control" id="updatedEmail" placeholder={updatedEmail} bind:value={updatedEmail}>
          </div>
          <div class="form-group">
            <label for="updatedPassword">Password</label>
            <input type="password" class="form-control" id="updatedPassword" aria-describedby="passwordHelp" placeholder="Password" bind:value={updatedPassword}>
            <small id="passwordHelp" class="form-text text-muted">Mật khẩu phải có ít nhất 8 ký tự, có ít nhất một chữ viết hoa, 
              một chữ viết thường,  
              một số và một ký tự đặc biệt</small>
          </div>
          <div class="form-group">
            <label for="updatedRetypePassword">Retype Password</label>
            <input type="password" class="form-control" id="updatedRetypePassword" placeholder="Retype Password" bind:value={updatedRetypePassword}>
          </div>
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button type="submit" class="btn btn-primary">Save changes</button>
          </form>
          {:else if dataType == 'flights'}

          <form on:submit={updateFlight}>
            <div class="form-group">
              <label for="updatedFlightNumber">Number</label>
              <input type="text" class="form-control" id="updatedFlightNumber" placeholder={updatedFlightNumber} bind:value={updatedFlightNumber}>
            </div>
            <div class="form-group">
              <label for="updatedDeparture">Departure</label>
              <input type="text" class="form-control" id="updatedDeparture" placeholder="Departure" bind:value={updatedDeparture}>
            </div>
            <div class="form-group">
                <label for="updatedArrival">Arrival</label>
                <input type="text" class="form-control" id="updatedArrival" placeholder="Arrival" bind:value={updatedArrival}>
            </div>
            <div class="form-group">
                <label for="updatedDepartureTime">Departure Time</label>
                <input type="text" class="form-control" id="updatedDepartureTime" placeholder="Departure Time" bind:value={updatedDepartureTime}>
            </div>
            <!--
            <div class="form-group">
                <label for="updatedDepartureHourTime">Departure Hour Time</label>
                <input type="text" class="form-control" id="updatedDepartureHourTime" placeholder="Departure Hour Time" bind:value={updatedDepartureHourTime}>
            </div>
            <div class="form-group">
                <label for="updatedArrivalHourTime">Arrival Hour Time</label>
                <input type="text" class="form-control" id="updatedArrivalHourTime" placeholder="Arrival Hour Time" bind:value={updatedArrivalHourTime}>
            </div>
            <div class="form-group">
                <label for="updatedBoardingTime">Boarding Time</label>
                <input type="text" class="form-control" id="newBoardingTime" placeholder="Boarding Time" bind:value={updatedBoardingTime}>
            </div>
            <div class="form-group">
                <label for="updatedTerminal">Terminal</label>
                <input type="text" class="form-control" id="updatedTerminal" placeholder="Terminal" bind:value={updatedTerminal}>
            </div>
            -->
            <div class="form-group">
                <label for="updatedStatus">Status</label>
                <input type="text" class="form-control" id="updatedStatus" placeholder="Status" bind:value={updatedStatus}>
            </div>
            <div class="form-group">
                <label for="updatedAvailableSeats">Available Seats</label>
                <input type="text" class="form-control" id="updatedAvailableSeats" placeholder="Available Seats" bind:value={updatedAvailableSeats}>
            </div>
            <div class="form-group">
                <label for="updatedFlightAirplaneID">Airplane ID</label>
                <input type="text" class="form-control" id="updatedFlightAirplaneID" placeholder="Airplane ID" bind:value={updatedAirplaneId}>
            </div>
            
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Save changes</button>
              
        </form>

            {:else if dataType == 'airplanes'}

            <form on:submit={updateAirplane}>
                <div class="form-group">
                  <label for="updatedAirplaneName">Name</label>
                  <input type="text" class="form-control" id="updatedAirplaneName" placeholder="Enter name" bind:value={updatedAirplaneName}>
                </div>
                <div class="form-group">
                  <label for="updatedCapacity">Capacity</label>
                  <input type="text" class="form-control" id="updatedCapacity" placeholder="Capacity" bind:value={updatedCapacity}>
                </div>
                
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Save changes</button>
                  
            </form>

          {/if}
        </div>
          
      </div>
    </div>
  </div>

  
  <!-- Modal -->
  <div class="modal fade" id="deleteActionConfirmation" tabindex="-1" role="dialog" aria-labelledby="deleteActionConfirmationTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="deleteActionConfirmationTitle">Delete Data</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          Are you sure you want to delete row {selected}?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">No</button>
          <button type="button" class="btn btn-primary" data-dismiss="modal" on:click={deleteFromDatabase}>Yes</button>
        </div>
      </div>
    </div>
  </div>

