<script>
    export let showModal = false;
    // export let message = 'default value';
</script>

{#if showModal}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="backdrop" on:click|self> <!--this is an event modifier and a passed event-->
        <div id="modal">
            <!-- <p>{message}</p> -->
            <slot></slot>
        </div>
    </div>
{/if}

<main></main>

<style>
    .backdrop{
        width: 100%;
        height: 100%;
        position: fixed;
        /* background: rgba(100,100,100,0.8); */
        background: rgba(76, 80, 94, 0.6);
    }

    #modal{
        padding: 1%;
        border-radius: 10px;
        border: 4px solid orange;
        max-width: 500px;
        /* margin: 10px auto; */
        margin: 18% auto;
        text-align: center;
        background: white;
    }

    #bar{
        /* width: 5px; */
        height: 100%;
        /* height: 90%; */
        /* background: orange; */
    }
</style>