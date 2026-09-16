const form=document.getElementById("resumeForm"), input=document.getElementById("resume"), browse=document.getElementById("browse"), drop=document.getElementById("dropzone"), fileName=document.getElementById("fileName");
browse.onclick=()=>input.click(); input.onchange=()=>showFile();
["dragenter","dragover"].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.add("drag")}));
["dragleave","drop"].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.remove("drag")}));
drop.addEventListener("drop",e=>{input.files=e.dataTransfer.files;showFile()});
function showFile(){fileName.textContent=input.files[0]?`Selected: ${input.files[0].name}`:"";}
let chart;
form.addEventListener("submit",async e=>{
 e.preventDefault(); if(!input.files.length){showError("Please select a resume first.");return;}
 document.getElementById("loading").classList.remove("hidden");document.getElementById("error").classList.add("hidden");
 const data=new FormData(form);
 try{
  const r=await fetch("/analyze",{method:"POST",body:data}); const d=await r.json(); if(!r.ok)throw new Error(d.error||"Analysis failed");
  render(d);
 }catch(err){showError(err.message)}finally{document.getElementById("loading").classList.add("hidden")}
});
function showError(x){const el=document.getElementById("error");el.textContent=x;el.classList.remove("hidden")}
function render(d){
 document.getElementById("results").classList.remove("hidden"); document.getElementById("fileLabel").textContent=d.filename;
 document.getElementById("score").textContent=d.score;document.getElementById("match").textContent=d.match_percentage;document.getElementById("ats").textContent=d.ats_score;document.getElementById("words").textContent=d.word_count;
 document.getElementById("predicted").textContent=d.predicted_role;document.getElementById("target").textContent=d.target_role;document.getElementById("confidence").textContent=d.confidence+"%";document.getElementById("confBar").style.width=d.confidence+"%";
 fill("skills",d.skills,false);fill("missing",d.missing_skills,true);
 const s=document.getElementById("suggestions");s.innerHTML=d.suggestions.map(x=>`<div class="recommendation"><b>AI</b>${x}</div>`).join("");
 if(chart)chart.destroy(); chart=new Chart(document.getElementById("skillChart"),{type:"doughnut",data:{labels:["Matched","Missing"],datasets:[{data:[d.matched_skills.length,d.missing_skills.length]}]},options:{plugins:{legend:{position:"bottom"}},cutout:"68%"}});
 document.getElementById("results").scrollIntoView({behavior:"smooth"});
}
function fill(id,arr,missing){const el=document.getElementById(id);el.innerHTML=arr.length?arr.map(x=>`<span class="${missing?"missing":""}">${x}</span>`).join(""):`<span>No gaps detected 🎉</span>`}
