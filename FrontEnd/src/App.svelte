<!-- keep this as light as possible, just use it for my routing manuevers -->

<script>
	import Home from './Home.svelte';
	import ModelCreation from './ModelCreation.svelte';
	import NotFound from './NotFound.svelte';
	import UseModel from './UseModel.svelte';

	const getAllModels = async () => {
		const response = await fetch("http://localhost:5000/getAllModels");
		const data = await response.json();
		return data;
	};

	const getModelById = async (id) => {
		const response = await fetch(`http://localhost:5000/getById/${id}`);
		// const response = await fetch(`http://localhost:5000/getById/63767433911301ea5e0a6fef`);
		const data = await response.json();
		return data;
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
	router('/UseModel/:id',
	async(ctx, next) => {
		let model = await getModelById(ctx.params.id);
		params = {"model": model}
		next();
	},
	() => (page=UseModel)
	);
	//make this the create model page
	router('/ModelCreation/',
	(ctx, next) => {
		let userObj = JSON.parse(document.cookie);
		params = {"LoggedUser": userObj.loggedUser, "LoggedEmail": userObj.loggedEmail};
		next();
	},
	() => (page=ModelCreation)
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