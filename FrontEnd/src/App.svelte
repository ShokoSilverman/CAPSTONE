<!-- keep this as light as possible, just use it for my routing manuevers -->

<script>
	import Home from './Home.svelte';
	import ModelCreation from './ModelCreation.svelte';
	import NotFound from './NotFound.svelte';
	import UseModel from './UseModel.svelte';
	import UserModels from './UserModels.svelte';

	const getAllModels = async () => {
		const response = await fetch("http://localhost:5000/getAllModels");
		const data = await response.json();
		return data;
	};

	const getModelById = async (id) => {
		const response = await fetch(`http://localhost:5000/getById/${id}`);
		const data = await response.json();
		return data;
	};

	const getUserModels = async (email) => {
		const response = await fetch(`http://localhost:5000/getAllByEmail/${email}`);
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
		let userObj = JSON.parse(document.cookie);
		params = {"model": model, "loggedUser": userObj.loggedUser, "loggedEmail": userObj.loggedEmail}
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
	router('/UserModels/',
	async(ctx, next) => {
		let userObj = JSON.parse(document.cookie);
		let models = await getUserModels(userObj.loggedEmail);
		params = {"models": models, "loggedUser": userObj.loggedUser, "loggedEmail": userObj.loggedEmail};
		next();
	},
	() => (page=UserModels)
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