<script>
    import axios from 'axios';
    import Sidebar from './sidebar.svelte';
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

        //dante saved me
        modelFile = document.querySelector("#modelFile").files[0];
        let modelObject = {'dirty_csv': modelFile, 'output_field': modelOutput, 'model_type': +isRegression, 'training_percent': trainingPercent, 'min_acc': minimumAccuracy, 'name': modelName, 'is_private': +isPrivate, 'description': modelDescription, 'user': username, 'user_email': email};
        //change my backend to use json instead of form data
        console.log(modelObject)

        // const request = new XMLHttpRequest();
        // request.open("POST", "http://localhost:8888/mainlearningapi/createModel");
        // request.setRequestHeader("Content-Type", "multipart/form-data");
        // request.send(JSON.stringify(modelObject));
        // request.onload = () =>{
		// 	alert(request.responseText)
        // }

        // let response = await axios.post('http://localhost:8888/mainlearningapi/createModel', modelObject)
        
        let entries = Object.entries(modelObject)

        let formData = new FormData();
        for(let i = 0; i < entries.length; i++){
            console.log(entries[i][0], entries[i][1], entries[i]);
            formData.append(entries[i][0], entries[i][1])
        }
        //send form data to backend
        // let response = await axios.post('http://localhost:8888/mainlearningapi/createModel', formData)
        // alert(response.data)
        axios({
            method: "post",
            url: "http://localhost:8888/mainlearningapi/createModel",
            data: formData,
            headers: { "Content-Type": "multipart/form-data" },
        })
            .then(function (response) {
                //handle success
                console.log(response);
        })
            .catch(function (response) {
                //handle error
                console.log(response);
        });
        
        // console.log(formData)
    }

    
</script>


<!-- add sidebar and top right menu to this page -->
<Sidebar showSideBar={showSideBar}></Sidebar>
<main>
<p class=curUser on:click={()=>{showSideBar = !showSideBar}}>{username}</p>
<form>
    <label for="">model name:</label>
    <input type="text" bind:value={modelName} maxlength="30">
    <br>
    <label for="">description:</label>
    <input type="text" bind:value={modelDescription}>
    <br>
    <label for="">type:</label>
    <label for="">Classification: </label>
    <input type="checkbox" name="" id="" bind:checked={isClassification} on:click={() => {isClassification = !isClassification; isRegression = !isClassification}}>
    <label for="">Regression: </label>
    <input type="checkbox" name="" id="" bind:checked={isRegression} on:click={() => {isRegression = !isRegression; isClassification = !isRegression}}>
    <br>
    <label for="">Output field: </label>
    <input type="text" bind:value={modelOutput}>
    <br>
    <label for="">training %: </label>
    <input type="text" bind:value={trainingPercent}>
    <br>
    <label for="">minimum accuracy %:</label>
    <input type="text" bind:value={minimumAccuracy}>
    <br>
    <label for="">public: </label>
    <input type="checkbox" bind:checked={isPublic} on:click={() => {isPrivate = !isPrivate}}>
    <label for="">private: </label>
    <input type="checkbox" bind:value={isPrivate} bind:checked={isPrivate}>
    <br>
    <label for="">input file:</label>
    <input id="modelFile"type="file" accept=".csv," bind:value={modelFile}>
    <br>
    <button on:click|preventDefault={createModel}>Create Model</button>
</form>
</main>

<style>
label{
    display: inline-block
}
</style>