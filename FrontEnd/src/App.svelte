<!-- keep this as light as possible, just use it for my routing manuevers -->

<script>
	import Home from './Home.svelte';
	import SecondPage from './secondpage.svelte';
	import NotFound from './NotFound.svelte';

	const getAllModels = async () => {
		const response = await fetch("http://localhost:5000/getAllModels");
		const data = await response.json();
		return data;
	};


	//how to redirect
	const secondPage = () =>{
		window.location.href = 'http://localhost:8080/secondpage';
	};

	//routing

	import router from 'page';

	let page;
	let params

	// router('/', () => (page=Home));
	router('/',
	async(ctx, next) => {
		let modelList = [];
		const modelPromise = await getAllModels();
		for(let i = 0; i < modelPromise.length; i++){
			modelList.push(modelPromise[i]);
		}
		params = {"models": modelList}

		next();
	},
	() => (page=Home)
	);
	router('/secondpage',
	(ctx, next) => {
		params = ctx.params;
		// params = {"test":"test1"}
		next();
	},
	() => (page=SecondPage)
	);
	router('/*', () => (page=NotFound));

	router.start();

	//end of routing

</script>


<main>
	<svelte:component this={page} {params} />
</main>

<style>
	
</style>