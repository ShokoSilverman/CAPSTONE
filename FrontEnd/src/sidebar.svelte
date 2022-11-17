<script>
    export let showSideBar = false;

    const createModelClick = () =>{
        window.location.href = 'http://localhost:8080/ModelCreation';
    }

</script>

{#if showSideBar}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="backdrop" on:click|self> <!--this is an event modifier and a passed event-->
        <div id="sidebar" style="padding-top: 5%;">
            <br>
            <p on:click={createModelClick}>Create Model</p>
        </div>
    </div>
{/if}

<main></main>

<style>
    .backdrop{
        width: 100%;
        height: 100%;
        position: fixed;
        background: rgba(76, 80, 94, 0.6);
    }

    #sidebar{
        height: 100%; /* Full-height: remove this if you want "auto" height */
        width: 250px; /* Set the width of the sidebar */
        position: fixed; /* Fixed Sidebar (stay in place on scroll) */
        z-index: 1; /* Stay on top */
        top: 0; /* Stay at the top */
        right: 0;
        /* background-color: rgba(76, 80, 94, 1); */
        background-color: white;
        /* background-color: #303642; */
        overflow-x: hidden; /* Disable horizontal scroll */
        padding-top: 20px;
    }

    #sidebar p {
    padding: 6px 8px 6px 16px;
    text-decoration: none;
    font-size: 25px;
    color: #303642;
    display: block;
    }

    #sidebar p:hover {
    cursor: pointer;
    }
</style>