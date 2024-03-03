document.addEventListener("DOMContentLoaded", () => {
    fetch("/projects").then(res => res.json()).then(projectsData => {
        projectsData.forEach(project => {
            /* add br */
            document.querySelector("#myprojects").appendChild(document.createElement("br"));
            document.querySelector("#myprojects").appendChild(generateprojectelement(project));
            
        });
    })
    

});

function generateprojectelement(data){
    const a = document.createElement("a");
    a.classList.add("projectlink");
    a.href = data.Link;

    const div = document.createElement("div");
    div.classList.add("project");

    const img = document.createElement("img");
    img.classList.add("projectimg");
    img.src = data.Icon;
    img.width = 75;
    img.height = 75;

    const h2 = document.createElement("h2");
    h2.classList.add("projectname");
    h2.innerText = data.Name;

    const p = document.createElement("p");
    p.classList.add("projectdescription");
    p.innerText = data.ProjectDescription;

    div.appendChild(img);
    div.appendChild(h2);
    div.appendChild(p);
    a.appendChild(div);
    return a;
}
