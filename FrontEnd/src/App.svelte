<script>
	import Modal from './Modal.svelte';
	let showModal = false;

	const toggleModal = () => {
		let button = document.getElementById('signModal');
		if(button.style.visibility == 'hidden'){
			document.getElementById('signModal').style.visibility = 'visible';
		}else document.getElementById('signModal').style.visibility = 'hidden';
		showModal = !showModal
		
	}

	let email;
	let username;
	let password;
	let confPassword;
	let passCheck = "";
	
	const isSamePass = () =>{
		if (password != confPassword){
			passCheck = "Passwords do not match!"
		}else{
			passCheck = ""
		}
	}

	const register = () => {
		let pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/;
		if (passCheck == "Passwords do not match!") return;
		if (pattern.test(password)){
			console.log('good pass')
		}else {
			console.log('bad pass')
		}
		
	};


</script>

<Modal showModal={showModal} on:click={toggleModal}>
	<div id='flex-form'>
		<form id='login'>
			<input type="text" name="" id="" placeholder="Email" bind:value={email}>
			<br>
			<input type="password" name="" id="" placeholder="Password" bind:value={password} on:focusout={isSamePass}>
			<br>
			<button>Login</button>
		</form>
		<div id='bar'></div>
		<form id='register'>
			<input type="text" name="" id="" placeholder="Email" bind:value={email}>
			<br>
			<input type="text" name="" id="" placeholder="Username" bind:value={username}>
			<br>
			<input type="password" name="" id="" placeholder="Password" bind:value={password} on:focusout={isSamePass}>
			<br>
			<input type="password" name="" id="checkPass" placeholder="Confirm Password" bind:value={confPassword} on:focusout={isSamePass}><p id="passConf">{passCheck}</p>
			<br>
			<button on:click|preventDefault={register}>Register</button>
		</form>
	</div>
</Modal>
<main>
	<button on:click={toggleModal} id="signModal">Login/Sign Up</button>
	<h1>Welcome to ML-Silver</h1>
	<h4>ML-Silver's creator had one goal in mind:</h4>
	<h4>Bringing machine learning to the everyday person, and make it as easy as possible.</h4>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: white;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}
	h4 {
		color: orange;
		text-transform: uppercase;
		font-size: 2em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	#signModal{
		position: absolute;
		top: 1.5%;
		right: 1%;
	}

	#passConf{
        color:red;
        font-size: 80%;
    }

	#flex-form{
		display: flex;
		flex-direction: row;
		justify-content: space-evenly;
	}

	#signModal{
		visibility: visible;
	}

	#bar{
		width: 0.5%;
		background: orange;
	}




</style>