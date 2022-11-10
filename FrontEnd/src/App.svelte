<!-- keep this as light as possible, just use it for my routing manuevers -->

<script>
	import Home from './Home.svelte';
	import SecondPage from './secondpage.svelte';
	import NotFound from './NotFound.svelte';

	//routing

	import router from 'page';

	let page;
	let params

	router('/', () => (page=Home));
	router('/secondpage',
	(ctx, next) => {
		params = ctx.params;
		next();
	},
	() => (page=SecondPage)
	);
	router('/*', () => (page=NotFound));

	router.start();

	//end of routing

	//how to redirect
	const secondPage = () =>{
		window.location.href = 'http://localhost:8080/secondpage';
	}
</script>


<main>
	<svelte:component this={page} {params} />
</main>

<style>
	
</style>