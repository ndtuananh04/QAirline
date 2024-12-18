<script>
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';

	let chartCanvas;
	let chartInstance;
	let selectedYear = 2024; // Mặc định là 2024

	Chart.register(...registerables);

	let chartData = [];

	// Fetch dữ liệu từ API theo năm đã chọn
	const fetchChartData = async (year) => {
		const token = localStorage.getItem('jwt');
		const response = await fetch(`http://localhost:5000/quantity-ticket`, {
			headers: { Authorization: `Bearer ${token}` }
		});

		const result = await response.json();
		if (result.status === 'success') {
			// Lọc dữ liệu theo năm được chọn
			chartData = result.data.filter((item) => item.year === year);
			renderChart();
		} else {
			alert('Lỗi khi tải dữ liệu biểu đồ');
		}
	};

	// Render biểu đồ với dữ liệu đã lọc
	const renderChart = () => {
		if (chartInstance) chartInstance.destroy();

		const months = Array.from({ length: 12 }, (_, index) => `Tháng ${index + 1}`);
		const businessData = Array(12).fill(0);
		const skybossData = Array(12).fill(0);
		const economyData = Array(12).fill(0);

		// Chỉ lấy dữ liệu của năm đã chọn và điền vào mảng dữ liệu tương ứng
		chartData.forEach((item) => {
			const monthIndex = item.month - 1;
			businessData[monthIndex] = item.business || 0;
			skybossData[monthIndex] = item.skyboss || 0;
			economyData[monthIndex] = item.economy || 0;
		});

		// Tạo gradient cho các dòng
		const gradientBlue = chartCanvas.getContext('2d').createLinearGradient(0, 0, 0, 400);
		gradientBlue.addColorStop(0, 'rgba(0, 0, 255, 0.3)');
		gradientBlue.addColorStop(1, 'rgba(0, 0, 255, 0.8)');

		const gradientOrange = chartCanvas.getContext('2d').createLinearGradient(0, 0, 0, 400);
		gradientOrange.addColorStop(0, 'rgba(255, 165, 0, 0.3)');
		gradientOrange.addColorStop(1, 'rgba(255, 165, 0, 0.8)');

		const gradientGreen = chartCanvas.getContext('2d').createLinearGradient(0, 0, 0, 400);
		gradientGreen.addColorStop(0, 'rgba(0, 128, 0, 0.3)');
		gradientGreen.addColorStop(1, 'rgba(0, 128, 0, 0.8)');

		chartInstance = new Chart(chartCanvas, {
			type: 'line',
			data: {
				labels: months,
				datasets: [
					{
						label: 'Business',
						data: businessData,
						borderColor: gradientBlue,
						backgroundColor: gradientBlue,
						//fill: true,
						borderWidth: 2,
						pointBackgroundColor: 'rgba(0, 0, 255, 1)',
						pointBorderWidth: 2,
						pointRadius: 5,
						tension: 0.4
					},
					{
						label: 'Skyboss',
						data: skybossData,
						borderColor: gradientOrange,
						backgroundColor: gradientOrange,
						//fill: true,
						borderWidth: 2,
						pointBackgroundColor: 'rgba(255, 165, 0, 1)',
						pointBorderWidth: 2,
						pointRadius: 5,
						tension: 0.4
					},
					{
						label: 'Economy',
						data: economyData,
						borderColor: gradientGreen,
						backgroundColor: gradientGreen,
						//fill: true,
						borderWidth: 2,
						pointBackgroundColor: 'rgba(0, 128, 0, 1)',
						pointBorderWidth: 2,
						pointRadius: 5,
						tension: 0.4
					}
				]
			},
			options: {
				responsive: true,
				plugins: {
					title: {
						display: true,
						text: `Số lượng vé theo tháng (${selectedYear})`,
						font: {
							size: 18,
							weight: 'bold'
						},
						color: '#333'
					},
					tooltip: {
						mode: 'index',
						intersect: false
					}
				},
				scales: {
					x: {
						title: { display: true, text: 'Tháng' },
						grid: { display: false }
					},
					y: {
						title: { display: true, text: 'Số lượng vé' },
						beginAtZero: true,
						grid: { color: '#ddd' }
					}
				},
				elements: {
					line: {
						borderJoinStyle: 'round'
					},
					point: {
						radius: 5,
						borderWidth: 2
					}
				}
			}
		});
	};

	// Hàm xử lý khi người dùng chọn năm
	const handleYearChange = (event) => {
		selectedYear = parseInt(event.target.value, 10); // Chuyển năm về kiểu số
		fetchChartData(selectedYear);
	};

	onMount(() => {
		fetchChartData(selectedYear); // Lấy dữ liệu cho năm mặc định khi trang tải
	});
</script>

<!-- Div chứa canvas, giúp căn giữa biểu đồ -->
<div class="chart-container">
	<canvas bind:this={chartCanvas}></canvas>
</div>

<!-- Dropdown chọn năm -->
<div class="year-selector">
	<label for="year">Chọn năm: </label>
	<select id="year" bind:value={selectedYear} on:change={handleYearChange}>
		<option value="2024">2024</option>
		<option value="2025">2025</option>
		<option value="2026">2026</option>
	</select>
</div>

<style>
	.chart-container {
		flex: 1;
		overflow-y: auto;
		padding: 50px;
		margin-left: 200px;
	}

	.chart-container canvas {
		width: 100%;
		height: calc(100vh - 80px);
		max-height: 100%;
		border-radius: 12px;
		box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
	}

	.year-selector {
		margin-top: 20px;
		text-align: center;
	}

	.year-selector select {
		font-size: 16px;
		padding: 5px;
		border-radius: 5px;
		border: 1px solid #ccc;
	}
</style>
