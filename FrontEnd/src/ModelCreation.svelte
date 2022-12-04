<script>
    import axios from 'axios';
    import Sidebar from './sidebar.svelte';
    import { RingLoader } from 'svelte-loading-spinners';


    let showLoader = false;
    let showSideBar = false;

    export let params;
    
    let username = params.LoggedUser;
    let email = params.LoggedEmail;

    let isClassification = true
    let isRegression = false; //fix this shit, make it one var isClassification = true/false
    let isPrivate = false;
    $: isPublic = !isPrivate;

    let modelName;
    let modelDescription;
    let modelOutput;
    let trainingPercent = 20;
    let minimumAccuracy = 75;
    let modelFile;

    const createModel = async() =>{
        showLoader = true;

        //dante saved me
        modelFile = document.querySelector("#modelFile").files[0];
        let modelObject = {'dirty_csv': modelFile, 'output_field': modelOutput, 'model_type': +isRegression, 'training_percent': trainingPercent, 'min_acc': minimumAccuracy, 'name': modelName, 'is_private': +isPrivate, 'description': modelDescription, 'user': username, 'user_email': email};
        //change my backend to use json instead of form data
        console.log(modelObject)

        let entries = Object.entries(modelObject)

        let formData = new FormData();
        for(let i = 0; i < entries.length; i++){
            console.log(entries[i][0], entries[i][1], entries[i]);
            formData.append(entries[i][0], entries[i][1])
        }
        console.log(formData);
        axios({
            method: "post",
            url: "http://localhost:8888/mainlearningapi/createModel",
            data: formData,
            headers: { "Content-Type": "multipart/form-data" },
        })
            .then(function (response) {
                //handle success
                console.log(response);
                window.location.href = `http://localhost:8080/UseModel/${response.data}`;
        })
            .catch(function (response) {
                //handle error
                console.log(response);
        });
        
        // console.log(formData)
    }

    
</script>


<!-- add sidebar and top right menu to this page -->
<div id="sideBar">
    <Sidebar showSideBar={showSideBar}></Sidebar>
</div>
<main>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <p class=curUser on:click={()=>{showSideBar = !showSideBar}}>{username}</p>
    <h1>Create A New Model</h1>
    <form>
        <div class="formBox">
            <label for="">Model Name:</label>
            <input type="text" bind:value={modelName} maxlength="30">
        </div>
        <div class="formBox">
            <label for="">Description:</label>
            <textarea bind:value={modelDescription}></textarea>
        </div>
        <div class="formBox">
            <label for="">Type:</label>
            <label class="modelType" for="">Classification: </label>
            <input type="checkbox" name="" id="" bind:checked={isClassification} on:click={() => {isClassification = !isClassification; isRegression = !isClassification}}>
            <label class="modelType" for="" style="padding-left: 5%;">Regression: </label>
            <input type="checkbox" name="" id="" bind:checked={isRegression} on:click={() => {isRegression = !isRegression; isClassification = !isRegression}}>
        </div>
        <div class="formBox">
            <label for="">Output field: </label>
            <input type="text" bind:value={modelOutput}>
        </div>
        <div class="formBox">
            <label for="">Training %: </label>
            <input type="text" bind:value={trainingPercent}>
        </div>
        <div class="formBox">
            <label for="">Minimum accuracy %:</label>
            <input type="text" bind:value={minimumAccuracy}>
        </div>
        <div class="formBox">
            <label for="">Visibility:</label>
            <label for="" class="modelType">Public: </label>
            <input type="checkbox" bind:checked={isPublic} on:click={() => {isPrivate = !isPrivate}}>
            <label for="" class="modelType" style="padding-left: 5%;">Private: </label>
            <input type="checkbox" bind:value={isPrivate} bind:checked={isPrivate}>
        </div>
        <div class="formBox">
            <label for="">Input file:</label>
            <input id="modelFile" type="file" accept=".csv," bind:value={modelFile}>
        </div>
        <div class="center">
            <button on:click|preventDefault={createModel}>Create Model</button>
        </div>
    </form>
    {#if showLoader}
        <div id="loadingSym">
            <RingLoader size=400/>
        </div>
    {/if}
</main>

<style>

    h1{
        position: fixed;
        top: 0;
        left: 0;
		color: orange;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
        padding-left: 3%;
        padding-top: 2%;
    }


    form{
        border: 3px solid orange;
        background-color: white;
        width: 50%;
        margin: auto;
        margin-top: 10%;
        height: auto;
        padding-top: 2%;
    }

    label{
        color: black;
        text-align: right;
        width: 40%;
        padding-right: 10%;
    }

    #loadingSym{
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    #sideBar{
        z-index: 10;
    }

    .formBox{
        display: flex;
        flex-direction: row;
    }

    textarea{
        resize: none;
        overflow: auto;
        height: 12%;
        width: 40%;
    }

    .modelType{
        width: auto;
        padding: 0px 1% 0px 0px;
    }

    #modelFile{
        border-width: 0px;
        padding: 0 0 0 0;
        margin: 0 0 0 0;
        color: black;
    }

    input{
        margin-bottom: 2%;
    }

    .center{
        margin-top: 3%;
    }






</style>