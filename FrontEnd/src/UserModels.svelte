<script>
    import Sidebar from "./sidebar.svelte";
    export let params;
    let models = params.models;
    let username = params.loggedUser;
    let email = params.LoggedEmail;
    let showSideBar = false;
</script>

<Sidebar showSideBar={showSideBar}></Sidebar>
<main>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <p class=curUser on:click={()=>{showSideBar = !showSideBar}}>{username}</p>
    <h1>Models</h1>
    {#each models as model (model._id)}
        <a href="/UseModel/{model._id}">{model.name}</a>
        <br>
    {/each}
</main>

<style>

</style>