const API = "http://127.0.0.1:8000";

async function createPatient() {

    const patient = {

        id: document.getElementById("id").value,
        name: document.getElementById("name").value,
        city: document.getElementById("city").value,
        age: Number(document.getElementById("age").value),
        gender: document.getElementById("gender").value,
        height: Number(document.getElementById("height").value),
        weight: Number(document.getElementById("weight").value)

    }

    await fetch(API + "/create", {

        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(patient)

    })

    alert("Patient created")

    loadPatients()
}

async function loadPatients() {

    let response = await fetch(API + "/view")
    let data = await response.json()

    let table = document.querySelector("#patientsTable tbody")

    table.innerHTML = ""

    for (let id in data) {

        let p = data[id]

        table.innerHTML += `
<tr>
<td>${id}</td>
<td>${p.name}</td>
<td>${p.city}</td>
<td>${p.age}</td>
<td>${p.bmi}</td>
<td>
<button onclick="deletePatient('${id}')">Delete</button>
</td>
</tr>
`

    }

}

async function deletePatient(id) {

    await fetch(API + "/delete/" + id, {
        method: "DELETE"
    })

    alert("Patient deleted")

    loadPatients()

}