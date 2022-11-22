<script>
    import axios from "axios";
    import Sidebar from "./sidebar.svelte";
    export let params;
    
    let username = params.loggedUser;
    let email = params.LoggedEmail;
    let showSideBar = false;
    let model = params.model;
    console.log(model);
    let graph = model.graph;
    let inputCols = model.input_cols;

    
    
    const testData = async() =>{
        let userInputs = document.getElementsByClassName("userIn");
        let testValues = [];
        for(let i = 0; i<userInputs.length; i++){
            testValues.push(userInputs[i].value);
        }
        let testValCombo = testValues.join(",");
        console.log(testValCombo);

        let learnedValue;

        // let data_out = {'id': model._id, 'entered_data': testValCombo}
        let data_out = {'id': '63767433911301ea5e0a6fef', 'entered_data': '21,1'}
        console.log(data_out)

        axios({
            method: "get",
            url: "http://localhost:8888/usemodelapi/useModel",
            data: {'id': model._id, 'entered_data': testValCombo},
            // data: data_out,
            headers: { "Content-Type": "multipart/form-data" },
        })
            .then(function (response) {
                //handle success
                console.log(response);
                learnedValue = response.data;
                console.log(learnedValue)
        })
            .catch(function (response) {
                //handle error
                console.log(response);
        });
    }

</script>

<Sidebar showSideBar={showSideBar}></Sidebar>
<main>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <p class=curUser on:click={()=>{showSideBar = !showSideBar}}>{username}</p>
    <img id="treeImg" src="data:image;base64,{graph}" alt="">
    {#each inputCols as inputCol}
        <input class="userIn" type="text" placeholder={inputCol}>
    {/each}
    <button on:click={testData}>Test Data</button>

</main>

<style>
    #treeImg{
        width: 40%;
    }
</style>