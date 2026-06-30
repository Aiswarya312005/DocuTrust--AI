async function uploadPDF(){

    let file =
    document.getElementById("pdf").files[0];

    let formData =
    new FormData();

    formData.append("pdf", file);

    let response =
    await fetch("/upload",{
        method:"POST",
        body:formData
    });

    let data =
    await response.json();

    alert(data.message);
}

async function askQuestion(){

    let question =
    document.getElementById("question").value;

    let response =
    await fetch("/ask",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            question:question
        })
    });

    let data =
    await response.json();

    document.getElementById("answer").innerHTML =
    data.answer;
}
