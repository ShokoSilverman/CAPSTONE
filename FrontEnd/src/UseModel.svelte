<script>
    import { RingLoader } from 'svelte-loading-spinners';
    import BigImg from './BigImg.svelte';
    


    import axios from "axios";
    import Sidebar from "./sidebar.svelte";
    export let params;
    
    let username = params.loggedUser;
    let email = params.LoggedEmail;
    let showSideBar = false;
    let model = params.model;
    // console.log(model)
    let name = model.name;
    let description = model.description;
    let userCreated = model.user;
    let dateCreated = model.dateCreated;
    let graph = model.graph;
    let inputCols = model.input_cols;

    let showLoader = false;
    let showBigImg = false;

    const togBigImg = () =>{
        showBigImg = !showBigImg;
        let sideToggle = document.getElementsByClassName('curUser')[0]
        if (sideToggle.style.visibility == 'hidden'){
            sideToggle.style.visibility = 'visible';
        }else sideToggle.style.visibility = 'hidden';
    }
    
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
        // console.log(testValCombo);
        showLoader = true;
        try{
        let response = await axios.post(`http://localhost:8888/usemodelapi/useModel?id=${model._id}&entered_data=${testValCombo}`);
        learnedValue = response.data;
        }catch(err){
            learnedValue = "An error has occured, please try again later";
        }
        outputVal.textContent = "Result: " + learnedValue;
        outputVal.style.visibility = "visible";
        showLoader = false;
    }

</script>
<Sidebar showSideBar={showSideBar}></Sidebar>
<BigImg showBigImg={showBigImg} on:click={togBigImg} img="data:image;base64,{graph}"></BigImg>
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
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- add button to top left that shows absolute when big pic shows -->
            <img id="treeImg" src="data:image;base64,{graph}" alt="" on:click={togBigImg}>
            <div id="inputContainer">
                {#each inputCols as inputCol}
                    <input class="userIn" type="text" placeholder={inputCol} title={inputCol}>
                {/each}
                <!-- <input class="userIn" type="text" name="" id="">
                <input class="userIn" type="text" name="" id=""> -->
            </div>
            <button on:click={testData}>Test Data</button>
            {#if showLoader}
                <RingLoader />
            {/if}
            <!-- move loading animation here and reformat to fit in bottom left of screen, uses too much space on right side and can help fill in, add orange bored to whole thing -->
            <p id="outputVal"></p>
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

    #inputContainer{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        width: 60%;
    }

    #treeImg{
        width: 60%;
        border: 8px solid orange;
        margin-bottom: 1%;
    }

    #treeImg:hover{
        cursor: pointer;
    }

    h1{
        font-size: 4rem;
        color: orange;
        margin-bottom: 3%;
        margin-top: 1%;
        margin-left: 1%;
    }

    #infoDiv{
        margin-left: 2%;
        margin-top: 12%;
    }

    h2{
        font-size: 1.8rem;
        color: orange;
        /* margin-bottom: 1%;
        margin-top: 1%; */
    }

    .modelInfo{
        font-size: 1.4rem;
        color: white;
        margin-bottom: 1%;
        margin-top: 1%;
        margin-left: 5%;
    }

    .userIn{
        width: 20%;
        margin: 1% 1% 1% 1%;
    }

    #outputVal{
        font-size: 2rem;
        color: orange;
        margin-top: 1%;
        visibility: hidden;
    }

    


</style>