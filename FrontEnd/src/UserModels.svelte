<script>
    import Sidebar from "./sidebar.svelte";
    export let params;
    let modelList = params.models;
    let username = params.loggedUser;
    let email = params.LoggedEmail;
    let showSideBar = false;
</script>

<Sidebar showSideBar={showSideBar}></Sidebar>
<main>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <p class=curUser on:click={()=>{showSideBar = !showSideBar}}>{username}</p>
    <h1>My Models</h1>
    <div class="modelList">
		<!-- <div style="border-bottom-width: 1.5px;" class="horBar"></div> -->
		<div class="modelWrapper tableHeaders">
			<div class="modelID">ID</div>
			<div class="modelName">Model Name</div>
			<div class="modelDate">Date Created</div>
			<div class="modelType">Model Type</div>
			<div class="modelDescription">Model Description</div>
			<div style="width: 5%;">Use</div>
		</div>
	{#each modelList as model}
		<div class="modelWrapper">
			<div class="modelID">{model._id}</div>
			<div class="modelName">{model.name}</div>
			<div class="modelDate">{model.dateCreated}</div>
			<div class="modelType">{model.model_type}</div>
			<div class="modelDescription" title={model.description}>{model.description}</div>
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<div class="modelGo" on:click={()=>{document.location.href=`/UseModel/${model._id}`}}>GO</div>
			
		</div>
	{/each}
</main>

<style>
    h1{
        text-align: center;
		color: white;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
        padding-top: 4%;
    }

    .modelList{
        padding-left: 5%;
        padding-right: 5%;
    }

    .modelDate{
        width: 10%;
    }
</style>