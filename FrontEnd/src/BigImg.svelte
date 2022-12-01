<script>

    import Zoom from 'svelte-zoom'

    export let showBigImg = false;
    export let img;
    // export let message = 'default value';
</script>

{#if showBigImg}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <button on:click|self>Hide</button>
    <div class="backdrop"> <!--this is an event modifier and a passed event-->
            <!-- <img id="tree" src={img} alt=""> -->
            <Zoom src={img} alt="test"/>
    </div>
{/if}

<main></main>

<style>

    button{
        position: fixed;
        top: 2%;
        left: 1%;
        z-index: 10;
    }


    .backdrop{
        width: 100vw;
        height: 100vh;
        position: fixed;
        /* background: rgba(100,100,100,0.8); */
        background: rgba(76, 80, 94, 0.6);
        top: 0;
        left: 0;
    }


</style>