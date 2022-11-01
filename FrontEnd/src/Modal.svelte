<script>
    export let showModal = false;
    // export let message = 'default value';
</script>

{#if showModal}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="backdrop" on:click|self> <!--this is an event modifier and a passed event-->
        <div class="modal">
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
        background: rgba(100,100,100,0.8);
    }

    .modal{
        padding: 10px;
        border-radius: 10px;
        max-width: 400px;
        /* margin: 10px auto; */
        margin: 18% auto;
        text-align: center;
        background: white;
    }
</style>