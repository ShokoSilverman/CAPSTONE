<script>
	import Modal from './Modal.svelte';
	let showModal = false;

	const toggleModal = () => {
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
		
	};

</script>

<Modal showModal={showModal} on:click={toggleModal}>
	<form>

	</form>
	<form>
		<input type="text" name="" id="" placeholder="Email" bind:value={email}>
		<br>
		<input type="text" name="" id="" placeholder="Username" bind:value={username}>
		<br>
		<input type="password" name="" id="" placeholder="Password" bind:value={password}>
		<br>
		<input type="text" name="" id="checkPass" placeholder="Confirm Password" bind:value={confPassword} on:focusout={isSamePass}><p id="passConf">{passCheck}</p>
		<br>
		<button on:click={register}>Register</button>
	</form>
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


</style>