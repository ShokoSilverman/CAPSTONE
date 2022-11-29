<script>
    import { RingLoader } from 'svelte-loading-spinners';


    import axios from "axios";
    import Sidebar from "./sidebar.svelte";
    export let params;

    const outputElement = document.getElementById("outputVal");
    
    
    let username = params.loggedUser;
    let email = params.LoggedEmail;
    let showSideBar = false;
    let model = params.model;
    console.log(model)
    let name = model.name;
    let description = model.description;
    let userCreated = model.user;
    let dateCreated = model.dateCreated;
    let graph = model.graph;
    let inputCols = model.input_cols;

    let showLoader = false;

    
    
    const testData = async() =>{
        let learnedValue;
        const outputVal = document.getElementById("outputVal")
        let userInputs = document.getElementsByClassName("userIn");
        outputVal.style.visibility = "hidden";
        let testValues = [];
        for(let i = 0; i<userInputs.length; i++){
            testValues.push(userInputs[i].value);
        }
        let testValCombo = testValues.join(",");
        console.log(testValCombo);
        showLoader = true;
        try{
        let response = await axios.post(`http://localhost:8888/usemodelapi/useModel?id=${model._id}&entered_data=${testValCombo}`);
        learnedValue = response.data;
        }catch(err){
            learnedValue = "An error has occured, please try again later";
        }
        outputVal.textContent = learnedValue;
        outputVal.style.visibility = "visible";
        showLoader = false;
    }

</script>
<Sidebar showSideBar={showSideBar}></Sidebar>
<main>
    <h1>{name}</h1>
    <div id="mainWrapper">
        <div id="leftInfo">
            <div id="infoDiv">
                <h2>Created By:</h2>
                <p class="modelInfo">{userCreated}</p>
                <h2>Date Created:</h2>
                <p class="modelInfo">{dateCreated}</p>
                <h2>Description:</h2>
                <p class="modelInfo">{description}</p>
            </div>
        </div>
        <div id="mainInfo">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <p class=curUser on:click={()=>{showSideBar = !showSideBar}}>{username}</p>
            <img id="treeImg" src="data:image;base64,{graph}" alt="">
            <div id="inputContainer">
                {#each inputCols as inputCol}
                    <input class="userIn" type="text" placeholder={inputCol}>
                {/each}
                <input type="text" name="" id="">
            </div>
            <button on:click={testData}>Test Data</button>
            <p id="outputVal"></p>
            {#if showLoader}
                <RingLoader />
            {/if}
        </div>
        <!-- <div id="RightInfo"></div> -->
    </div>

</main>

<style>
    
    #mainWrapper{
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        width: 100vw;
    }

    #leftInfo{
        width: 30%;
        align-self: flex-start;
    }

    #mainInfo{
        display: flex;
        flex-direction: column;
        align-items: center;
        /* justify-content: center; */
        width: 70%;
        
    }

    #treeImg{
        width: 60%;
        border: 8px solid orange;
    }

    #inputContainer{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        width: 60%;
    }

    h1{
        font-size: 4rem;
        color: orange;
        margin-bottom: 3%;
        margin-top: 1%;
        margin-left: 1%;
    }

    h2{
        font-size: 1.4rem;
        color: orange;
        /* margin-bottom: 1%;
        margin-top: 1%; */
    }

    #infoDiv{
        margin-left: 2%;
        margin-top: 12%;
    }

    .modelInfo{
        font-size: 1.2rem;
        color: white;
        margin-bottom: 1%;
        margin-top: 1%;
        margin-left: 5%;
    }

</style>